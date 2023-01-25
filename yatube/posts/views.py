from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post
from .forms import PostForm
from users.forms import User

POSTS_ON_SCREEN = 10


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    text = 'Последние обновления на сайте'
    context = {
        'title': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)[:POSTS_ON_SCREEN]
    paginator = Paginator(post_list, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    text = f'Записи сообщества {group.title}'
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': text,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    paginator = Paginator(posts, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    id = Post.objects.get(id=post_id)
    template = 'posts/post_detail.html'
    context = {
        'posts': posts,
        'id': id,
        'title': f'{posts.text[:30]}'
    }
    return render(request, template, context)


@login_required
def post_create(request):
    is_edit = False
    form = PostForm()
    template = 'posts/create_post.html'
    context = {'form': form,
               'is_edit': is_edit}
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", post.author)
        return render(request, template, context)
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form.save()
        return redirect('posts:post_detail', post_id)
    template = 'posts/create_post.html'
    context = {'form': form,
               'post': post,
               'is_edit': is_edit}
    return render(request, template, context)
