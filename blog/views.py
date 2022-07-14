from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Comment, Post, User
from accounts.models import Profile
from .forms import NewCommentForm, PostSearchForm, PostCreateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404

def home(request):
    all_posts = Post.newmanager.all()
    context = {'posts': all_posts}

    return render(request, 'blog/index.html', context)

@login_required(login_url='login')
def post_create(request):
    form = PostCreateForm()
    categories = Category.objects.all()

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        try:
            image = request.FILES["image"]
        except:
            image = None

        Post.objects.create(
            author=request.user,
            category=category,
            title=request.POST.get('title'),
            image=image,
            image_caption=request.POST.get('image_caption'),
            content=request.POST.get('content'),
            status=request.POST.get('status'),
        )
        return redirect('/')

    context = {'form': form, 'categories':categories}
    return render(request, 'blog/post.html', context)

def page_not_found_view(request, exception):
    return render(request, 'blog/404.html', status=404)

@login_required(login_url='login')
def post_edit(request, pk):
    post = Post.objects.get(id=pk)
    form = PostCreateForm(instance=post)
    categories = Category.objects.all()

    if request.user != post.author:
        raise PermissionDenied


    if request.method == "POST":

        form = PostCreateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            form.category = category
            form.title = request.POST.get('title')
            form.image=request.FILES.get('image')
            form.image_caption=request.POST.get('image_caption')
            form.content=request.POST.get('content')
            form.status=request.POST.get('status')
            form.save()
            return redirect('/')
        else:
            print(form.errors)

    context = {'form': form, 'categories': categories, 'post': post}
    return render(request, 'blog/post.html', context)


@login_required(login_url='login')
def post_delete(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.author:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        post.delete()
        return redirect('/')

    context = {'post': post}
    return render(request, 'blog/modal_delete.html', context)

@login_required(login_url='login')
def post_publish(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.author:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        print('valid')
        post.status='published'
        post.save()
        return redirect('/')

    context = {'post': post}
    return render(request, 'blog/modal_publish.html', context)

def post_single(request, pk):

    post = get_object_or_404(Post, id=pk, status='published')
    fav = bool

    if post.favourites.filter(id=request.user.id).exists():
        fav = True

    allcomments = post.comments.filter(status=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 6)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    comment_form = NewCommentForm()

    return render(request, 'blog/single.html', {'post': post, 'comment_form': comment_form, 'comments':  user_comment, 'comments': comments, 'allcomments': allcomments, 'fav': fav})


def addcomment(request):
    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                result = comment_form.cleaned_data.get('content')
                user = request.user.username
                id = request.user.id
                avatar = Profile.objects.filter(user=id).values()
                avatar_url = avatar[0]['avatar']
                user_comment.author = request.user
                user_comment.save()
                return JsonResponse({'result': result, 'user': user, 'avatar_url': avatar_url})


def category(request, name):
    category = get_object_or_404(Category, name=name)

    posts = Post.newmanager.filter(category=category)
    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category.html', context)

def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {"category_list": category_list}
    return context

def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []

    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))
        if search_string is not None:
            search_string = Post.objects.filter(
                title__icontains=search_string)[:3]
            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug'))

            return JsonResponse({'search_string': data})


    if 'q' in request.GET:
        form = PostSearchForm(request.GET)

        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__icontains=q)

            results = Post.objects.filter(query)

    return render(request, 'blog/search.html',
                  {'form': form,
                   'q': q,
                   'c': c,
                   'results': results})

