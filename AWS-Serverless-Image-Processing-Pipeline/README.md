## AWS Serverless Image Processing Pipeline

A fully serverless image-processing pipeline built using AWS Lambda, Amazon S3, and Amazon DynamoDB.
This project automatically processes uploaded images — generating thumbnails, storing processed images in an output bucket, and recording metadata in DynamoDB.

### Overview

This project demonstrates an event-driven serverless architecture using AWS services.
When an image is uploaded to the input S3 bucket, a Lambda function is automatically triggered to:

1. Retrieve the uploaded image

2. Resize it (e.g., generate a thumbnail) using the Pillow library

3. Save the processed image in the output S3 bucket

4. Store image metadata (dimensions, size, timestamps) in DynamoDB

### Architecture Components
AWS Service	Purpose
Amazon S3 (Input Bucket) - Stores original images uploaded by the user. Triggers Lambda on object creation.
AWS Lambda (image-processor-lambda) - Processes images using Pillow, saves thumbnails, and writes metadata.
Amazon S3 (Output Bucket) -	Stores processed images under the processed/ folder.
Amazon DynamoDB (ImageMetadata)	- Stores metadata of processed images (original/processed dimensions, size, timestamps).
AWS IAM	- Provides Lambda permissions to access S3 and DynamoDB.

### Workflow

1. Upload an image to the input S3 bucket (e.g., input-bucket/).

2. The Lambda function (image-processor-lambda) is automatically triggered by the ObjectCreated event.

    Lambda:

       1) Downloads the uploaded image

       2) Resizes it using Pillow

       3) Uploads the processed image to the output bucket under processed/

       4) Inserts metadata into DynamoDB

3. You can verify results by:

       1) Checking the output bucket for the processed image

       2) Viewing CloudWatch logs

       3) Confirming metadata in DynamoDB

**DynamoDB Table**: ImageMetadata
| Attribute              | Type                 | Description                            |
| ---------------------- | -------------------- | -------------------------------------- |
| `image_name`           | String (Primary Key) | Original image file name               |
| `original_width`       | Number               | Width of the input image               |
| `original_height`      | Number               | Height of the input image              |
| `processed_width`      | Number               | Width of the output image              |
| `processed_height`     | Number               | Height of the output image             |
| `original_size_bytes`  | Number               | File size of the input image           |
| `processed_size_bytes` | Number               | File size of the output image          |
| `timestamp`            | String               | UTC timestamp when image was processed |


**Lambda Function Code (image-processor-lambda)**
lambda_function.py

**Example Output**
- Input:

     input-bucket/photo.jpg

- Output:

     output-bucket/processed/thumb_photo.jpg

- DynamoDB Item:
```
{
  "image_name": "photo.jpg",
  "original_width": 1920,
  "original_height": 1080,
  "processed_width": 200,
  "processed_height": 113,
  "original_size_bytes": 202345,
  "processed_size_bytes": 54321,
  "timestamp": "2025-10-25T18:45:00Z"
}
```

- Logs (CloudWatch Example)
```  
Event received: {...}
Processing image from bucket: input-bucket, key: photo.jpg
Original image size: 1920x1080
Processed image size: 200x113
Metadata stored successfully in DynamoDB.
```

### Key Learnings

- Event-driven architecture with S3 triggers

- Image manipulation using Pillow in Lambda layers

- Metadata management via DynamoDB

- End-to-end serverless design pattern

### Future Enhancements

- Add SNS or SES notification after processing

- Include additional image filters (e.g., grayscale, compression)

- Add API Gateway to trigger Lambda manually

- Enable user uploads through a web interface

Step-by-Step Project Setup
   Step 1: Create S3 Buckets

Create two buckets in the same region:

image-input-bucket

image-output-bucket

Keep Block all public access enabled.

   Step 2: Create IAM Role for Lambda

Create a role LambdaExecutionRole with the following policies:

AmazonS3FullAccess

AmazonDynamoDBFullAccess

CloudWatchLogsFullAccess

   Step 3: Create DynamoDB Table

Create a table:

Name: ImageMetadata

Partition key: image_name (String)

Billing mode: On-demand

   Step 4: Build and Publish Pillow Lambda Layer

SSH into your EC2 instance (Amazon Linux 2023):

mkdir lambda_pillow_layer && cd lambda_pillow_layer
pip install pillow==10.2.0 -t python/
zip -r pillow_layer.zip python
aws lambda publish-layer-version \
  --layer-name pillow-layer \
  --zip-file fileb://pillow_layer.zip \
  --compatible-runtimes python3.9 \
  --region us-east-2


Copy the Layer ARN from the output.

  Step 5: Create the Lambda Function

Name: image-processor-lambda

Runtime: Python 3.9

Execution Role: LambdaExecutionRole

Layer: Add your published Pillow layer

Lambda Function Code:

import boto3
import os
from PIL import Image
from io import BytesIO
import json
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageMetadata')

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        
        # Download image
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_data = response['Body'].read()
        image = Image.open(BytesIO(image_data))
        original_size = image.size
        print(f"Original size: {original_size}")
        
        # Resize
        image.thumbnail((128, 128))
        processed_key = f"processed/thumb_{os.path.basename(object_key)}"
        print(f"Processed image path: {processed_key}")
        
        # Upload to output bucket
        output_bucket = "image-output-bucket"
        buffer = BytesIO()
        image.save(buffer, format=image.format)
        buffer.seek(0)
        s3.put_object(Bucket=output_bucket, Key=processed_key, Body=buffer)
        print(f"Processed image uploaded to {output_bucket}/{processed_key}")
        
        # Store metadata
        table.put_item(Item={
            'image_name': os.path.basename(object_key),
            'bucket': bucket_name,
            'output_bucket': output_bucket,
            'processed_key': processed_key,
            'original_width': original_size[0],
            'original_height': original_size[1],
            'processed_width': image.size[0],
            'processed_height': image.size[1],
            'timestamp': int(time.time())
        })
        print("Metadata inserted successfully in DynamoDB.")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image processed successfully!'})
        }

    except Exception as e:
        print("Error processing image:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

  Step 6: Add S3 Trigger

Go to your input bucket → Properties → Event Notifications → Create event.

Select event type: All object create events.

Choose Destination → Lambda → image-processor-lambda.

Save and verify trigger is active.

🧪 Step 7: Test End-to-End

Upload an image to your input bucket.

Check:

Processed image in image-output-bucket/processed/

Metadata in DynamoDB ImageMetadata

Logs in CloudWatch (should show original/processed dimensions).

   Expected Output:

Lambda resizes the image.

Saves processed image in the output bucket.

Inserts metadata into DynamoDB.

CloudWatch shows execution trace.

