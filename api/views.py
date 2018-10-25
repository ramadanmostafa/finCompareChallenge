from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.utils import save_data
from .serializers import BulkUploadCsvSerializer


class BulkUploadCsvView(APIView):
    permission_classes = (AllowAny, )
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        """
        accepts a csv file
        :param request:
        :return:
        """
        serializer = BulkUploadCsvSerializer(data=request.data)
        if serializer.is_valid():
            save_data(serializer.validated_data['file'])
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
