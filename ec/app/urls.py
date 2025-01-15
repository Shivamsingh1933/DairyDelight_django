from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.urls import path
from . import views
from django.urls import path
from django.urls import path
from . import views
from .views import checkout


urlpatterns = [
    path("", views.home, name="home"),
    path('contact/', views.contact, name="contact" ),
    path('about/', views.about, name="about"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>', views.updateAddressView.as_view(), name='updateAddress'),
   
    path('checkout/', checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone', views.payment_done, name='payment_done'),
    path('download_receipt/<str:payment_id>/', views.download_receipt, name='download_receipt'),
    path('search/', views.search, name='search'),
    
    #path('payment/success/', PaymentSuccess.as_view(), name='payment_success'),

    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
  
    #path('checkout/', checkout.as_view(), name='checkout'),
    path('orders/', views.home, name='orders'),


    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    path('wishlist/', views.show_wishlist, name='wishlist'),

    #path("send-payment-link/", views.send_payment_link, name="send_payment_link"),
    
   
    
    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'), name ='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'login'), name='logout'),
    
    
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = 'app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'), name ='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html',form_class = MySetPasswordForm), name ='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'), name ='password_reset_complete'),
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
