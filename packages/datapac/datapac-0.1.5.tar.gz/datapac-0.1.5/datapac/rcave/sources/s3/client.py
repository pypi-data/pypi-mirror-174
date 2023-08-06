import os
from contextlib import contextmanager

import boto3

from datapac.config import S3Config


@contextmanager
def connect(config: S3Config):
    yield boto3.client(
        "s3",
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
    )


def download(client, bucket: str, key: str, path: str):
    # ensure depth
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(f"{path}", "wb") as f:
        client.download_fileobj(bucket, key, f)


def upload(client, bucket: str, key: str, path: str):
    with open(path, "rb") as f:
        client.upload_fileobj(f, bucket, key)
