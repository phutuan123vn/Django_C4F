from django.urls import path
from blog import views


urlpatterns = [
    path("", views.BlogsView.as_view(), name="home"),
    path("comment/<slug:slug>/", views.blogComment, name="comment"),
    path('like/<slug:slug>/', views.likeBlog, name="like"),
    path("<slug:slug>/", views.BlogShowView.as_view(), name="show"),
]
