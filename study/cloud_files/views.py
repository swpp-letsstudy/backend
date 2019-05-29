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


class CloudFileTree(APIView):

    def get(self, request, format=None):

        try:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
            file_tree = response['file_tree']['Contents']
            return Response({'file_tree': file_tree})
        except ClientError as e:
            return Response({'error': e})
