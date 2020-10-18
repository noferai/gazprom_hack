from rest_framework.views import APIView
from tdmt.tenders.models import Transaction


class HighchartLine(APIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get("client_id")
        mcc = kwargs.get("mcc")
