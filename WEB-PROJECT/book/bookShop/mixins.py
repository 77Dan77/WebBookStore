from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from .models import Customer, Cart
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            # if not customer:
                # customer = Customer.objects.create(
                #     user=request.user
                #
                # )
            cart = Cart.objects.filter(owner=customer).first()  #in_order=False

            if not cart:
                cart = Cart.objects.create(owner=customer)


        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)