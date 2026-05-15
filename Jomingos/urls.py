from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('tasks/', include('tasks.urls')),
    path('care-notes/', include('care_notes.urls')),
    path('medications/', include('medications.urls')),
    path('vitals/', include('vitals.urls')),
    path('family/', include('family.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
