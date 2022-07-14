from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PwdResetForm, PwdChangeForm, PwdResetForm, PwdResetConfirmForm

app_name = 'accounts'

urlpatterns = [
    path('register/', views.accounts_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html", form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html", form_class=PwdChangeForm, success_url='/account/password_change_done/'), name='pwdforgot'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html", form_class=PwdResetForm, success_url='/account/password_reset_done/'), name='pwdreset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', form_class=PwdResetConfirmForm, success_url='/account/password_reset_complete/'), name="pwdresetconfirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('profile/favourites/', views.favourite_list, name='favourite_list'),

    path('like/', views.like, name='like'),
    path('thumbs/', views.thumbs, name='thumbs'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/delete/', views.delete_user, name='deleteuser'),

    path('drafts/', views.drafts, name='drafts'),

]

