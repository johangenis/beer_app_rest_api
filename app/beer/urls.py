from django.urls import path, include
from rest_framework.routers import DefaultRouter

from beer import views


router = DefaultRouter()
router.register("tags", views.TagViewSet)

app_name = "beer"

urlpatterns = [
    path("", include(router.urls)),
    path("api/beer/", include("beer.urls")),
]
