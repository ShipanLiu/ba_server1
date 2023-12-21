from django.urls import path, include
# from package drf-nested-routers for building nested router
from rest_framework_nested import routers

from . import views

# initialize the router, create a router instance
router = routers.DefaultRouter()

# register "customer/" endpoints
router.register("customers", views.CustomerViewSet, basename="customers")
# "ais/"
router.register("ais", views.AIsViewSet, basename="ais")
# "projects/"
router.register("projects", views.ProjectsViewSet, basename="projects")
# "images"
router.register("images", views.ImagesViewSet, basename="images")

# for rested router: /projects/project_id/results/
projects_router = routers.NestedDefaultRouter(router, "projects", lookup="project") # lookup "project" ---changes--->  project_pk
# projects_router.register("upload-images", views.ResultsViewSet, basename="upload-images") #the drf will create for us 2 route based on the basename: "result-sets-datail", "result-sets-list"
projects_router.register("results", views.ResultsViewSet, basename="result-sets")



urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(projects_router.urls)),
]

"""
admin/
auth/
auth/
store/ ^customers/$ [name='customers-list']
store/ ^customers\.(?P<format>[a-z0-9]+)/?$ [name='customers-list']
store/ ^customers/me/$ [name='customers-me']
store/ ^customers/me\.(?P<format>[a-z0-9]+)/?$ [name='customers-me']
store/ ^customers/(?P<pk>[^/.]+)/$ [name='customers-detail']
store/ ^customers/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='customers-detail']


store/ ^ais\.(?P<format>[a-z0-9]+)/?$ [name='ais-list']
store/ ^ais/(?P<pk>[^/.]+)/$ [name='ais-detail']
store/ ^ais/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='ais-detail']


store/ ^projects/$ [name='projects-list']
store/ ^projects\.(?P<format>[a-z0-9]+)/?$ [name='projects-list']
store/ ^projects/(?P<pk>[^/.]+)/$ [name='projects-detail']
store/ ^projects/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='projects-detail']


store/ ^images/$ [name='images-list']
store/ ^images\.(?P<format>[a-z0-9]+)/?$ [name='images-list']
store/ ^images/(?P<pk>[^/.]+)/$ [name='images-detail']
store/ ^images/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='images-detail']

store/ ^$ [name='api-root']
store/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']

store/ ^projects/(?P<project_pk>[^/.]+)/results/$ [name='result-sets-list']
store/ ^projects/(?P<project_pk>[^/.]+)/results\.(?P<format>[a-z0-9]+)/?$ [name='result-sets-list']
store/ ^projects/(?P<project_pk>[^/.]+)/results/(?P<pk>[^/.]+)/$ [name='result-sets-detail']
store/ ^projects/(?P<project_pk>[^/.]+)/results/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='result-sets-detail']

store/ ^$ [name='api-root']
store/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']


"""