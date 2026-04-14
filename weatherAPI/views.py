from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    def get(self, request):
        return Response(
            {
                "message": "Welcome to Weather API",
                "endpoints": ["/monthly", "/seasonal", "/annual"],
            }
        )
