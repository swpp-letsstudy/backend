from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')
BUCKET_NAME = 'letsstudy-test'


class CloudFileDetail(APIView):

    def post(self, request, format=None):
        file_path = request.data['filepath']
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': file_path,
                },
                ExpiresIn=3600)
            return Response({'url': url}, status=status.HTTP_200_OK)
        except ClientError as e:
            return Response({'error': e}, status.HTTP_204_NO_CONTENT)


class CloudFileCreate(APIView):

    def post(self, request, format=None):
        file_path = request.data['filepath']
        try:
            url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': file_path,
                },
                ExpiresIn=3600)
            return Response({'url': url}, status=status.HTTP_200_OK)
        except ClientError as e:
            return Response({'error': e})
