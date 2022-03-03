# Project Overview
When data is inserted in reprocess S3 bucket by user, lambda is triggered which aggregates the data, posts aggregated
data in RDS, logs in DynamoDB and notifies client. In case of any processing error it inserts data in error bucket,
logs in dynamodb and notifies client

# Steps For CloudFormation Resource Creation
* Create IAM role for lambda manually with access to S3, DynamoDB, SNS and RDS
* Create database from https://www.db4free.net/
* Create table using create_table_get_records_to_test module locally with flag CREATE_TABLE as True
* Create S3 bucket. Upload files of cloudformation code, lambda layer and python code
* Deploy resources using Cloudformation
* Subscribe to SNS
* Add trigger from reprocess s3 to lambda manually
* Test the workflow
* Validate data in RDS with create_table_get_records_to_test module locally with flag CREATE_TABLE as False

# Demo Video for cloud formation deployment
* https://youtu.be/HBt8MXHcaPI

# Demo video for manual deployment
* https://youtu.be/HBt8MXHcaPI
