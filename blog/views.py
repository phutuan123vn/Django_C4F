from pprint import pprint
from typing import Any

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Prefetch
from blog import models, serializers
from django.db.models import Prefetch


class BlogList(generics.ListCreateAPIView):
    #### Comment Authenticateion and Permission for production
    # authentication_classes = []
    # permission_classes = [AllowAny,]
    ##################################
    queryset = models.Blog.objects.all().order_by("created_at")
    serializer_class = serializers.BlogSerializer
    
    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)
    
class BlogDetail(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [AllowAny,]
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogDetailSerializer
    lookup_field = "slug"
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class BlogCommentCreate(generics.CreateAPIView):
    #### Comment Authenticateion and Permission for production
    # authentication_classes = []
    # permission_classes = [AllowAny,]
    ##################################
    queryset = models.BlogComment.objects.all()
    serializer_class = serializers.BlogCommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
        
        
class BlogDetailComment(generics.ListAPIView):
    #### Comment Authenticateion and Permission for production
    # authentication_classes = []
    # permission_classes = [AllowAny,]
    ##################################
    lookup_field = "slug"
    serializer_class = serializers.BlogCommentSerializer
    queryset = models.Blog.objects.prefetch_related(Prefetch(
                                                        "blog_comment",
                                                        queryset=models.BlogComment.objects.order_by("created_at").only("comment","created_at","user_id__username")
                                                    ),
                                                    "blog_like__user_id")\
                                #   .only("blog_comment__comment","blog_comment__created_at")
                                #   .only("blog_comment__comment","blog_comment__created_at")
    
    def get(self, request: Request,slug:str) -> Response:
        response = Response()
        blog = self.get_object()
        comments = self.list(request,
                             queryset=blog.blog_comment.all(),
                             serializer=serializers.BlogCommentSerializer
                             )
        if bool(request.query_params.get('page', None)):
            response.data = {"comments": comments.data}
            return response
        like_user_queryset = blog.blog_like.all()
        blog = serializers.BlogSerializer(blog,context=self.get_serializer_context()).data
        response.data = {
            "blog": blog,
            "comments":comments.data,
            "author": blog['user_id'] == request.user.id,
            "liked": like_user_queryset.filter(user_id=request.user.id).exists(),
            }
        return response
    
    def list(self, request, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        serializer_class = kwargs.pop('serializer', self.serializer_class)
        context = self.get_serializer_context()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context=context)
        return serializer.data
       
    
    def post(self, request: Request, slug: str) -> Response:
        blog = self.get_object()
        data = request.data.copy()
        # print(data)
        serializer = serializers.BlogCommentSerializer(data={
            "comment": data['comment'],
            "user_id": data['user_id'],
        })
        if serializer.is_valid():
            # serializer.save()
            serializer.save(blog_id=blog)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
# class BlogCreateView(generics.CreateAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny,]
#     queryset = models.Blog.objects.all()
#     serializer_class = serializers.BlogSerializer
    
#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user)