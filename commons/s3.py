import json

import time

import boto3

from botocore.exceptions import ClientError, NoCredentialsError

from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage

AWS_ACCESS_KEY_ID = getattr(settings, "AWS_ACCESS_KEY_ID", "")

AWS_SECRET_ACCESS_KEY = getattr(settings, "AWS_SECRET_ACCESS_KEY", "")

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:

    AWS_CREDS = dict(
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

else:

    AWS_CREDS = {}

BUCKET_NAME = settings.S3_BUCKET_NAME


def get_s3_client():
    return boto3.client("s3", **AWS_CREDS)


def get_s3_resource():
    return boto3.resource("s3", **AWS_CREDS)


def move_s3_object(source, destination):
    # currently used at:

    # levelup.contents.api.v1.views.content.ContentViewSet.re_process_media

    get_s3_resource().Object(BUCKET_NAME, destination).copy(
        CopySource={"Bucket": BUCKET_NAME, "Key": source}
    )

    get_s3_resource().Object(BUCKET_NAME, source).delete()


# todo: Dipesh make bucket name dynamic constants through settings


def create_presigned_post(
    object_name, bucket_name=BUCKET_NAME, fields=None, conditions=None, expiration=3600
):
    s3_client = get_s3_client()

    try:

        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )

    except (ClientError, NoCredentialsError) as _e:

        return None

    # The response contains the presigned URL and required fields

    return response


# todo: Dipesh make bucket name dynamic constants through settings


def create_presigned_get(object_name, bucket_name=BUCKET_NAME, expiration=3600):
    s3_client = get_s3_client()

    try:

        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

    except (ClientError, NoCredentialsError) as _e:

        response = None

    return response


# TODO: Nabin, Created temporarily until the two S3 buckets are resolved to one. (levelup-video-upload-demo and

#  temp-work-bucket)


def create_presigned_get_temp(object_name, bucket_name=BUCKET_NAME, expiration=3600):
    s3_client = get_s3_client()

    bucket_name = "levelupstage"

    try:

        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

    except (ClientError, NoCredentialsError) as _e:

        response = None

    return response


def check_object_exists(object_name, bucket_name=BUCKET_NAME):
    s3_client = get_s3_client()

    try:

        s3_client.head_object(Bucket=bucket_name, Key=object_name)

    except ClientError:

        return False

    else:

        return True


class StaticStorage(S3Boto3Storage):
    location = "static-files"

    default_acl = "public-read"  # since private is default in this project, need to define this is public


# currently haven't been used in project, kept for future

# class PublicMediaStorage(S3Boto3Storage):

#     location = 'media-public'

#     default_acl = 'public-read'  # since private is default in this project, need to define this is public

#     file_overwrite = False


# basically this is the default


class PrivateMediaStorage(S3Boto3Storage):
    location = "media-private"

    default_acl = (
        "private"  # no need to define private, but to overcome future mistakes keep it
    )

    file_overwrite = False

    custom_domain = False


def get_duration(bucket_name, content_media):
    s3_object = get_s3_resource().Object(
        bucket_name,
        f"contents/{content_media.content.category.lower()}/"
        f"{content_media.identifier}/meta.json",
    )

    try:

        data = s3_object.get()

        json_text = json.load(data["Body"])

        duration_seconds = json_text["format"]["duration"]

        duration_text = time.strftime("%H:%M:%S", time.gmtime(float(duration_seconds)))

        return duration_seconds, duration_text

    except Exception:
        return None, None
