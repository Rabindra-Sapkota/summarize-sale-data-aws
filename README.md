# summarize-sale-data-aws
When data is inserted in s3, trigger lambda to aggregate it. Post aggregated data in RDS, file log in DynamoDB and notify client. In case of any processing error data is inserted in error bucket of s3

# CloudFormation Resource Creation
* Create s3 bucket and upload all file content there
* Create IAM role for lambda manually with access to s3, dynamodb, sns, rds
* Create SNS resource first as lambda code depends on it
* Database creation takes long time. So for test, create database from https://www.db4free.net/
* Create zip file for lambda layer and lambda code updating value of SNS arn. Also note name for other resources
* Create Rest of the resources
