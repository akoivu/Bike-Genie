from rest_framework import routers

from web.api_views import StationViewSet

router = routers.DefaultRouter()
router.register(r"stations", StationViewSet)

urlpatterns = router.urls