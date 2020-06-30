import boto3
import os

client = boto3.client('s3')
IMAGE_BUCKET_NAME='edu.au.cc.dam0045.image-gallery'
IMAGE_PATH='images'

def get_image(imageid):
    response = client.get_object(Bucket=IMAGE_BUCKET_NAME, Key=imageid)

    if response is None:
        return None
    else:
        file_path = save_image(imageid, response['Body'].read())
        return file_path

def save_image(imageid, image):
    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)

    file_path = '{}/{}'.format(IMAGE_PATH, imageid)
    file = open(file_path, 'wb')
    file.write(image)
    file.close()

    return file_path
