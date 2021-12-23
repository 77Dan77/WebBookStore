from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Cart)
admin.site.register(Customer)


