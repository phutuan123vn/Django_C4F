from django.urls import path,include,re_path
import chatapp.views as views

# urlpatterns = [
#     path('', views.HomeView.as_view(), name='home'),
#     path('create/', views.create_or_join, name='create'),
#     path('generate/<int:pk>/', views.generate_code, name='generate'),
#     path('sendmsg/<int:pk>/',views.send_msg, name='sendmsg'),
#     path('get-msg/', views.getMsg, name="getmsg"),
#     path('join/<int:pk>/', views.create_or_join, name='chat'),
# ]

urlpatterns = [
    path('',views.ChatRoomView.as_view(),name='room'),
    path('code/',views.ChatCodeView.as_view(),name='code'),
    path('code/<int:room_id>/',views.ChatCodeView.as_view(),name='code'),
    path('<int:room_id>/',views.ChatMessageView.as_view(),name='room'),
]
