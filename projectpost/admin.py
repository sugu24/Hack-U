from django.contrib import admin

# Register your models here.
from .models import ThreadModel, PostDataModel

admin.site.register(PostDataModel)
admin.site.register(ThreadModel)