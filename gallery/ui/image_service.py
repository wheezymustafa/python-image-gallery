import boto3
import os

client = boto3.client('s3')
IMAGE_BUCKET_NAME='edu.au.cc.dam0045.image-gallery'
IMAGE_PATH='static/images'

def get_image(imageid):
    if image_is_available(imageid):
        return get_formatted_file_path(imageid) 
    response = client.get_object(Bucket=IMAGE_BUCKET_NAME, Key=imageid)

    if response is None:
        return None
    else:
        if save_image(imageid, response['Body'].read()):
            return True 
        else:
            return False

def save_image(imageid, image):
    try:
        if not os.path.exists(IMAGE_PATH):
            os.makedirs(IMAGE_PATH)

        file_path = '{}/{}'.format(IMAGE_PATH, imageid)
        file = open(file_path, 'wb')
        file.write(image)
        file.close()
    except:
        return False

    return True

def image_is_available(imageid):
    return True if os.path.exists(IMAGE_PATH) and os.path.exists(get_formatted_file_path(imageid)) else False

def get_formatted_file_path(imageid):
    return '{}/{}'.format(IMAGE_PATH, imageid)


def upload_image(imageid, image):
    try:
        client.put_object(Bucket=IMAGE_BUCKET_NAME, Key=imageid, Body=image)
    except:
        return False
    return True


def delete_image(imageid):
    try:
        resp = client.delete_object(Bucket=IMAGE_BUCKET_NAME, Key=imageid)
        return True if resp.DeleteMarker else False
    except:
        return False
