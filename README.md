# summarize-sale-data-aws
When data is inserted in s3, trigger lambda to aggregate it. Post aggregated data in RDS, file log in DynamoDB and notify client. In case of any processing error data is inserted in error bucket of s3
