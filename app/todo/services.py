import uuid

from django.http import QueryDict
from rest_framework import status, viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response


def get_or_create_cookie(request) -> str:
    if not request.COOKIES.get("uid"):
        return str(uuid.uuid4())
    return request.COOKIES.get("uid")


# QueryDictはimmutableなので、dictに変換してから追加して再度QueryDictに変換する
def add_uid_to_data(data: QueryDict, cookie: str) -> QueryDict:
    dict = data.dict()
    uid = cookie
    dict["uid"] = uid
    data = QueryDict("", mutable=True)
    data.update(dict)
    return data


# レスポンスのボディとステータスコードを仕様に合わせた汎用ビュー群
# 作成時とリスト取得時にはクッキーにuidをセットする
class BaseCreateAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        cookie = get_or_create_cookie(request)
        data = add_uid_to_data(request.data, cookie)
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)
        response.set_cookie("uid", cookie)
        return response


class BaseUpdateAPIView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        cookie = get_or_create_cookie(request)
        if not instance.uid == cookie:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = add_uid_to_data(request.data, cookie)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if not serializer.is_valid():
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseDestroyAPIView(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.uid == get_or_create_cookie(request):
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        cookie = get_or_create_cookie(request)
        queryset = self.filter_queryset(self.get_queryset()).filter(uid=cookie)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        response.set_cookie("uid", cookie)
        return response


class BaseRetrieveAPIView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.uid == get_or_create_cookie(request):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BaseTodoViewSet(
    BaseCreateAPIView,
    BaseUpdateAPIView,
    BaseDestroyAPIView,
    BaseListAPIView,
    BaseRetrieveAPIView,
    viewsets.GenericViewSet,
):
    pass
