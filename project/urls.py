from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # for "djoser", using for token
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # for store app
    path('store/', include('store.urls')),
]
