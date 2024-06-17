from pprint import pprint
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView, TemplateView

import blog.models as models
from utils import user_verify

# Create your views here.


class BlogsView(ListView):
    template_name = 'blog/index.html'
    model = models.Blog
    context_object_name = 'blogs'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.values('title','description','level','user_id__username',
                               'slug','likes')
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        # print("print", context)
        pprint(context)
        return context
        
class BlogShowView(DetailView):
    template_name = 'blog/show.html'
    model = models.Blog
    context_object_name = 'blog'
    
    def get_queryset(self):
        # queryset = super().get_queryset()
        queryset = models.Blog.objects.filter(slug=self.kwargs['slug'])
        return queryset.values('title','description','level','user_id__username',
                               'slug','likes','created_at','id')
    
    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        context['comments'] = models.BlogComment.objects.filter(blog_id=self.get_object()['id'])\
                                                        .values('comment','user_id__username','created_at')\
                                                        .order_by('created_at')
        return context


@user_verify
@require_http_methods(["POST"])
def blogComment(request:HttpRequest, slug, *args, **kwargs):
    comment = request.POST['comment']
    blog = models.Blog.objects.values('id').get(slug=slug)
    query = models.BlogComment.objects.create(user_id=request.user, blog_id_id=blog['id'], comment=comment)
    query.save()
    comments = models.BlogComment.objects.filter(blog_id=blog['id'])\
                                         .values('comment','user_id__username','created_at')\
                                         .order_by('created_at')
    # print(comments)
    return JsonResponse({"status": "success",
                         "comment": list(comments)[-1]})


@user_verify
def likeBlog(request:HttpRequest, slug, *args, **kwargs):
    blog = models.Blog.objects.get(slug=slug)
    like = models.BlogLike.objects.filter(blog_id=blog, user_id=request.user)
    if like.exists():
        like.delete()
        blog.likes -= 1
    else:
        like = models.BlogLike.objects.create(blog_id=blog, user_id=request.user)
        like.save()
        blog.likes += 1
    blog.save()
    # models.Blog.objects.filter(id=blog.id).update(likes=blog.likes)
    return JsonResponse({"status": "success",
                         "likes": blog.likes})