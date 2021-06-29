from django.conf import settings  # noqa
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm

from .models import Group, Post
from yatube.settings import POSTS_PER_PAGE

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/index.html', {
        'page': page,
        'post_list': post_list})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post = Post.objects.filter(group=group)
    paginator = Paginator(post, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/group.html', {
        'group': group,
        'page': page, 'post': post})


def profile(request, username):
    username = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=username)
    paginator = Paginator(post, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/profile.html', {
        'username': username,
        'page': page, 'post': post})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    return render(request, 'posts/post.html', {
        'username': username, 'post': post})


@login_required
def new_post(request):
    action_name = 'Добавить запись'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'posts/new.html', {
        'form': form,
        'action_name': action_name})


@login_required
def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(
        Post,
        author__username=username,
        id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    action_name = 'Редактировать запись'

    if form.is_valid():
        form.save()
        return redirect('post', username=post.author, post_id=post.pk)

    return render(request, 'posts/new.html', {
        'form': form,
        'action_name': action_name})


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
