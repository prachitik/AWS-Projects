## AWS Serverless Image Processing Pipeline

A fully serverless image-processing pipeline built using AWS Lambda, Amazon S3, and Amazon DynamoDB.

### Overview
This project automatically resizes and processes images uploaded to an Amazon S3 input bucket, stores the processed versions in an output bucket, and logs metadata (such as image dimensions and timestamps) in Amazon DynamoDB — all powered by AWS Lambda and the Pillow library.

This project demonstrates a scalable, event-driven serverless architecture using multiple AWS services working together.


### Architecture Components
AWS Service	|  Purpose
1. Amazon S3 (Input Bucket) - Stores original images uploaded by the user. Triggers Lambda on object creation.
2. AWS Lambda (image-processor-lambda) - Processes images using Pillow, saves thumbnails, and writes metadata.
3. Amazon S3 (Output Bucket) -	Stores processed images under the processed/ folder.
4. Amazon DynamoDB (ImageMetadata)	- Stores metadata of processed images (original/processed dimensions, size, timestamps).
5. AWS IAM	- Provides Lambda permissions to access S3 and DynamoDB.

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
``Refer lambda_function.py``

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




### Step-by-Step Project Setup
   #### Step 1: Create S3 Buckets

  Create two buckets in the same region:

    image-input-bucket

    image-output-bucket

  Keep Block all public access enabled.

#### Step 2: Create IAM Role for Lambda

1. Create a role LambdaExecutionRole with the following policies:

AmazonS3FullAccess

AmazonDynamoDBFullAccess

CloudWatchLogsFullAccess

#### Step 3: Create DynamoDB Table

Create a table:

Name: ImageMetadata

Partition key: image_name (String)

Billing mode: On-demand

#### Step 4: Build and Publish Pillow Lambda Layer

1. SSH into your EC2 instance (Amazon Linux 2023):
   
```
mkdir lambda_pillow_layer && cd lambda_pillow_layer
pip install pillow==10.2.0 -t python/
zip -r pillow_layer.zip python
aws lambda publish-layer-version \
  --layer-name pillow-layer \
  --zip-file fileb://pillow_layer.zip \
  --compatible-runtimes python3.9 \
  --region us-east-2
```

2. Copy the Layer ARN from the output.

#### Step 5: Create the Lambda Function

Name: image-processor-lambda

Runtime: Python 3.9

Execution Role: LambdaExecutionRole

Layer: Add your published Pillow layer

Lambda Function Code: ``Refer lambda_function.py``


#### Step 6: Add S3 Trigger

1. Go to your input bucket → Properties → Event Notifications → Create event.

2. Select event type: All object create events.

3. Choose Destination → Lambda → image-processor-lambda.

4. Save and verify trigger is active.

 #### Step 7: Test End-to-End

1. Upload an image to your input bucket.

2. Check:

 - Processed image in image-output-bucket/processed/

- Metadata in DynamoDB ImageMetadata

- Logs in CloudWatch (should show original/processed dimensions).

### Expected Output:

- Lambda resizes the image.

- Saves processed image in the output bucket.

- Inserts metadata into DynamoDB.

- CloudWatch shows execution trace.

### Troubleshooting and Fixes
| Issue                                                                                           | Root Cause                                             | Resolution                                                                     |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| ❌ SSH timeout to EC2                                                                            | NACL inbound/outbound rules not allowing port 22       | Added SSH (22), HTTP (80), HTTPS (443), and ephemeral ports (1024–65535) rules |
| ❌ `InvalidSignatureException` when publishing layer                                             | IAM not configured properly on EC2                     | Attached proper IAM role and verified token-based metadata access              |
| ❌ `cannot import name '_imaging'`                                                               | Pillow version mismatch between EC2 and Lambda runtime | Rebuilt layer for Python 3.9 runtime                                           |
| ❌ `An error occurred (ValidationException): Missing key image_name`                             | DynamoDB table required partition key missing          | Added `'image_name'` attribute in `put_item()`                                 |
| ⚠️ Lambda returned `‘Records’` error on test                                                    | Event test JSON did not match S3 trigger structure     | Triggered via real S3 upload event instead of console test                     |
| ✅ **Final Fix:** All runtime, permissions, and event configurations aligned — system functional |                                                        |                                                                                |


### Key Learnings

- Event-driven architecture with S3 triggers

- Image manipulation using Pillow in Lambda layers

- Metadata management via DynamoDB

- End-to-end serverless design pattern
