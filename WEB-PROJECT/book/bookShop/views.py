
# Create your views here.
import stripe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .mixins import CartMixin
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, request
from django.contrib.contenttypes.models import ContentType
from .forms import RegistrationForm, LoginForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from django.shortcuts import redirect

# def get_product_url(obj, viewname):
#     ct_model = obj.__class__.meta.model_name
#     return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})
# @login_required
@require_http_methods(["GET"])
def get(request):
    booksFirst = Book.objects.order_by('-date')[:7]
    booksSecond = Book.objects.order_by('-date')[7:14]
    booksThird = Book.objects.order_by('-date')[14:21]
    booksBest = Book.objects.filter(category=3).order_by('-stock')[:7]
    bookWesterns = Book.objects.filter(category=18).order_by('-stock')[:7]
    bookFiction = Book.objects.filter(category=6).order_by('-stock') | Book.objects.filter(category=21).order_by('-stock') | Book.objects.filter(category=24).order_by('-stock')

    # template = loader.get_template('bookShop/Main.html')  # getting our template
    # return HttpResponse(template.render())
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)

        cart = Cart.objects.filter(owner=customer).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)

        cart = Cart.objects.get(owner=customer)
        return render(request, "bookShop/Main.html", {"book_list_First": booksFirst, "book_list_Second": booksSecond, "book_list_Third": booksThird, "book_Best": booksBest, "book_Fiction": bookFiction[:7], "book_Westerns": bookWesterns, 'cart': cart})
    else:
        return render(request, "bookShop/Main.html",
                      {"book_list_First": booksFirst, "book_list_Second": booksSecond, "book_list_Third": booksThird,
                       "book_Best": booksBest, "book_Fiction": bookFiction[:7], "book_Westerns": bookWesterns,
                       })

class GenreBindMoney:
    """Жанры и года выхода фильмов"""
    def get_binding(self):
        return Book.objects.values('binding').distinct()

    def get_genres(self):
        return Genre.objects.all()

    def get_money(self):
        return Book.objects.all()


class BaseView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        products = Book.objects.all()
        context = {
            'products': products,
            'cart': cart
        }

        return render(request, 'Main.html', context)



class BooksView(GenreBindMoney, ListView):
    """Список books"""
    model = Book
    queryset = Book.objects.all()



class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        books = Book.objects.all()
        context = {'form': form, 'books': books, 'cart': self.cart}
        return render(request, 'Login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'Login.html', {'form': form, 'cart': self.cart})


def logout_view(request):
    form = LoginForm(request.POST or None)
    logout(request)
    return HttpResponseRedirect('/')



class RegistrationView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        books = Book.objects.all()
        context = {'form': form, 'books': books, 'cart': self.cart}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            customer = Customer(email=form.cleaned_data['email'], user=new_user)
            cart = Cart.objects.filter(owner=customer).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
            customer.save()
            # Customer.objects.create(
            #     user=new_user
            # )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'registration.html', context)

class BookDetails(View):
    def get(self, request, slug):
        print(slug)
        book = Book.objects.get(url=slug)
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(owner=customer)
            return render(request, "bookShop/book_detail.html", {"book": book, "cart": cart})
        else:
            return render(request, "bookShop/book_detail.html", {"book": book})
    # def dispatch(self, request, *args, **kwargs):
    #     # self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
    #     self.queryset = self.model._base_manager.all()
    #     return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'book_detail.html'
    slug_url_kwargs = 'slug'


class StoresView(View):
    def get(self, request):
        genre = Genre.objects.all()
        bookBinding = Book.objects.values("binding").distinct()
        bookPrice = Book.objects.values("money").distinct()
        book = Book.objects.all()

        paginator = Paginator(book, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(owner=customer)
            return render(request, "bookShop/Stores.html", {'page_obj': page_obj, "genres": genre, "booksBinding": bookBinding, "bookPrice": bookPrice, "books": book, 'cart': cart})
        else:
            return render(request, "bookShop/Stores.html",
                          {'page_obj': page_obj, "genres": genre, "booksBinding": bookBinding, "bookPrice": bookPrice,
                           "books": book})
class NewView(View):
    def get(self, request):
        genre = Genre.objects.all()
        bookBinding = Book.objects.values("binding").distinct()
        bookPrice = Book.objects.values("money").distinct()
        book = Book.objects.all()

        booksFirst = Book.objects.order_by('-date')[:7]
        booksSecond = Book.objects.order_by('-date')[7:14]
        booksThird = Book.objects.order_by('-date')[14:21]
        booksBest = Book.objects.filter(category=3).order_by('-stock')[:7]
        bookWesterns = Book.objects.filter(category=18).order_by('-stock')[:7]
        bookFiction = Book.objects.filter(category=6).order_by('-stock') | Book.objects.filter(category=21).order_by(
            '-stock') | Book.objects.filter(category=24).order_by('-stock')


        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(owner=customer)
            return render(request, "new.html",
                      {"book_list_First": booksFirst, "book_list_Second": booksSecond, "book_list_Third": booksThird,
                       "book_Best": booksBest, "book_Fiction": bookFiction[:7], "genres": genre, "booksBinding": bookBinding, "bookPrice": bookPrice, "books": book, "book_Westerns": bookWesterns,
                       'cart': cart})
        else:
            return render(request, "new.html",
                          {"book_list_First": booksFirst, "book_list_Second": booksSecond,
                           "book_list_Third": booksThird,
                           "book_Best": booksBest, "book_Fiction": bookFiction[:7], "genres": genre,
                           "booksBinding": bookBinding, "bookPrice": bookPrice, "books": book,
                           "book_Westerns": bookWesterns})

class BestsellerView(View):
    def get(self, request):
        genre = Genre.objects.all()
        bookBinding = Book.objects.values("binding").distinct()
        bookPrice = Book.objects.values("money").distinct()
        book = Book.objects.all()


        booksFirst = Book.objects.order_by('-date')[:7]
        booksSecond = Book.objects.order_by('-date')[7:14]
        booksThird = Book.objects.order_by('-date')[14:21]
        booksBest = Book.objects.filter(category=3).order_by('-stock')[:7]
        bookWesterns = Book.objects.filter(category=18).order_by('-stock')[:7]
        bookFiction = Book.objects.filter(category=6).order_by('-stock') | Book.objects.filter(category=21).order_by(
            '-stock') | Book.objects.filter(category=24).order_by('-stock')


        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(owner=customer)
            return render(request, "bestseller.html",
                      {"book_list_First": booksFirst, "book_list_Second": booksSecond, "book_list_Third": booksThird,
                       "book_Best": booksBest, "book_Fiction": bookFiction[:7], "genres": genre, "booksBinding": bookBinding, "bookPrice": bookPrice, "books": book, "book_Westerns": bookWesterns,
                       'cart': cart})
        else:
            return render(request, "bestseller.html",
                          {"book_list_First": booksFirst, "book_list_Second": booksSecond,
                           "book_list_Third": booksThird,
                           "book_Best": booksBest, "book_Fiction": bookFiction[:7], "genres": genre,
                           "booksBinding": bookBinding, "bookPrice": bookPrice, "books": book,
                           "book_Westerns": bookWesterns,
                            })

class CartView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(owner=customer)
            context = {
                'cart': cart,
            }
            return render(request, 'cart.html', context)
        else:
            return render(request, 'Login.html', {'form': form})

class AddToCartView(View):

    def get(self, request,  *args, **kwargs):
        form = LoginForm(request.POST or None)
        product_slug = kwargs.get('slug')
        if request.user.is_authenticated:
            print(kwargs.get('slug'))
            customer = Customer.objects.get(user=request.user.id)
            if len(Cart.objects.filter(owner=customer)) == 0:
                Cart(owner=customer).save()
            cart = Cart.objects.get(owner=customer)
            product = Book.objects.get(id=product_slug)
            amount = 1
            existence = False
            for book_in_cart in cart.products.all():
                if book_in_cart.book.id == product.id:
                    book_in_cart.amount += amount
                    book_in_cart.total_price.amount += product.money.amount
                    cart.total_price += product.money.amount
                    book_in_cart.save()
                    existence = True
                    break
            if not existence:
                cartProduct = CartProduct(book=product, amount=amount, total_price=product.money.amount * amount)
                cartProduct.save()
                cart.products.add(cartProduct)
                cart.total_products += 1
                cart.total_price += product.money.amount
                cart.save()
            cart.total_amount_of_products += amount
            cart.save()
            # cart_product, created = CartProduct.objects.get_or_create(
            #     user=cart.owner, cart=cart, image=product.image, money=product.money, object_id=product.id, title=product.name)
            # if created:
            return HttpResponseRedirect('/cart/')
        else:
            return render(request, 'Login.html', {'form': form})


def deleteElementFromCart(request):
    item_id = request.GET['item_id']
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=request.user.id)
    cart = Cart.objects.get(owner=customer)
    cartProduct = CartProduct.objects.get(id=item_id)

    if cartProduct.amount == 1:
        product = Book.objects.filter(name=cartProduct.book)[0]
        cart.total_price -= product.money.amount

        cartProduct.delete()
    else:
        product = Book.objects.filter(name=cartProduct.book)[0]
        print(product)
        cart.total_price -= product.money.amount
        cartProduct.amount -= 1
        cartProduct.total_price -= product.money
        cartProduct.save()
    # cart.total_products -= 1  #!!!!!!!!!!
    cart.total_amount_of_products -= 1

    cart.save()
    return redirect("cart")


def cleanCart(request):
    customer = Customer.objects.get(user=request.user.id)
    cart = Cart.objects.get(owner=customer)
    cartProduct = CartProduct.objects.all()
    cart.total_price = 0
    cart.total_amount_of_products = 0
    # cart.total_products = 0  #!!!!!!!!!!!!!!
    cartProduct.delete()
    cart.save()

    return redirect("cart")


def get_queryset(request):

   queryset = Book.objects.filter()

   if 'binding' in request.GET:
        queryset = queryset.filter(
            binding=request.GET['binding']
        )

   if 'genre' in request.GET:
        queryset = queryset.filter(
            genres__id=request.GET['genre']
        )


   if 'price' in request.GET:

       if request.GET.get("price") == '<5':
           queryset = queryset.filter(money__range=[0, 5])

       if request.GET.get("price") == '5-10':
           queryset = queryset.filter(money__range=(5, 10))

       if request.GET.get("price") == '10-20':
           queryset = queryset.filter(money__range=(10, 20))

       if request.GET.get("price") == '20-50':
           queryset = queryset.filter(money__range=(20, 50))

       if request.GET.get("price") == '50>':
           queryset = queryset.filter(money__range=(50, 100))


   if 'sort' in request.GET:
       if request.GET.get("sort") == 'p-':
           queryset = queryset.order_by('-money')

       if request.GET.get("sort") == 'p+':
           queryset = queryset.order_by('money')

       if request.GET.get("sort") == 'd+':
           queryset = queryset.order_by('date')

       if request.GET.get("sort") == 'd-':
           queryset = queryset.order_by('-date')

   if request.user.is_authenticated:
       customer = Customer.objects.get(user=request.user)
       cart = Cart.objects.get(owner=customer)
       context = {"cart": cart, "book_list": queryset, "genres": Genre.objects.all(), "bindings": Book.objects.order_by().values("binding").distinct()}
       return render(request, 'bookShop/book_list.html', context)
   else:
       context = {"book_list": queryset, "genres": Genre.objects.all(),
                  "bindings": Book.objects.order_by().values("binding").distinct()}
       return render(request, 'bookShop/book_list.html', context)


class FilterPriceBooksView(GenreBindMoney, ListView):
    paginate_by = 15
    model = Book
#     def get_queryset(self):
#
#         # if filter_queryset(request) is not None:
#         #     if self.request.GET.get("price") == '<5':
#         #         queryset = filter_queryset(request).filter(money__range=(0, 5))
#         #
#         #     if self.request.GET.get("price") == '5-10':
#         #         queryset = filter_queryset(request).filter(money__range=(5, 10))
#         #
#         #     if self.request.GET.get("price") == '10-20':
#         #         queryset = filter_queryset(request).filter(money__range=(10, 20))
#         #
#         #     if self.request.GET.get("price") == '20-50':
#         #         queryset = filter_queryset(request).filter(money__range=(20, 50))
#         #
#         #     if self.request.GET.get("price") == '50>':
#         #         queryset = filter_queryset(request).filter(money__range=(50, 100))
#         #
#         #
#         # else:
#         if self.request.GET.get("price") == '<5':
#             queryset = Book.objects.filter(money__range=(0, 5))
#
#         if self.request.GET.get("price") == '5-10':
#             queryset = Book.objects.filter(money__range=(5, 10))
#
#         if self.request.GET.get("price") == '10-20':
#             queryset = Book.objects.filter(money__range=(10, 20))
#
#         if self.request.GET.get("price") == '20-50':
#             queryset = Book.objects.filter(money__range=(20, 50))
#
#         if self.request.GET.get("price") == '50>':
#             queryset = Book.objects.filter(money__range=(50, 100))
#
#         print(queryset)
#         return queryset


class Search(ListView):
    paginate_by = 4
    model = Book

    def get_queryset(self):
        return Book.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, object_list=None, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context = {"genres": Genre.objects.all(),
                   "bindings": Book.objects.order_by().values("binding").distinct(), "q": self.request.GET.get("q"), "book_list": Book.objects.filter(name__icontains=self.request.GET.get("q"))}
        context["q"] = self.request.GET.get("q")
        return context


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        stripe.api_key='sk_test_51K4LpALs9GVApt96BOdY8Uvb4LaZeio7oEyG0asTYNKHd7OyyxqLy7gaKddJphRjCRQp8Sgas6ugq4bR3GzlfitV00ERkdyDvB'
        intent = stripe.PaymentIntent.create(
            amount=int(self.cart.total_price * 100),
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )

        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form,
            'client_secret': intent.client_secret
        }
        return render(request, 'checkout.html', context)


class PayedOnlineOrderView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        print("PAYINGG")
        customer = Customer.objects.get(user=request.user)
        new_order = Order()
        new_order.customer = customer
        new_order.first_name = customer.user.first_name
        new_order.last_name = customer.user.last_name
        new_order.phone = customer.phone
        new_order.address = customer.address
        new_order.buying_type = Order.BUYING_TYPE_SELF
        new_order.save()
        self.cart.save()
        new_order.cart = self.cart
        new_order.status = Order.STATUS_PAYED
        new_order.save()
        customer.orders.add(new_order)
        return JsonResponse({"status": "payed"})


def adminView(request):
    context = {}
    if (not request.user.is_staff):
        context['msg'] = "You have no rights to access this resource!"
    else:
        context['users'] = User.objects.all()
        context['books'] = Book.objects.all()
    return render(request, 'bookShop/admin.html', context)

def aboutView(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        context = {"cart": cart}
    else:
        context = {}
    return render(request, 'about.html', context)