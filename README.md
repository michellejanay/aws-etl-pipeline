
# ETL Pipeline

## Project Background

This project was devised by Brian Thorpe of Generation UK for Generation UK’S Data Engineering October 24’ - January 25’ Cohort. 

We were tasked as a team to create a solution for Super Cafe as specified below. SuperCafe was a fictional chain of cafes imagined for the purposes of this project .

## Project Introduction

Super Café has hundreds of outlets. Up until now, a CSV file from each SuperCafe store, containing data about every transaction made for that day, has been uploaded to a piece of software installed in SuperCafe’s back office computers.They were experiencing issues with collating and analysing data produced at each branch. Also, they sought to best target new and returning customers. Also they have expressed a need to understand which products were selling well.

## Project Brief

We were to build a fully scalable ETL (Extract, Transform, Load) or ELT pipeline to handle large volumes of transaction data for the business SuperCafe, placing the data in a single location, such that the company’s data could be easily queried.

Flexibility of how this ETL pipeline was to be created was given though usage of Amazon Web Services, S3,L lambda, redshift, cloudformation cloudwatch and Virtual Private cloud was recommended and provided for.

It was the vision of the notional client that:
-Each night a CSV for each branch would be uploaded to the cloud. 
-The system developed would read each file and perform ETL steps, including the removal of sensitive data and the normalisation of data.
-Data would be stored in a data warehouse. 
-Data analytics software would be used to create Business Intelligence analytics for the Client. 
-Application monitoring software would be used to produce operational metrics, such as system errors, up-time and more.

## Other Specified Requirements.

- The Minimal Viable Product should be completed by the end of the fourth week.
- Adequate consideration of and prevention of unnecessary costs in the use of Web Services, through the selection of appropriate services and through services monitoring and through the use of efficient code, to be justified at fourth week presentation.

## Running the File

./deploy.sh de-course brew-crew brew-crew <ip>

Confirmation that the entire application has been deployed can be achieved by visiting the AWS Console> CloudFormation Section of the AWS Websire and checking that all components of the stack are described (as described in the illustrations below.) 

![CloudFormation Stack](https://github.com/michellejanay/aws-etl-pipeline/blob/main/readme_images/CloudFormation-stack.jpg)
![ETL Stack](https://github.com/michellejanay/aws-etl-pipeline/blob/main/readme_images/Etl_stack.jpg)
![Deployment Bucket Stack](https://github.com/michellejanay/aws-etl-pipeline/blob/main/readme_images/deployment-bucket-stack.jpg)


## Triggering the lambda function
Lambda functionality is automatically triggered when a CSV File is uploaded into the S3 Raw Data Bucket  

## Check Cloudwatch logs
These are available at the AWS CloudWatch Resource.

## Accessing Grafana
Find where Grafana is being hosted by going to EC2 > Instances in AWS.
Find your instance and click on it.
Open the given IP address.
In your browser. Use login details set in initial setup.

## Uploading files to Grafana to creating dashboards
Click on the hamburger menu to go to Dashboards.
Select 'New' > 'Import'
Upload the files from the grafana directory
Select 'Postgres' as the datasource. 

## How our design went about meeting the project's requirements. 

We understood from the outset that we would be creating an ETL pipeline. AWS Redshift was chosen as our Data Warehouse over Snowflake due to its relative cost. This determined the decision that we where going to engineer an ETL rather than an ELT pipeline.

Deploy.sh is a shell script that initiates the CloudFormation process. This script automates the creation of the Cloudformation at AWS with code, removing the need to manually create the CloudFormation at the AWS Console (Website/ GUI). This shell script builds the AWS Deployment Bucket. 

The deployment-bucket-stack.yml file holds the necessary perameters and naming conventions.

The shell script also builds the etl-stack. The etl-stack comprises all resources of the ETL Pipeline along with their properties.

Resources described by the etl stack are secured by the VPC, with the exclusion of the S3 Raw Data Bucket. The S3 Data Bucket exists solely within the public cloud.

An event is triggered when a CSV Raw Data File is uploaded into the S3 Raw Data Bucket through the Lambda function.

This lambda function encapsulates the entire ETL process, including the cleansing of the data and its being moved to the data warehouse (Redshift) for storage.

Clean data stored with Amazon Redshift is now available for data visualisations and insights via Grafana. 

An EC2 instance is the virtual server that incorporates Grafana into our system.

Grafana is used to monitor and visualise business trends and AWS resources.

The entire ETL process is monitored with AWS CloudWatch.

# How did you guarantee the project's requirements? 

During the project we were introduced to Amazon Web Services. We developed the fundamental knowledge and skills to construct an ETL pipeline using Amazon Web services CloudFormation, Lambda, S3 and Redshift.

We had Prior experience of converting CSV Files to Python files. We als had prior experience of writing functions to cleanse and normalise data, including those needed to remove sensitive or unwanted data.

Knowledge of how to query normalised data for the Grafana Dashboard Visualisations was acquired during the project.

We began the project with a thorough understanding of the client's needs. We documented business needs such as automation and reporting. Regular feedback from the client ensured that we met their expectations throughout the project
 
Using Agile methodology we broke the project into sprints and used a ticketing system amongst the team to complete tasks. After each sprint we reviewed the products development with the client.

# If you had more time, what is one thing you would improve upon? 

If we had more time we would do more testing including checking for edge cases to make sure the system works in all situations and doesn’t break under unexpected conditions.

For future improvements we could add more data analysis like tracking the busiest days of the week or during specific times. We could also set up real-time alerts using SNS to notify the client or engineers about important things like high resource usage or system issues so they can act quickly.

Another improvement would be optomising the Python code.

# What did you most enjoy implementing?

This project was a collaborative effort with clear role distribution. Some members focused on the ETL pipeline and python scripts, while others set up AWS resources and dashboards.

Everybody enjoyed working on the tasks they chose and collaborating as a group with other team members. We also liked sharing knowledge based on our research and findings. 

# Credits 
[Me (Michelle)](https://github.com/michellejanay) <br>
[Noor](https://github.com/Hunzaa) <br>
[Evans](https://github.com/e-ldn) <br>
[Adam](https://github.com/Adam5510) <br>
[Alex](https://github.com/AlexH1000598) <br>