"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todo import views

router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'user')
router.register(r'apartments', views.ApartmentView, 'apartment')
router.register(r'reviews', views.ReviewView, 'review')
router.register(r'subleases', views.ApartmentSubleaseView, 'sublease')
router.register(r'universities', views.UniversityView, 'university')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/post_review', views.post_review),
    path('api/sign_in',views.sign_in),
    path('api/sign_up',views.sign_up),
    path('api/get_nearest_apartments', views.get_nearest_apartments),
    path('api/get_university_apartments', views.get_university_apartments),
    path('api/add_apartments', views.add_apartments),
    path('api/get_apartment_reviews', views.get_apartment_reviews),
    path('api/like_review', views.like_review),
    path('api/dislike_review', views.dislike_review),
    path('api/post_sublease', views.post_sublease),
    path('api/get_apartment_subleases', views.get_apartment_subleases),
    path('api/get_university_data', views.get_university_data),
    path('api/email_tenant',views.email_tenant)
]
