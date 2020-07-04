import boto3
import os

client = boto3.client('s3')
IMAGE_BUCKET_NAME='edu.au.cc.dam0045.image-gallery'
IMAGE_PATH='static/images'

def get_bucket_name():
    if os.environ['S3_IMAGE_BUCKET']:
        return os.environ['S3_IMAGE_BUCKET']
    else:
        return IMAGE_BUCKET_NAME

def get_image_path():
    if os.environ['IG_ROOT_PATH']:
        return '{}/{}'.format(os.environ['IG_ROOT_PATH'], IMAGE_PATH)
    else:
        return IMAGE_PATH

def get_image(imageid):
    if image_is_available(imageid):
        return get_formatted_file_path(imageid) 
    response = client.get_object(Bucket=get_bucket_name(), Key=imageid)

    if response is None:
        return None
    else:
        if save_image(imageid, response['Body'].read()):
            return True 
        else:
            return False

def save_image(imageid, image):
    if not os.path.exists(get_image_path()):
        print('Creating {}'.format(get_image_path()))
        os.makedirs(get_image_path())

    file_path = '{}/{}'.format(get_image_path(), imageid)
    file = open(file_path, 'wb')
    file.write(image)
    file.close()

def image_is_available(imageid):
    return True if os.path.exists(get_image_path()) and os.path.exists(get_formatted_file_path(imageid)) else False

def get_formatted_file_path(imageid):
    return '{}/{}'.format(get_image_path(), imageid)


def upload_image(imageid, image):
    try:
        client.put_object(Bucket=get_bucket_name(), Key=imageid, Body=image)
    except:
        return False
    return True


def delete_image(imageid):
    try:
        resp = client.delete_object(Bucket=get_bucket_name(), Key=imageid)
        return True if resp.DeleteMarker else False
    except:
        return False
