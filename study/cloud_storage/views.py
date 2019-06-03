from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import boto3
from botocore.exceptions import ClientError
import re

from study.utils.file_tree_generator import FileTreeGenerator


s3_client = boto3.client('s3')
BUCKET_NAME = 'letsstudy-test'


class CloudStorageFileDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        groupId = request.data['groupId']
        file_path_in_group = request.data['filepath']
        file_path = '{}/{}'.format(groupId, file_path_in_group)
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


class CloudStorageFileCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        groupId = request.data['groupId']
        file_path_in_group = request.data['filepath']
        file_path = '{}/{}'.format(groupId, file_path_in_group)
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


class CloudStorageFileTree(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        groupId = self.request.query_params.get('groupId')
        try:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
            global_file_paths = map(lambda content: content['Key'], response['Contents'])
            file_paths = self.filter_group_file_paths(global_file_paths, groupId)
            file_tree = FileTreeGenerator().put_all(file_paths).tree
            return Response(file_tree)
        except ClientError as e:
            return Response({'error': e})

    def filter_group_file_paths(self, global_file_paths, groupId):
        group_file_paths = filter(
            lambda global_file_path: re.match(r'^{}/'.format(groupId), global_file_path),
            global_file_paths)
        file_paths = map(
            lambda file_path: re.sub(r'^{}/'.format(groupId), '', file_path),
            group_file_paths)
        return file_paths
