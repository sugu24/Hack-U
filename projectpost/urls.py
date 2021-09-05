from django.contrib import admin
from django.urls import path
from .views import BulletinBoardView, SelectThreadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('selectThread/', SelectThreadView, name='selectThread'),
    path('bulletinBoard/<int:pk>', BulletinBoardView, name='bulletinBoard'),
]