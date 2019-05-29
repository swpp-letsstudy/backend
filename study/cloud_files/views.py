from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from botocore.exceptions import ClientError


class CloudFileDetail(APIView):

    def post(self, request, format=None):
        file_path = request.data['filepath']
        s3_client = boto3.client('s3')
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': 'letsstudy-test',
                    'Key': file_path,
                },
                ExpiresIn=3600)
            return Response({'url': url}, status=status.HTTP_200_OK)
        except ClientError as e:
            Response({'error': e}, status.HTTP_204_NO_CONTENT)

