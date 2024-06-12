from django.contrib import admin
from django.urls import path
from .views import dashboard, data_page, perhitungan
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', dashboard, name="dashboard") ,
    path('data/', data_page ),
    path('perhitungan/', perhitungan ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
