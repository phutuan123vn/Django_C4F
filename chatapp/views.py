import datetime
from multiprocessing import context
from pprint import pprint

from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from chatapp import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from chatapp import models
from utils import generate_random_string
from rest_framework.response import Response
# Create your views here.

class ChatRoomView(ListCreateAPIView):
    serializer_class = serializers.ChatRoomSerializer
    queryset = models.Room.objects
    
    def get(self, request, *args, **kwargs):
        room_queryset = self.get_queryset()
        room = self.list(request, queryset=room_queryset)
        message_queryset = models.Message.objects.filter(room=room_queryset[0])\
                                                 .order_by('date')\
                                                 .values('user__username','date','value')
        message = self.list(request, queryset=message_queryset,
                            serializer=serializers.MessageSerializer)
        return Response({'room': room.data,
                         'messages': message.data
                         })
        

    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.POST)
        # pprint(vars(request))
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.prefetch_related('group').filter(group__user=self.request.user).order_by('id')
        return queryset
        # return self.queryset.filter(group__user=self.request.user).values('name','creator__username','id').order_by('id')
    
    def perform_create(self, serializer):
        group = Group.objects.create(name=f"room_{serializer.validated_data['name']}")
        group.user_set.add(self.request.user)
        return serializer.save(creator=self.request.user, group=group)
    
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = kwargs.pop('queryset') or None
        serializer = kwargs.pop('serializer', self.serializer_class)
        context = self.get_serializer_context()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer_data = serializer(page, many=True,context=context)
            return self.get_paginated_response(serializer_data.data)

        serializer_data = serializer(queryset, many=True,context=context)
        return serializer_data.data
    
# @method_decorator(login_required(login_url='/account/'), name='dispatch')
# class HomeView(ListView):
#     model = models.Room
#     template_name = 'chat/index.html'
#     context_object_name = 'rooms'
#     paginate_by = 5
#     query = None
    
#     def get_queryset(self):
#         groupRoom = Group.objects.filter(user=self.request.user).all()
#         self.queryset = self.model.objects.filter(group__in=groupRoom).all().order_by('id')
#         return self.queryset.values('name','creator__username','id')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.queryset:
#             msg = models.Message.objects.filter(room = context['rooms'][0]['id'])\
#                                                         .values('user__username','date','value')\
#                                                         .order_by('date')
#             paginator = Paginator(msg, 15)
#             page = paginator.get_page(paginator.num_pages)
#             context['messages'] = page.object_list
#             del page, paginator,msg
#         return context
    
# @login_required(login_url='/account/')
# def create_or_join(request:HttpRequest,pk=None):
#     if is_ajax(request):
#         typeData = request.POST.get('type')
#         if typeData == 'create':
#             containName = models.Room.objects.filter(name__icontains=request.POST.get('value')).exists()
#             if containName:
#                 return JsonResponse({'status': 'error', 'message': 'Name already exists'})
#             group = Group.objects.create(name=f"room_{request.POST.get('value')}")
#             group.user_set.add(request.user)
#             models.Room.objects.create(creator=request.user, name=request.POST.get('value'),group=group).save()
#             return JsonResponse({'status': 'success'})
#         elif typeData == 'join':
#             code = models.Code.objects.filter(code__iexact=request.POST.get('value'), expires__gte=timezone.now())
#             if code.exists():
#                 room = code.first().room
#                 room.group.user_set.add(request.user)
#                 return JsonResponse({'status': 'success', 'room_id': room.id})
#             return JsonResponse({'status': 'error', 'message': 'Code not found'})
#     return redirect('chatapp:home')


# @login_required(login_url='/account/')
# @require_http_methods(['POST'])
# def send_msg(request:HttpRequest,pk=None, *args, **kwargs):
#     room = models.Room.objects.get(pk=pk)
#     if is_ajax(request):
#         msg = models.Message.objects.create(room=room, user=request.user, value=request.POST['message'])
#         msg.save()
#         res_data = {
#             'username': request.user.username,
#             'date': msg.date,
#             'value': msg.value
#         }
#         return JsonResponse({'status': 'success', 'message': res_data})
#         # return JsonResponse({'status': 'success'})
#     # return render(request, 'chat/chat.html', {'room': room, 'messages': messages})

# @login_required(login_url='/account/')
# @require_http_methods(['GET'])
# def generate_code(request:HttpRequest,pk=None):
#     ####
#     def run():
#         code = generate_random_string()
#         unique = models.Code.objects.filter(code__iexact=code).exists()
#         while unique:
#             code = generate_random_string()
#             unique = models.Code.objects.filter(code__iexact=code).exists()
#         room = models.Room.objects.get(pk=pk)
#         models.Code.objects.create(code=code, room=room, expires=timezone.now() + datetime.timedelta(minutes=30)).save()
#         return JsonResponse({'status': 'success', 'code': code})
#     ######
#     if is_ajax(request):
#         code_exist = models.Code.objects.filter(room__id=pk)
#         if code_exist.exists():
#             code_exist = code_exist.first().expires - timezone.now() <= datetime.timedelta(minutes=25)
#             if code_exist:
#                 models.Code.objects.filter(room__id=pk).delete()
#                 return run()
#             return JsonResponse({'status': 'error', 'message': 'Code already exists or Wait for 5 minutes to generate new code'})
#         return run()
#     return redirect('chatapp:home')

# @login_required(login_url='/account/')
# @require_http_methods(['GET'])
# def getMsg(request:HttpRequest):
#     if is_ajax(request):
#         room = models.Room.objects.get(pk=request.GET.get('room_id'))
#         msg = models.Message.objects.filter(room=room).values('user__username','date','value').order_by('date')
#         paginator = Paginator(msg, 15)
#         page = paginator.get_page(paginator.num_pages)
#         return JsonResponse({'status': 'success', 'messages': list(page.object_list)})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})