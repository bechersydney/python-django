from django.contrib.auth import authenticate, login, logout
from .form import MyUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # restriction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message, User
from .form import RoomForm, UserForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except Exception:
            messages.error(request, "User doesn't exist")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username and pass do not exist")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # freeze the saving first
            user.username = user.username.lower()
            user.save()
            login(request, user)  # automatically log in
            return redirect('login')
        else:
            messages.error(request, 'An error occur during registration')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )  # icontains used in matching
    topics = Topic.objects.all().order_by('name')
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room_by_id = Room.objects.get(id=pk)
    room_messages = room_by_id.message_set.all().order_by('-created_at')  # get message using the modelname_set
    participants = room_by_id.participants.all()
    context = {
        'room': room_by_id,
        'room_messages': room_messages,
        'participants': participants
    }
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room_by_id,
            body=request.POST.get('comment')
        )
        room_by_id.participants.add(request.user)
        return redirect('room', pk=room_by_id.id)

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.topic = request.POST.get('topic')
        #     room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room_by_id = Room.objects.get(id=pk)
    form = RoomForm(instance=room_by_id)  # pre fill the values in form
    topics = Topic.objects.all()
    if request.user != room_by_id.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room_by_id.name = request.POST.get('name')
        room_by_id.topic = topic
        room_by_id.description = request.POST.get('description')
        room_by_id.save()
        return redirect('home')
    context = {
        'form': form,
        'topics': topics,
        'room': room_by_id,
        'is_update': True
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room_by_id = Room.objects.get(id=pk)
    if request.user != room_by_id.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room_by_id.delete()
        return redirect('home')
    context = {'obj': room_by_id}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_comment(request, pk):
    message = Message.objects.get(pk=pk)
    if message.user != request.user:
        return HttpResponse('You are not allowed to delete message')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()  # get rooms from user using mode_set.all
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'room_messages': room_messages
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


@login_required(login_url='login')
def topics(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q)
     ).order_by('name')  # icontains used in matching
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


@login_required(login_url='login')
def activities(request):
    messages = Message.objects.all()
    context = {'room_messages': messages}
    return render(request, 'base/activity.html', context)
