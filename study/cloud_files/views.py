from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import boto3
from botocore.exceptions import ClientError

from study.utils.recursive_default_dict import RecursiveDefaultDict


s3_client = boto3.client('s3')
BUCKET_NAME = 'letsstudy-test'


class CloudFileDetail(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
            file_paths = map(lambda content: content['Key'], response['Contents'])

            recursive_default_dict = RecursiveDefaultDict()
            for file_path in file_paths:
                file_path_split = file_path.split('/')
                if not file_path_split[-1]:
                    file_path_split = file_path_split[:-1]
                directory_names = file_path_split[:-1]
                file_name = file_path_split[-1]
                recursive_default_dict[directory_names] = file_name

            return Response({'file_tree': recursive_default_dict.to_dict()})
        except ClientError as e:
            return Response({'error': e})
