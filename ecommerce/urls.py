
from django.contrib import admin
from django.urls import path ,include,re_path
from django.views.generic import  TemplateView
#from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('store.urls')),
    path('admin/', admin.site.urls)

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

