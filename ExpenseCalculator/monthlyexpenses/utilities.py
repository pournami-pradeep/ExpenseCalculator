from rest_framework import status
from rest_framework.response import Response

from monthlyexpenses.Custommessages import Custommessage


def success(msg, response):
    return Response(
        {
            "status": True,
            "msg": msg,
            "response": response,
        },
        status=status.HTTP_200_OK,
    )


def serializer_error(serializer):
    msg_ob = Custommessage()
    return Response(
        {"status": False, "msg": msg_ob.form_error, "response": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )
