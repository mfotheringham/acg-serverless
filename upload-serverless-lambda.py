import json
import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:ap-southeast-2:774983433151:deployServerless')
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    
    serverless_bucket = s3.Bucket('fipjip.com')
    build_bucket = s3.Bucket('build.fipjip.com')
    
    serverless_zip = StringIO.StringIO()
    build_bucket.download_fileobj('build.zip', serverless_zip)
    
    with zipfile.ZipFile(serverless_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            serverless_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            serverless_bucket.Object(nm).Acl().put(ACL='public-read')
    topic.publish(Subject="Lambda Message", Message="Serverless deployed successfully!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
