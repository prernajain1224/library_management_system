from django.contrib import admin
from .models import Profile,Book,IssuedBook

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(IssuedBook)
