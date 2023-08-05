from django.db.models import F

from .models import Todo
from .serializers import TodoSerializer
from .services import BaseTodoViewSet


class TodoViewSet(BaseTodoViewSet):
    queryset = Todo.objects.all().order_by(
        F("deadline").asc(nulls_last=True)
    )  # 期限が近い順に並べる(nullは最後にする)
    serializer_class = TodoSerializer
