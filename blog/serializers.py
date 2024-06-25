from django.contrib.auth.models import User
from rest_framework import serializers, pagination
from django.core.paginator import Paginator
from blog import models


class BlogSerializer(serializers.ModelSerializer):
    # user_id = serializers.HyperlinkedRelatedField()
    blog = serializers.HyperlinkedIdentityField(view_name="blog:detail", lookup_field="slug")
    
    class Meta:
        model = models.Blog
        fields = "__all__"
        read_only_fields = ['likes']
        
    def create(self, validated_data):
        return models.Blog.objects.create(**validated_data)
        
        
class BlogCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username')
    # user = serializers.
    
    class Meta:
        model = models.BlogComment
        fields = ['id','username','comment','created_at']
        
    def create(self, validated_data):
        # print(validated_data)
        return models.BlogComment.objects.create(**validated_data)
        
        
class BlogLikeSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user_id.username")
    
    class Meta:
        model = models.BlogLike
        fields = ["id","username"]
        
        
class BlogDetailSerializer(serializers.ModelSerializer):
    # blog_comment = BlogCommentSerializer(many=True)
    blog_comment = serializers.SerializerMethodField()
    blog_like = BlogLikeSerializer(many=True) 
    
    
    class Meta:
        model = models.Blog
        fields = "__all__"
        
    # def get_blog_like(self,obj):
    #     return obj.blog_like.order_by("-created_at")
        
    def get_blog_comment(self,obj):
        paginator = pagination.PageNumberPagination()
        page_number = self.context['request'].query_params.get('page')
        comments_queryset = models.BlogComment.objects.filter(blog_id=obj).order_by("-created_at")
        paginated_queryset = paginator.paginate_queryset(comments_queryset, self.context['request'], view=self)
        
        if paginated_queryset is not None:
            serializer = BlogCommentSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data).data
        
        serializer = BlogCommentSerializer(comments_queryset, many=True)
        return serializer.data


