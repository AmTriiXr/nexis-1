from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import activate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpRequest

from .forms import AddressForm
from .forms import ReviewForm
from .forms import PaymentForm
from .forms import PasswordResetForm

from .models import Article, ArticleDetail
from .models import Case, CaseDetail
from .models import Category
from .models import Feature, FeatureDetail
from .models import Service, ServiceDetail
from .models import Process
from .models import WhyUs
from .models import Product, ProductDetail
from .models import Review
from .models import Order, OrderItem
from .models import Address
from .models import Testimonial

from .middleware import TestimonialsMiddleware

from .tokens import generate_token
from .utils import change_password

from nexis import settings

import time
from datetime import datetime, timedelta
import string
import re
import qrcode
from PIL import Image



def forget_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:

                form.add_error(
                    'email', 'Non esiste nessun account con questo indirizzo email.')
            else:
                token_generator = default_token_generator
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                current_site = get_current_site(request)
                domain = current_site.domain
                reset_url = reverse_lazy('password_reset_confirm', kwargs={
                    'uidb64': uidb64,
                    'token': token
                })

                con = {
                    'user': user,
                    'domain': domain,
                    'reset_url': reset_url
                }

                subject = 'Reset password {}'.format(domain)
                html_message = render_to_string(
                    'reset_password_email.html', con)
                plain_message = strip_tags(html_message)
                from_email = 'no-reply@skailar.net'

                if email == "admin@skailar.net" or email == "no-reply@skailar.net":
                    send_mail(subject, plain_message, from_email,
                              ["edoardo.bergamo03@icloud.com"], html_message=html_message)
                else:
                    send_mail(subject, plain_message, from_email,
                              [email], html_message=html_message)

                return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    context = {
        'form': form
    }

    return render(request, 'forget-password.html', context)

def testimonials(request, slug=None):
    if slug:
        service = get_object_or_404(Service, slug=slug)
    else:
        service = Service.objects.all()[:6]

    testimonials = Testimonial.objects.all()
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'testimonials': testimonials,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'testimonials.html', context)

def serviceDetail(request, slug=None):
    if slug:
        serviceDetail = get_object_or_404(ServiceDetail, slug=slug)
    else:
        serviceDetail = ServiceDetail.objects.all()

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'serviceDetail': serviceDetail,
        'enough_testimonials': enough_testimonials,
    }
    return render(request, 'serviceDetail.html', context)

def index(request, slug=None):
    if slug:
        feature = get_object_or_404(Feature, slug=slug)
        service = get_object_or_404(Service, slug=slug)

    else:
        feature = Feature.objects.all()[:4]
        service = Service.objects.all()[:6]
        process = Process.objects.all()[:3]

    testimonial = Testimonial.objects.all()
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'feature': feature,
        'service': service,
        'process': process,
        'testimonial': testimonial,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'index.html', context)


def feature_detail(request, slug):
    if slug:
        feature_detail = get_object_or_404(FeatureDetail, slug=slug)
    else:
        feature_detail = FeatureDetail.objects.all()

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'feature_detail': feature_detail,
        'enough_testimonials': enough_testimonials,
    }
    return render(request, 'feature_detail.html', context)


def about(request):
    whyus = WhyUs.objects.all()

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'whyus': whyus,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'about-us.html', context)


def services(request, slug=None):
    if slug:
        service = get_object_or_404(Service, slug=slug)

    else:
        service = Service.objects.all()[:6]

    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'enough_testimonials': enough_testimonials,
        'service': service,
    }
    return render(request, 'services.html', context)


def careers(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'enough_testimonials': enough_testimonials,
        'service': service,
    }

    return render(request, 'careers.html', context)


def demo_product(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'demo_product.html', context)


def case(request, slug=None):
    if slug:
        case = get_object_or_404(Case, slug=slug)
    else:
        case = Case.objects.all()

    paginator = Paginator(case, 9)
    pagina = request.GET.get('pagina')
    case_page = paginator.get_page(pagina)

    enough_testimonials = Testimonial.objects.count() >= 10
    service = Service.objects.all()[:6]

    context = {
        'case': case,
        'case_page': case_page,
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'case.html', context)


def single_case(request, slug=None):
    if slug:
        casedetail = get_object_or_404(CaseDetail, slug=slug)
    else:
        casedetail = CaseDetail.objects.all()

    service = Service.objects.all()[:6]
    case = Case.objects.all()
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'casedetail': casedetail,
        'case': case,
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'single-case.html', context)


def tos(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'tos.html', context)


def privacy_policy(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'privacy_policy.html', context)


def products(request, slug=None):
    if slug:
        lista_product = get_object_or_404(Product, slug=slug)
    else:
        lista_product = Product.objects.all()

    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    ordering = request.GET.get('ordering')

    if ordering == 'price_asc':
        products = products.order_by('price')
    elif ordering == 'price_desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 6)
    pagina = request.GET.get('pagina')
    product = paginator.get_page(pagina)

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'product': product,
        'query': query,
        'ordering': ordering,
        'enough_testimonials': enough_testimonials,
    }
    return render(request, 'products.html', context)


@csrf_exempt
def single_product(request, slug=None):
    if slug:
        product_detail = get_object_or_404(ProductDetail, slug=slug)
        reviews = product_detail.reviews.all()
    else:
        product_detail = ProductDetail.objects.all()
        reviews = Review.objects.all()

    product = Product.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.prodotto = product_detail
            review.save()
            return redirect('single_product', slug=slug)
    else:
        form = ReviewForm()

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'product': product,
        'product_detail': product_detail,
        'form': form,
        'reviews': reviews,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'single_product.html', context)


@login_required
def cart(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = None

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'order_items': order_items,
        'order': order,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'cart.html', context)


@login_required
def checkout(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = None

    address = Address.objects.filter(user=request.user)

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'order_items': order_items,
        'order': order,
        'address': address,
        'enough_testimonials': enough_testimonials,
    }
    return render(request, 'checkout.html', context)


@login_required
def decrease_quantity(request, orderitem_id):
    order_item = get_object_or_404(OrderItem, id=orderitem_id)
    order_item.decrease_quantity()

    return redirect('cart')


@login_required
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(product__slug=product_slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart")


@login_required
def cart_remove(request, product_slug):
    order_item = OrderItem.objects.get(
        user=request.user, product__slug=product_slug, ordered=False)
    order_item.delete()
    messages.info(request, "This item was removed from your cart.")
    return redirect("cart")


def pricing(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'pricing.html', context)


def blog(request, slug=None):
    if slug:
        blogs = get_object_or_404(
            Article.objects.filter(featured=True), slug=slug)
    else:
        blogs = Article.objects.filter(featured=True)

    service = Service.objects.all()[:6]

    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('pagina')
    blog = paginator.get_page(page_number)

    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'blog': blog,
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'blog.html', context)


class RecentPostListView(ListView):
    model = Article

    def get_queryset(self):
        current_post_slug = self.get('slug')
        if current_post_slug:
            return Article.objects.exclude(slug=current_post_slug).order_by('-date')[:5]
        return Article.objects.all().order_by('-date')[:5]


def single_blog(request, slug=None):
    if slug:
        detail = get_object_or_404(
            ArticleDetail.objects.filter(featured=True), slug=slug)
    else:
        detail = ArticleDetail.objects.filter(featured=True)

    blog = Article.objects.filter(featured=True)
    queryset = Article.objects.filter(featured=True).exclude(
        slug=slug).order_by('-date')[:3]
    categories = Category.objects.all()
    service = Service.objects.all()[:6]

    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'blog': blog,
        'detail': detail,
        'queryset': queryset,
        'categories': categories,
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'blog-single.html', context)


def contact(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'contact.html', context)


@login_required
def logout_user(request):
    auth_logout(request)
    return redirect('index')


@csrf_exempt
def signup(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('index')

    if request.method == "POST":
        privacy_terms = request.POST.get('check2')
        remember_me = request.POST.get('check1')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if remember_me:
            request.session.set_expiry(30 * 24 * 60 * 60)

        else:
            request.session.set_expiry(0)

        if privacy_terms:
            expires = datetime.utcnow() + timedelta(days=30)
            response = HttpResponse()
            response.set_cookie('privacy_terms_accepted', True, expires=expires)

        else:
            expires = datetime.utcnow() + timedelta(days=30)
            response = HttpResponse()
            response.set_cookie('privacy_terms_accepted', False, expires=expires)

        digit_error = re.search(r"\d", pass1) is None
        uppercase_error = re.search(r"[A-Z]", pass1) is None
        lowercase_error = re.search(r"[a-z]", pass1) is None
        symbol_error = re.search(
            r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', pass1) is None

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist, Please try some other username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered.")
            return redirect('signup')

        if username == 'skailar'.lower() and not request.user.is_superuser:
            messages.error(
                request, "Username already exist, Please try some other username.")
            return redirect('signup')

        if username == 'admin'.lower() and not request.user.is_superuser:
            messages.error(
                request, "Username already exist, Please try some other username.")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched.")
            return redirect('signup')

        if username in pass1:
            messages.error(
                request, "Your password cannot contain your username. Please choose a different password.")
            return redirect('signup')

        if fname in pass1:
            messages.error(
                request, "Your password cannot contain your First name. Please choose a different password.")
            return redirect('signup')

        if lname in pass1:
            messages.error(
                request, "Your password cannot contain your Last name. Please choose a different password.")
            return redirect('signup')

        if email in pass1:
            messages.error(
                request, "Your password cannot contain your Last name. Please choose a different password.")
            return redirect('signup')

        if len(pass1) < 13:
            messages.error(
                request, "Your password must contain at least twelve characters.")
            return redirect('signup')

        if len(pass1) > 35:
            messages.error(
                request, "Your password must contain a maximum of 35 characters.")
            return redirect('signup')

        if digit_error:
            messages.error(
                request, "The password must contain at least one numeric character.")
            return redirect('signup')

        if uppercase_error:
            messages.error(
                request, "The password must contain at least one uppercase character.")
            return redirect('signup')

        if lowercase_error:
            messages.error(
                request, "The password must contain at least one lowercase character.")
            return redirect('signup')

        if symbol_error:
            messages.error(
                request, "The password must contain at least one symbol.")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect('signup')

        for i in range(len(pass1) - 2):
            if pass1[i] == pass1[i+1] == pass1[i+2]:
                messages.error(
                    request, "The password must not contain three consecutive identical characters.")
                return redirect('signup')

        for i in range(len(pass1) - 2):
            chars = pass1[i:i+3]
            if all(c in string.digits for c in chars) and (chars in string.digits or chars[::-1] in string.digits):
                messages.error(
                    request, "Your password cannot contain three consecutive digits.")
                return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(
            request, "Your Account has been created succesfully! Please check your email to confirm your email address in order to activate your account.")

        current_site = get_current_site(request)

        context = {
            'name': myuser.first_name,
            'surname': myuser.last_name,
            'user': myuser.username,
            'domain': current_site.domain,
        }

        subject = "Welcome to Skailar!"
        html_message = render_to_string('email_welcome.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]

        if to_list == "admin@skailar.net" or to_list == "no-reply@skailar.net":
            send_mail(subject, plain_message, from_email, [
                      "edoardo.bergamo03@icloud.com"], html_message=html_message)
        else:
            send_mail(subject, plain_message, from_email,
                      to_list, html_message=html_message)

        current_site = get_current_site(request)

        context = {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        }

        email_subject = "Confirm your Email - Skailar"
        html_message = render_to_string('email_confirmation.html', context)
        plain_message = strip_tags(html_message)
        from_email = "no-reply@skailar.net"
        to_email = myuser.email

        if to_email == "admin@skailar.net" or to_email == "no-reply@skailar.net":
            send_mail(email_subject, plain_message, from_email, [
                      "edoardo.bergamo03@icloud.com"], html_message=html_message)
        else:
            send_mail(email_subject, plain_message, from_email,
                      [to_email], html_message=html_message)

        return redirect('login')

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, "register.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!")
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')


def login_view(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        remember_me = request.POST.get('check1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            if remember_me:
                expires = datetime.utcnow() + timedelta(days=30)
                response = HttpResponse()
                response.set_cookie(
                    'privacy_terms_accepted',
                    value='true',
                    expires=expires,
                    domain='skailar.net',
                    path='/',
                    secure=True,
                    httponly=True,
                )
                request.session.set_expiry(30 * 24 * 60 * 60)
            else:
                expires = datetime.utcnow() + timedelta(0)
                response = HttpResponse()
                response.set_cookie(
                    'privacy_terms_accepted',
                    value='false',
                    expires=expires,
                    domain='skailar.net',
                    path='/',
                    secure=True,
                    httponly=True,
                )
                request.session.set_expiry(0)
            login(request, user)
            fname = user.first_name
            return redirect('index')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("login")

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, "login.html", context)


@login_required
def my_account(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        passwd = request.POST.get('password')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        digit_error = re.search(r"\d", pass1) is None
        uppercase_error = re.search(r"[A-Z]", pass1) is None
        lowercase_error = re.search(r"[a-z]", pass1) is None
        symbol_error = re.search(
            r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', pass1) is None

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered.")
            return redirect('my_account')

        if pass1 == passwd:
            messages.error(
                request, "Password already in use, Please try some other password.")
            return redirect('my_account')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched.")
            return redirect('my_account')

        if fname in pass1:
            messages.error(
                request, "Your password cannot contain your First name. Please choose a different password.")
            return redirect('my_account')

        if lname in pass1:
            messages.error(
                request, "Your password cannot contain your Last name. Please choose a different password.")
            return redirect('my_account')

        if email in pass1:
            messages.error(
                request, "Your password cannot contain your Email. Please choose a different password.")
            return redirect('my_account')

        if len(pass1) < 13:
            messages.error(
                request, "Your password must contain at least twelve characters.")
            return redirect('my_account')

        if len(pass1) > 35:
            messages.error(
                request, "Your password must contain a maximum of 35 characters.")
            return redirect('my_account')

        if digit_error:
            messages.error(
                request, "The password must contain at least one numeric character.")
            return redirect('my_account')

        if uppercase_error:
            messages.error(
                request, "The password must contain at least one uppercase character.")
            return redirect('my_account')

        if lowercase_error:
            messages.error(
                request, "The password must contain at least one lowercase character.")
            return redirect('my_account')

        if symbol_error:
            messages.error(
                request, "The password must contain at least one symbol.")
            return redirect('my_account')

        myuser = request.user

        if fname != myuser.first_name:
            myuser.first_name = fname

        if lname != myuser.last_name:
            myuser.last_name = lname

        if email != myuser.email:
            myuser.is_active = False
            myuser.email = email

            myuser.save()

            current_site = get_current_site(request)

            context = {
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            }

            email_subject = "Confirm your Email - Skailar"
            html_message = render_to_string('email_confirmation.html', context)
            plain_message = strip_tags(html_message)
            from_email = "no-reply@skailar.net"
            to_email = email

            send_mail(email_subject, plain_message, from_email,
                      [to_email], html_message=html_message)

            redirect("login")

        elif email == myuser.email:
            pass

        if phone:
            myuser.phone = phone

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10
    user = request.user

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
        'user': user,
    }

    return render(request, 'my-account.html', context)


@login_required
def my_orders(request):
    order_qs = Order.objects.filter(user=request.user, ordered=True)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = None

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'order_items': order_items,
        'order': order,
        'enough_testimonials': enough_testimonials,
    }
    return render(request, 'my-orders.html', context)


@login_required
def my_addresses(request):
    service = Service.objects.all()[:6]
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('my_addresses')
    else:
        form = AddressForm()

    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'form': form,
        'addresses': addresses,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'my-addresses.html', context)

def my_subscriptions(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'subscriptions.html', context)



def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('my_addresses')


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


def faq(request):
    service = Service.objects.all()[:6]
    enough_testimonials = Testimonial.objects.count() >= 10

    context = {
        'service': service,
        'enough_testimonials': enough_testimonials,
    }

    return render(request, 'faq.html', context)


def maintenance(request):
    if not settings.MAINTENANCE_MODE:
        raise Http404("La pagina richiesta non è stata trovata.")

    return render(request, 'coming.html')


def process_payment(request):
    return render(request, 'process_payment.html')


@csrf_exempt
def payment_confirmation(request):
    address = Address.objects.filter(user=request.user)
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    order = Order.objects.filter(user=request.user)

    user = address.first()

    context = {'address': address, 'order_items': order_items, 'order': order}

    subject = 'Payment Confirmation - Skailar'
    html_message = render_to_string('payment_confirmation_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'no-reply@skailar.net'
    to_email = user.email

    if to_email == "admin@skailar.net" or to_email == "no-reply@skailar.net":
        send_mail(subject, plain_message, from_email, [
                  "edoardo.bergamo03@icloud.com"], html_message=html_message)
    else:
        send_mail(subject, plain_message, from_email, [
                  to_email], html_message=html_message)

    return redirect('my_orders')