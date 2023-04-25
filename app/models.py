from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

class Feature(models.Model):
    flaticon = models.CharField(max_length=255, null=True, default=None)
    name = models.CharField(_('nome'), max_length=55)
    desc = models.TextField(_('description'))
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class FeatureDetail(models.Model):
    main_img = models.ImageField(upload_to='media/feature_detail/')
    titolo = models.CharField(_('titolo'), max_length=500)
    body_uno = models.TextField(_('body1'))
    body_due = models.TextField(_('body2'))
    img_uno = models.ImageField(upload_to='media/feature_detail/')
    img_due = models.ImageField(upload_to='media/feature_detail/')
    titolo_due = models.CharField(_('titolo_due'), max_length=255, blank=True, null=True)
    body_tre = models.TextField(_('body3'))
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titolo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titolo
    
class Service(models.Model):
    flaticon = models.CharField(max_length=255, null=True, default=None)
    name = models.CharField(_('name'), max_length=55)
    desc = models.TextField( _('desc'))
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ServiceDetail(models.Model):
    title = models.CharField(max_length=255, default="Untitled")
    image = models.ImageField(upload_to='media/service_details/', null=True, blank=True, default=None)
    content = HTMLField(default=None)
    slug = models.SlugField(unique=True, null=True, blank=False, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title 


class Process(models.Model):
    image = models.ImageField(upload_to='media/process/')
    name = models.CharField(_('name'), max_length=55)
    desc = models.TextField(_('desc'))

    def __str__(self):
        return self.name
    
class WhyUs(models.Model):
    image = models.ImageField(upload_to='media/process/')
    name = models.CharField(_('name'), max_length=55)
    desc = models.TextField(_('desc'))

    def __str__(self):
        return self.name
    
class Product(models.Model):
    image = models.ImageField(upload_to='media/products/', null=True)
    modello = models.CharField(_('modello'), max_length=20, null=True, default=None)
    name = models.CharField(_('name'), max_length=100)
    price = models.FloatField(_('price'))
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductDetail(models.Model):
    image_uno = models.ImageField(upload_to='media/product_details/')
    modello = models.CharField(max_length=20, null=True, default=None)
    image_due = models.ImageField(upload_to='media/product_details/')
    image_tre = models.ImageField(upload_to='media/product_details/')
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    intro = models.TextField()
    desc = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def decrease_quantity(self):
        if self.quantity != 1:
            self.quantity -= 1
        self.save()

class Order(models.Model):
    PAYMENT_METHODS = (
            ('Bank Transfer', 'bank_transfer'),
            ('Credit Card', 'credit_card')
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default='1')
    payment_method = models.CharField(choices=PAYMENT_METHODS, default='Credit Card', max_length=50)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s order"

    def get_subtotal_order_price(self):
        subtotal = 0
        for item in self.items.all():
            subtotal += item.get_total_price()
        return subtotal

    def calculate_shipping_cost(self):
        shipping_threshold = 500
        shipping_cost = 30
        order_total = self.get_subtotal_order_price()
        if order_total >= shipping_threshold:
            return 0
        else:
            return shipping_cost

    def get_total_order_price(self):
        subtotal = self.get_subtotal_order_price()
        shipping_cost = self.calculate_shipping_cost()
        total = subtotal + shipping_cost
        return total
    
    def paymentconfirmation(self):
        self.ordered = True
        self.save()
    
class Review(models.Model):
    prodotto = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, related_name='reviews', default=None)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    author_image = models.ImageField(upload_to='media/review/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Review"
        get_latest_by = 'timestamp'
        ordering = ['-timestamp']

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True, default='/assets/images/avatar.png')

class Case(models.Model):
    image = models.ImageField(upload_to='media/cases/', default=None)
    name = models.CharField(max_length=55)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class CaseDetail(models.Model):
    main_img = models.ImageField(upload_to='media/cases_details/')
    titolo = models.CharField(max_length=500)
    body_uno = models.TextField()
    body_due = models.TextField()
    img_uno = models.ImageField(upload_to='media/cases_details/')
    img_due = models.ImageField(upload_to='media/cases_details/')
    titolo_due = models.CharField(max_length=255, blank=True, null=True)
    body_tre = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titolo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titolo

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', default=1)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, default='')
    country = models.CharField(max_length=50, default='')
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=500, default='')
    phone = PhoneNumberField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.street_address} {self.city}, {self.state} {self.zip_code} {self.country}"

    def __repr__(self):
        return f"Address(street_address='{self.street_address}', city='{self.city}', state='{self.state}', zip_code='{self.zip_code}', country='{self.country}')"

    class Meta:
        default_related_name = 'addresses'

    class Meta:
        unique_together = ['user', 'street_address']

class Article(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/articles/', null=True, blank=True)
    authors = models.ImageField(upload_to='media/author/', null=True, blank=True)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='article_likes', blank=True)
    categories = models.ManyToManyField('Category', related_name='articles')
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/articles_details/', null=True, blank=True)
    authors = models.ImageField(upload_to='media/author/', null=True, blank=True)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    categories = models.ManyToManyField('Category', related_name='article_details')
    slug = models.SlugField(unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title 


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=False)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    pic = models.ImageField(upload_to='media/testimonials/')
    name = models.CharField(max_length=255)
    testimonial = models.TextField()
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Testimonials'

    @staticmethod
    def enough_testimonials():
        return Testimonial.objects.count() >= 50
