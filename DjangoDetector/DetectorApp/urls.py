from django.urls import path
from .views import pic_load_page_view

urlpatterns = [
    path('pic_load_page_view/', pic_load_page_view, name="files")
]
