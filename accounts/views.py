from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm, UserProfileForm
from .tokens import account_activation_token
from .models import Profile
from blog.models import Post, Vote
from django.db.models import F, Q


def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Post.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():

            q = Vote.objects.get(
                Q(post_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            if evote == True:
                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    q.vote = False
                    q.save(update_fields=['vote'])

                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})
            pass

            if evote == False:
                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    q.vote = True
                    q.save(update_fields=['vote'])

                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:
            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
                update.save()
                new = Vote(post_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()
                new = Vote(post_id=id, user_id=request.user.id, vote=False)
                new.save()

            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass


@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        context = {'result': result, }
        return JsonResponse(context)


@ login_required
def favourite_list(request):
    new = Post.newmanager.filter(favourites=request.user)
    context = {'new': new}
    return render(request, 'accounts/favourites.html', context)


@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {"avatar": avatar}
        return context
    else:
        return {'NotLoggedIn': User.objects.none()}


@login_required
def profile(request):
    posts = Post.newmanager.filter(author=request.user)
    context = {'posts': posts, 'section': 'profile'}
    return render(request, 'accounts/profile.html', context)

@login_required
def drafts(request):
    posts = Post.objects.filter(author=request.user, status='draft')
    context = {'posts': posts}
    return render(request, 'accounts/draft.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'accounts/update.html', context)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')


def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:login')
    else:
        return render(request, 'registration/activation_invalid.html')

