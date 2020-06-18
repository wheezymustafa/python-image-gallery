#!/usr/bin/bash
export IMAGE_GALLERY_BOOSTRAP_VERSION="1.0"
export SCRIPT_NAME="ec2-prod-latest.sh"
aws s3 cp s3://edu.au.cc.dam0045.image-gallery-config/$SCRIPT_NAME ./
/usr/bin/bash $SCRIPT_NAME
