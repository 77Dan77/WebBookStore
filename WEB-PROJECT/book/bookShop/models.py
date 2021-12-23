from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from djmoney.models.fields import MoneyField
import datetime
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField("Category", max_length=50)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Genre(models.Model):
    name = models.CharField("Genre", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Author(models.Model):
    name = models.CharField("Author", max_length=100)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class Book(models.Model):
    name = models.CharField("Title", max_length=150)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="books/")
    stock = models.PositiveSmallIntegerField("Stock", default=0)
    money = MoneyField(max_digits=6, decimal_places=2, default=0, default_currency='USD')
    year = models.PositiveSmallIntegerField("Date of Release")
    page = models.PositiveSmallIntegerField("Page Count", default=50)
    binding = models.CharField("Binding", max_length=100)
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    authors = models.ManyToManyField(Author, verbose_name="Authors")
    date = models.DateField("Date", default=datetime.date.today)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    pdf = models.FileField("PDF", upload_to='pdf/', default='pdf/blank.pdf')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={'slug': self.url})

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

class RatingStar(models.Model):
    value=models.PositiveSmallIntegerField("Value", default=0)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Star"
        verbose_name_plural = "Stars"

class Rating(models.Model):
    ip = models.CharField("IP Address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Star")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book")
    def __str__(self):
        return f"{self.star} - {self.book}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

class Review(models.Model):
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Text", max_length=1000)
    book = models.ForeignKey(Book, verbose_name="Book", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class CartProduct(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    total_price = MoneyField(max_digits=6, decimal_places=2, default=0, default_currency='USD')



class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE, related_name="usersCart")
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_amount_of_products = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    for_anonymous_user = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id)



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(default=0)
    # address = models.CharField(max_length=255, null=True, blank=True)
    orders = models.ManyToManyField('Order', blank=True, related_name='related_order')

    def __str__(self):
        return "Customer: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAYED = 'payed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_PAYED, 'Order payed'),
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order completed')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Self'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )


    customer = models.ForeignKey(Customer, related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, null=True, blank=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    buying_type = models.CharField(
        max_length=100,
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )

    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)
