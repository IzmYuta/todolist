from rest_framework.response import Response
from rest_framework.views import exception_handler


# 例外のレスポンスのBodyを空にする
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response = Response(status=response.status_code, headers=response.headers)

    return response
