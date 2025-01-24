#!/usr/bin/env bash
set -eu

#### CONFIGURATION SECTION ####
aws_profile="$1" # e.g. de-course
your_name="$2" # e.g. brew-crew
team_name="$3" # e.g. brew-crew (used for redshift details)

# EC2 config
ec2_ingress_ip="$4" # e.g. 12.34.56.78 (IP can be found on: https://whatismyipaddress.com)

deployment_bucket="${your_name}-deployment-bucket"
ec2_userdata=$(base64 -i userdata)

#### CONFIGURATION SECTION ####

echo ""
echo "Deleting deployment bucket..."
echo ""


echo ""
echo "Checking if bucket exists..."
echo ""

# Check if bucket exists before attempting to delete
if aws s3api head-bucket --bucket "${your_name}-deployment-bucket" --profile ${aws_profile} 2>/dev/null; then
    echo "Bucket exists, deleting..."

# Deletes the deployment bucket stack
aws cloudformation delete-stack --stack-name "${your_name}-deployment-bucket" \
    --profile ${aws_profile}

# Empties the buckets before deletion
aws s3 rm s3://"${your_name}-deployment-bucket" --recursive \
    --profile ${aws_profile}

# Deletes the buckets
aws s3 rb s3://"${your_name}-deployment-bucket" --force \
    --profile ${aws_profile}

else
    echo "Bucket "${your_name}-deployment-bucket" does not exist. Skipping deletion"
fi


echo ""
echo "Deleting etl stack..."
echo ""


echo ""
echo "Checking if bucket exists..."
echo ""

# Check if bucket exists before attempting to delete
if aws s3api head-bucket --bucket "${your_name}-raw-data" --profile ${aws_profile} 2>/dev/null; then
    echo "Bucket exists, deleting..."

# Deletes the etl-stack
aws cloudformation delete-stack --stack-name "${your_name}-etl-stack" \
    --profile ${aws_profile}

# Empties the buckets before deletion
aws s3 rm s3://"${your_name}-raw-data" --recursive \
    --profile ${aws_profile}

# Deletes the buckets
aws s3 rb s3://"${your_name}-raw-data" --force \
    --profile ${aws_profile}

else
    echo "Bucket "${your_name}-raw-data" does not exist. Skipping deletion"
fi


echo ""
echo "...Full Deletion Complete!"
echo ""
