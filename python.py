import boto3

def lambda_handler(event, context):
    source_bucket = '${bucketname}'
    destination_bucket = '${bucketname}'
    
    s3_client = boto3.client('s3')
    
    # List objects in the source bucket
    objects = s3_client.list_objects_v2(Bucket=source_bucket)['Contents']
    
    for obj in objects:
        object_key = obj['Key']
        
        # Check if the object key exists in the destination bucket
        try:
            s3_client.head_object(Bucket=destination_bucket, Key=object_key)
        except:
            # If the head_object call raises an exception, the object doesn't exist in the destination bucket
            # Copy the object from the source bucket to the destination bucket
            s3_client.copy_object(Bucket=destination_bucket, CopySource=f"{source_bucket}/{object_key}", Key=object_key)
    
    return {
        'statusCode': 200,
        'body': 'Files synced successfully!'
    }
