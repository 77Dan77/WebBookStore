from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import *

from . import api


api_urlpatterns = [
    path("api/updateBalance", api.updateBalance),
    path("api/deleteUser", api.deleteUser),
    path("api/getUserById", api.getUserDataById),
    path("api/updateUser", api.updateUser),
    path("api/createUser", api.createUser),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customadmin/', views.adminView),
    path('', views.get, name='Main'),
    path('about/', views.aboutView, name='about'),
    # path('', views.BaseView.as_view(), name='Main'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("logout/", views.logout_view, name="logout"),
    path('Login/', LoginView.as_view(), name='login'),
    path('filter/', views.get_queryset, name='filter'),
    path('filters/', views.FilterPriceBooksView.as_view(), name='filterPrice'),
    path('deleteElementFromCart/', views.deleteElementFromCart),
    path('paying/', views.cleanCart, name='paying'),
    path('Stores/', StoresView.as_view(), name='stores'),
    path('search/', views.Search.as_view(), name='search'),
    path('bestseller/', views.BestsellerView.as_view(), name='bestseller'),
    path('new/', views.NewView.as_view(), name='new'),
    path('cart/', CartView.as_view(), name='cart'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(), name='make_order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name="add_to_cart"),
    path('<slug:slug>/', views.BookDetails.as_view(), name="book_detail"),

]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
