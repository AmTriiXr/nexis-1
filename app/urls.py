from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.i18n import set_language
from django.views.static import serve
from .views import custom_page_not_found
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('about-us', views.about, name="about"),

    path('services', views.services, name="services"),
    path('service/<str:slug>', views.serviceDetail, name="serviceDetail"),

    path('careers', views.careers, name="careers"),
    path('demo-product', views.demo_product, name="demo_product"),
    path('cases', views.case, name="case"),
    path('case/<str:slug>', views.single_case, name="single_case"),

    path('legal/terms', views.tos, name="terms_of_service"),
    path('legal/privacy', views.privacy_policy, name="privacy_policy"),

    path('products', views.products, name="products"),
    path('product/<str:slug>', views.single_product, name="single_product"),
    path('pricing', views.pricing, name="pricing"),
    path('contact', views.contact, name="contact"),
    path('feature/<str:slug>', views.feature_detail, name="feature_detail"),
    path('cart', views.cart, name='cart'),
    path('add_to_cart/<slug:product_slug>', views.add_to_cart, name='add_to_cart'),
    path('cart_remove/<slug:product_slug>', views.cart_remove, name='cart_remove'),
    path('decrease_quantity/<int:orderitem_id>', views.decrease_quantity, name='decrease_quantity'),
    path('logout/', views.logout_user, name="logout_user"),

    path('account', views.my_account, name="my_account"),
    path('account/orders', views.my_orders, name="my_orders"),
    path('account/addresses', views.my_addresses, name="my_addresses"),
    path('account/subscriptions', views.my_subscriptions, name="my_subscriptions"),

    path('register', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('checkout', views.checkout, name='checkout'),
    path('forget-password', views.forget_password, name='forget_password'),
    path('frequently-asked-questions', views.faq, name="faq"),

    path('testimonials', views.testimonials, name='testimonials'),

    path('news', views.blog, name="blog"),
    path('new/<str:slug>', views.single_blog, name="single_blog"),

    path('maintenance', views.maintenance, name='maintenance'),
    path('process-payment', views.process_payment, name='process_payment'),
    path('payment-confirmation', views.payment_confirmation, name='payment_confirmation'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('tinymce/', include('tinymce.urls')),

    path('addresses/<int:pk>/delete/', views.delete_address, name='delete_address'),

    path('api/generate_qr_code/', views.generate_qr_code, name="generate_qr"),

    path('tos', RedirectView.as_view(url='/legal/terms', permanent=True)),
    path('tos/', RedirectView.as_view(url='/legal/terms', permanent=True)),
    path('privacy', RedirectView.as_view(url='/legal/privacy', permanent=True)),
    path('privacy-policy', RedirectView.as_view(url='/legal/privacy', permanent=True)),
    path('privacy-policy/', RedirectView.as_view(url='/legal/privacy', permanent=True)),
    path('privacy/', RedirectView.as_view(url='/legal/privacy', permanent=True)),
    path('products/', RedirectView.as_view(url='/products', permanent=True)),
    path('product/', RedirectView.as_view(url='/products', permanent=True)),
    path('product', RedirectView.as_view(url='/products', permanent=True)),
    path('register/', RedirectView.as_view(url='/register', permanent=True)),
    path('signup', RedirectView.as_view(url='/register', permanent=True)),
    path('signup/', RedirectView.as_view(url='/register', permanent=True)),
    path('case/', RedirectView.as_view(url='/cases', permanent=True)),
    path('case', RedirectView.as_view(url='/cases', permanent=True)),
    path('login/', RedirectView.as_view(url='/login', permanent=True)),
    path('signin', RedirectView.as_view(url='/login', permanent=True)),
    path('service', RedirectView.as_view(url='/services', permanent=True)),
    path('service/', RedirectView.as_view(url='/services', permanent=True)),
    path('signin/', RedirectView.as_view(url='/login', permanent=True)),
    path('faq/', RedirectView.as_view(url='/frequently-asked-questions', permanent=True)),
    path('faq', RedirectView.as_view(url='/frequently-asked-questions', permanent=True)),
    path('frequently-asked-questions/', RedirectView.as_view(url='/frequently-asked-questions', permanent=True)),
    

    path('blog/', RedirectView.as_view(url='/blog', permanent=True)),
    
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]

handler404 = 'app.views.custom_page_not_found'
