from django.urls import path, include
from rest_framework.routers import DefaultRouter

from beer import views


router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register("beers", views.BeerViewSet)
router.register("reviews", views.ReviewViewSet)

app_name = "beer"

urlpatterns = [path("", include(router.urls))]
