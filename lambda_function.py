import json
import os
import boto3
import pprint
import logging

rekognition_client = boto3.client('rekognition', region_name='us-east-1')

AWS_ACCESS_KEY_ID = "**************"
AWS_SECRET_ACCESS_KEY = "***************************"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SBA_Objects')

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
read_bucket_name = "finddistinctpeoplevideo-s3bucket-sbhack"
write_bucket_name = 'finddistinctshot-s3bucket-sbhack'
read_from_bucket = s3.Bucket(read_bucket_name)
write_to_bucket = s3.Bucket(write_bucket_name)


def find_text(read_bucket, write_buket):
    rekognition_client = boto3.client('rekognition')
    # read_obj = s3_client.get_object(Bucket=read_bucket, Key='latest.jpg')

    # write_object =s3_client.put_object(
    #     ACL='public-read',
    #     Body=read_obj['Body'],
    #     Bucket=write_buket,
    #     ContentType='image/jpeg',
    #     Key='test.jpg'
    #     )

    bucket = read_bucket
    file_name = 'https://s3.amazonaws.com/finddistinctpeoplevideo-s3bucket-sbhack/latest.jpg'
    key_name = 'test.jpg'
    # s3_client.upload_file(file_name, bucket, key_name)


    with open(file_name, 'rb') as data:
        s3.upload_fileobj(data, bucket, 'test.jpg')

    print(read_obj['Body'])
    responsetext = rekognition_client.detect_text(
        Image={
            'S3Object': {
                'Bucket': 'finddistinctpeoplevideo-s3bucket-sbhack',
                'Name': 'latest.jpg'

            }
        }
    )
    return responsetext


def find_label(read_bucket):
    rekognition_client = boto3.client('rekognition')
    responselabel = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': 'finddistinctpeoplevideo-s3bucket-sbhack',
                'Name': 'latest.jpg'
            }
        }
    )
    return responselabel


def lambda_handler(event, context):
    textdata = find_text(read_bucket_name, write_bucket_name);
    labeldata = find_label(read_bucket_name);
    totallables = []
    for key in textdata['TextDetections']:
        if (key['Type'] == 'WORD'):
            totallables.append(key['DetectedText'])
    print(totallables)

    response = table.put_item(
        Item={
            'objectsId': "1",
            'pepsi': totallables.count('pepsi'),
            'papmers': totallables.count('Pampers'),
            'imageURL': 'https://s3.amazonaws.com/finddistinctpeoplevideo-s3bucket-sbhack/latest.jpg'

        })
    return {'pepsi': totallables.count('pepsi'), 'papmers': totallables.count('Pampers')}
