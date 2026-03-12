from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, DealerViewSet, OrderViewSet

router = DefaultRouter()

router.register("products", ProductViewSet)
router.register("dealers", DealerViewSet)
router.register("orders", OrderViewSet)

urlpatterns = router.urls