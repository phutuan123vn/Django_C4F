from django.urls import path
from blog import views


urlpatterns = [
    path("", views.BlogList.as_view(), name="home"),
    # path("create/", views.BlogCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.BlogDetailComment.as_view(), name="detail"),
    # path("<slug:slug>/", views.BlogCommentCreate.as_view(), name="comment"),
    # path("comment/<slug:slug>/", views.blogComment, name="comment"),
    # path('like/<slug:slug>/', views.likeBlog, name="like"),
    # path("<slug:slug>/", views.BlogShowView.as_view(), name="show"),
]
