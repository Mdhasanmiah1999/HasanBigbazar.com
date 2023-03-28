from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from app import views

from django.contrib.auth import views as auth_views
from .forms import forms as LoginForm, MypasswordChangeForm
from .forms import forms as MypasswordResetForm
from .forms import MySetPasswordForm
from .forms import forms as SearchResultsView
from django.contrib import admin  
from .views import *


urlpatterns = [
    path('admin/sync-sql-kb/', admin.site.urls),

    path('admin/', admin.site.urls, name='admin'),  
    path('', views.ProductView.as_view(), name='home'),
    path('home/', views.ProductView.as_view(), name='home'),
    path('search/', views.SearchProduct, name='search'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('plus-cart/', views.plus_cart, name='plus-cart'),
    path('minus-cart/', views.minus_cart, name='minus-cart'),
    path('donate/', DonateView, name='donate'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout1/', views.checkout1, name='checkout1'),
     path('payment/success/', views.CheckoutSuccessView.as_view(), name='success'),
    path('payment/faild/', views.CheckoutFaildView.as_view(), name='faild'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
     path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
     path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MypasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('fairebase_login/', auth_views.LoginView.as_view(template_name='app/fairebase_login.html')),    
    #path('fairebase_login_save/', views.firebase_login_save)
    path('test_cookie/', views.test_cookie, name='test_cookie'),
    path('scookie',views.setcookie),  
    path('gcookie',views.getcookie)  
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


