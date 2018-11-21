import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

serverless_bucket = s3.Bucket('fipjip.com')
build_bucket = s3.Bucket('build.fipjip.com')

serverless_zip = StringIO.StringIO()
build_bucket.download_fileobj('build.zip', serverless_zip)

with zipfile.Zipfile(serverless_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        serverless_bucket.upload_fileobj(obj,nm,
            ExtraArgs={'Content-Type': mimetypes.guess_type(nm)[0]})
        serverless_bucket.Object(nm).Acl().put(ACL='public-read')
