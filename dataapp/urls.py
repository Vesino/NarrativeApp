from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Django rest_framework
from rest_framework.routers import DefaultRouter

# Views
from app import views
from app.views import AssetViewSet as asset_views

router = DefaultRouter()
router.register(r'assets', asset_views, basename='asstes')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('listfiles/', views.list_files, name='listfiles'),
    path('datavisual/', views.data_visualization, name='datavisual'),
    path('', include(router.urls))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)