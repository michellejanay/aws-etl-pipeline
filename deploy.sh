#!/usr/bin/env bash
set -eu

#### CONFIGURATION SECTION ####
aws_profile="$1" # e.g. de-course
your_name="$2" # e.g. brew-crew
team_name="$3" # e.g. brew-crew (used for redhsift details)

# EC2 config
ec2_ingress_ip="$4" # e.g. 12.34.56.78 (IP can be found on: https://whatismyipaddress.com)

deployment_bucket="${your_name}-deployment-bucket"
ec2_userdata=$(base64 -i userdata)

#### CONFIGURATION SECTION ####

# Create a deployment bucket stack to hold our zip files of lambdas
echo ""
echo "Doing deployment bucket..."
echo ""
aws cloudformation deploy --stack-name "${your_name}-deployment-bucket" \
    --template-file deployment-bucket-stack.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM --profile ${aws_profile} \
    --parameter-overrides \
      YourName="${your_name}";

if [ -z "${SKIP_PIP_INSTALL:-}" ]; then
    echo ""
    echo "Doing pip install..."
    # Install dependencies from requirements-lambda.txt into src directory with python 3.9
    # On windows use `py` not `python3`
    py -m pip install --platform manylinux2014_x86_64 \
        --target=./src --implementation cp --python-version 3.9 \
        --only-binary=:all: --upgrade -r requirements-lambda.txt;
else
    echo ""
    echo "Skipping pip install"
fi

# Create an updated ETL packaged template "etl-stack-packaged.yml" from the default "etl-stack.yml"
# ...and upload local resources to S3 (e.g zips files of your lambdas)
# A unique S3 filename is automatically generated each time
echo ""
echo "Doing packaging..."
echo ""
aws cloudformation package --template-file etl-stack.yml \
    --s3-bucket ${deployment_bucket} \
    --output-template-file etl-stack-packaged.yml \
    --profile ${aws_profile};

# Deploy the main ETL stack using the packaged template "etl-stack-packaged.yml"
echo ""
echo "Doing etl stack deployment..."
echo ""
aws cloudformation deploy --stack-name "${your_name}-etl-stack" \
    --template-file etl-stack-packaged.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile ${aws_profile} \
    --parameter-overrides \
      YourName="${your_name}" \
      TeamName="${team_name}" \
      EC2InstanceIngressIp="${ec2_ingress_ip}" \
      EC2UserData="${ec2_userdata}";

echo ""
echo "...all done!"
echo ""
