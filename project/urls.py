from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # for "djoser", using for token
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # for store app
    path('store/', include('store.urls')),
]

# only for developing process
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
all endpoints here:


# create/update users
http://127.0.0.1:8001/auth/users/


# create/update a customer(assocated to user)
http://127.0.0.1:8001/store/customers/


# [for Frontned]user login(get a response of "acccess-token" back)
http://127.0.0.1:8001/auth/jwt/create


# [for Frontend]: if the access-token is expired, then client has to send 
    "refresh-token" to server to get a new valide "access-token" for login


# after successfully logined in, you want to retrieve the profile(in the header add the JWT header)
# http://127.0.0.1:8001/auth/users/me/    with header {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMTU2MjQwLCJpYXQiOjE3MDMwNjk4NDAsImp0aSI6IjNkMzBiZmI1YTE5ZDRmNWQ4NzhhNGE1Y2UwYzVmMWQxIiwidXNlcl9pZCI6MX0.VyVLGg_jriYRdHw6y3q7c-L-Bh7p_aqUOOnhRgukThY"}


# I want to get the profile page
# http://127.0.0.1:8000/store/customers/me/ -> need to define sLizer + ViewSet





"""