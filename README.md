# summarize-sale-data-aws
When data is inserted in s3, trigger lambda to aggregate it. Post aggregated data in RDS, file log in DynamoDB and notify client. In case of any processing error data is inserted in error bucket of s3

# CloudFormation Resource Creation
* Create IAM role for lambda manually with access to S3, DynamoDB, SNS and RDS
* Create database from https://www.db4free.net/ and create table with schema as in code
* Create S3 bucket. Upload files of cloudformation code, lambda layer and python code
* Deploy resources using Cloudformation
* Subscribe to SNS
* Test the workflow

# Demo Video
* https://youtu.be/HBt8MXHcaPI
