from django.conf.urls import include
from django.urls import path

#from blogging import views
from .views import BlogView, BlogViewById


urlpatterns = [
    
    path('v1/blogs/', BlogView.as_view()),
    path('v1/blogs/<int:id>', BlogViewById.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
