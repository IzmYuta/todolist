from rest_framework import routers

from .views import TodoViewSet

router = routers.SimpleRouter()
router.register("todo", TodoViewSet)

app_name = "todo"
urlpatterns = router.urls
