import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from chatapp import models
from utils import generate_random_string, is_ajax

# Create your views here.

# decorators.method_decorator(login_required(login_url='/account/login'), name='dispatch')

@method_decorator(login_required(login_url='/account/'), name='dispatch')
class HomeView(ListView):
    model = models.Room
    template_name = 'chat/index.html'
    context_object_name = 'rooms'
    paginate_by = 5
    query = None
    
    def get_queryset(self):
        groupRoom = Group.objects.filter(user=self.request.user).all()
        self.queryset = self.model.objects.filter(group__in=groupRoom).all().order_by('id')
        return self.queryset.values('name','creator__username','id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.queryset:
            msg = models.Message.objects.filter(room = context['rooms'][0]['id'])\
                                                        .values('user__username','date','value')\
                                                        .order_by('date')
            paginator = Paginator(msg, 15)
            page = paginator.get_page(paginator.num_pages)
            context['messages'] = page.object_list
            del page, paginator,msg
        return context
    
@login_required(login_url='/account/')
def create_or_join(request:HttpRequest,pk=None):
    if is_ajax(request):
        typeData = request.POST.get('type')
        if typeData == 'create':
            containName = models.Room.objects.filter(name__icontains=request.POST.get('value')).exists()
            if containName:
                return JsonResponse({'status': 'error', 'message': 'Name already exists'})
            group = Group.objects.create(name=f"room_{request.POST.get('value')}")
            group.user_set.add(request.user)
            models.Room.objects.create(creator=request.user, name=request.POST.get('value'),group=group).save()
            return JsonResponse({'status': 'success'})
        elif typeData == 'join':
            code = models.Code.objects.filter(code__iexact=request.POST.get('value'), expires__gte=timezone.now())
            if code.exists():
                room = code.first().room
                room.group.user_set.add(request.user)
                return JsonResponse({'status': 'success', 'room_id': room.id})
            return JsonResponse({'status': 'error', 'message': 'Code not found'})
    return redirect('chatapp:home')


@login_required(login_url='/account/')
@require_http_methods(['POST'])
def send_msg(request:HttpRequest,pk=None, *args, **kwargs):
    room = models.Room.objects.get(pk=pk)
    if is_ajax(request):
        msg = models.Message.objects.create(room=room, user=request.user, value=request.POST['message'])
        msg.save()
        res_data = {
            'username': request.user.username,
            'date': msg.date,
            'value': msg.value
        }
        return JsonResponse({'status': 'success', 'message': res_data})
        # return JsonResponse({'status': 'success'})
    # return render(request, 'chat/chat.html', {'room': room, 'messages': messages})

@login_required(login_url='/account/')
@require_http_methods(['GET'])
def generate_code(request:HttpRequest,pk=None):
    ####
    def run():
        code = generate_random_string()
        unique = models.Code.objects.filter(code__iexact=code).exists()
        while unique:
            code = generate_random_string()
            unique = models.Code.objects.filter(code__iexact=code).exists()
        room = models.Room.objects.get(pk=pk)
        models.Code.objects.create(code=code, room=room, expires=timezone.now() + datetime.timedelta(minutes=30)).save()
        return JsonResponse({'status': 'success', 'code': code})
    ######
    if is_ajax(request):
        code_exist = models.Code.objects.filter(room__id=pk)
        if code_exist.exists():
            code_exist = code_exist.first().expires - timezone.now() <= datetime.timedelta(minutes=25)
            if code_exist:
                models.Code.objects.filter(room__id=pk).delete()
                return run()
            return JsonResponse({'status': 'error', 'message': 'Code already exists or Wait for 5 minutes to generate new code'})
        return run()
    return redirect('chatapp:home')

@login_required(login_url='/account/')
@require_http_methods(['GET'])
def getMsg(request:HttpRequest):
    if is_ajax(request):
        room = models.Room.objects.get(pk=request.GET.get('room_id'))
        msg = models.Message.objects.filter(room=room).values('user__username','date','value').order_by('date')
        paginator = Paginator(msg, 15)
        page = paginator.get_page(paginator.num_pages)
        return JsonResponse({'status': 'success', 'messages': list(page.object_list)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})