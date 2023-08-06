import logging

import boto3
import environ
from botocore.config import Config
from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage

LOGGER = logging.getLogger('django')


class ERPStorage(S3Boto3Storage):

    def signed_url(self, key):
        if self.location:
            key = f'{self.location.rstrip("/")}/{key}'
        s3_client = boto3.client('s3', config=Config(signature_version='s3v4', region_name='ca-central-1'))
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={
                                                            'Bucket': self.bucket_name,
                                                            'Key': key,
                                                        }, ExpiresIn=9000)
        except ClientError as e:
            LOGGER.error(e)
            return None
        return response


class MediaStorage(ERPStorage):
    env = environ.Env()
    bucket_name = env.str('S3_SHARED_BUCKET')  # 'tfg-shared'
    location = 'jobs/'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'
    default_acl = None


class ResourcesStorage(ERPStorage):
    env = environ.Env()
    bucket_name = env.str('RESOURCES_BUCKET')  # 'tfg-shared'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'
    default_acl = None


class GeneratedStorage(ERPStorage):
    env = environ.Env()
    bucket_name = env.str('GENERATED_BUCKET')  # 'tfg-shared'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'
    default_acl = None


class StaticStorage(ERPStorage):
    env = environ.Env()
    if not env.bool('AWS_LAMBDA', default=False):
        environ.Env.read_env()  # reading .env file
    bucket_name = env.str('S3_BUCKET')
    project_name = env.str('AWS_LAMBDA_FUNCTION_NAME')
    location = f'static/{project_name}'
    AWS_DEFAULT_ACL = None
