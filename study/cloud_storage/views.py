from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import boto3
from botocore.exceptions import ClientError
import re

from study.utils.recursive_default_dict import RecursiveDefaultDict


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
        groupId = request.data['groupId']
        try:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
            global_file_paths = map(lambda content: content['Key'], response['Contents'])
            file_paths = self.file_paths_to_tree(global_file_paths, groupId)
            file_tree = self.file_paths_to_tree(file_paths)
            return Response({'file_tree': file_tree})
        except ClientError as e:
            return Response({'error': e})

    def global_file_paths_to_group_file_paths(self, global_file_paths, groupId):
        group_file_paths = filter(
            lambda global_file_path: re.match(r'^{}/'.format(groupId), global_file_path),
            global_file_paths)
        file_paths = map(
            lambda file_path: re.sub(r'^{}/'.format(groupId), '', file_path),
            group_file_paths)
        return file_paths

    def file_paths_to_tree(self, file_paths):
        recursive_default_dict = RecursiveDefaultDict()
        for file_path in file_paths:
            file_path_split = file_path.split('/')
            if not file_path_split[-1]:
                file_path_split = file_path_split[:-1]
            directory_names = file_path_split[:-1]
            file_name = file_path_split[-1]
            recursive_default_dict[directory_names] = file_name
        return recursive_default_dict.to_dict()
