from django.db import connections
from django.db.utils import OperationalError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        db_ok = True
        try:
            connections["default"].cursor()
        except OperationalError:
            db_ok = False

        data = {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
        }
        status_code = 200 if db_ok else 503
        return Response(data, status=status_code)
