from django.urls import path,include
from .views import JobView,JobSearch
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("",JobView)

urlpatterns = [
    path('jobs/',include(router.urls)),
    path('job/search/',JobSearch.as_view(),name='search'),
    
]
