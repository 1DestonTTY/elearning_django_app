"""
URL configuration for elearning_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

#api
from rest_framework.routers import DefaultRouter
from accounts.api import UserViewSet

#swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'users', UserViewSet)

#swagger configure
schema_view = get_schema_view(
    openapi.Info(
        title="AWD E-Learning API",
        default_version='v1',
        description="API documentation for the E-Learning application.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), #allow anyone to view 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #registration
    path('register/', account_views.register, name='register'),
    
    #login logout 
    path('login/', auth_views.LoginView.as_view(template_name='accounts/loginpage.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    #base url
    path('', account_views.home, name='home'),

    #go to courses
    path('courses/', include('courses.urls')),
    
    #teacher search page
    path('directory/', account_views.user_search, name='user_search'),

    #chat
    path('chat_app/', include('chat.urls')),

    #api documentation
    path('api/', include(router.urls)),

    #swagger ui page documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

#serve uploaded photos during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)