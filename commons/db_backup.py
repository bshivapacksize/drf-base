import gzip
import os
import subprocess
import datetime
import urllib.parse

import boto3
from django.conf import settings

from drf_base.settings import DATABASES, ROOT_DIR


def config(param):
    val = DATABASES["default"].get(param.split("_")[1])
    return urllib.parse.quote(val)


DB_USER = config("DB_USER")
DB_NAME = config("DB_NAME")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DESTINATION_FILE = (
    f"backup {datetime.datetime.now()}.gz" """Ocean- check for timezone"""
)

BASE_LOCATION = os.path.join(ROOT_DIR, "backups")

CMD = ["pg_dump", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"]


def upload_file_to_s3():
    s3 = boto3.resource("s3")
    file_to_upload = os.path.join(BASE_LOCATION, DESTINATION_FILE)
    bucket_name = getattr(settings, "DB_BACKUP_BUCKET", None)
    if bucket_name:
        s3.meta.client.upload_file(
            file_to_upload, bucket_name, f"db-backups/levelup/{DESTINATION_FILE}"
        )


def db_backup():
    if not os.path.exists(BASE_LOCATION):
        os.mkdir(BASE_LOCATION)

    print(f"Performing backup from {DB_USER} on {DB_HOST}")
    print(f"Backup location:{BASE_LOCATION}")
    print(f"Backing up {DB_NAME} in : {DESTINATION_FILE}")
    with gzip.open(os.path.join(BASE_LOCATION, DESTINATION_FILE), "wb") as f:
        ps = subprocess.Popen(CMD, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(ps.stdout.readline, ""):
            f.write(stdout_line.encode("utf - 8"))

        ps.stdout.close()
        ps.wait()
    upload_file_to_s3()
    print("Backup Completed ")

    # RESTORE = ['psql -U db_user -h localhost db_name < backup']
