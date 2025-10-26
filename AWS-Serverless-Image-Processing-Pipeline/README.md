AWS Serverless Image Processing Pipeline

A fully serverless image-processing pipeline built using AWS Lambda, Amazon S3, and Amazon DynamoDB.
This project automatically processes uploaded images — generating thumbnails, storing processed images in an output bucket, and recording metadata in DynamoDB.

Overview

This project demonstrates an event-driven serverless architecture using AWS services.
When an image is uploaded to the input S3 bucket, a Lambda function is automatically triggered to:

Retrieve the uploaded image

Resize it (e.g., generate a thumbnail) using the Pillow library

Save the processed image in the output S3 bucket

Store image metadata (dimensions, size, timestamps) in DynamoDB

Architecture Components
AWS Service	Purpose
Amazon S3 (Input Bucket)	Stores original images uploaded by the user. Triggers Lambda on object creation.
AWS Lambda (image-processor-lambda)	Processes images using Pillow, saves thumbnails, and writes metadata.
Amazon S3 (Output Bucket)	Stores processed images under the processed/ folder.
Amazon DynamoDB (ImageMetadata)	Stores metadata of processed images (original/processed dimensions, size, timestamps).
AWS IAM	Provides Lambda permissions to access S3 and DynamoDB.

Workflow

Upload an image to the input S3 bucket (e.g., input-bucket/).

The Lambda function (image-processor-lambda) is automatically triggered by the ObjectCreated event.

Lambda:

Downloads the uploaded image

Resizes it using Pillow

Uploads the processed image to the output bucket under processed/

Inserts metadata into DynamoDB

You can verify results by:

Checking the output bucket for the processed image

Viewing CloudWatch logs

Confirming metadata in DynamoDB

   DynamoDB Table: ImageMetadata
Attribute	Type	Description
image_name	String (Primary Key)	Original image file name
original_width	Number	Width of the input image
original_height	Number	Height of the input image
processed_width	Number	Width of the output image
processed_height	Number	Height of the output image
original_size_bytes	Number	File size of the input image
processed_size_bytes	Number	File size of the output image
timestamp	String	UTC timestamp when image was processed
    Lambda Function Code (image-processor-lambda)
        lambda_function.py

    Example Output
Input:

     input-bucket/photo.jpg

Output:

     output-bucket/processed/thumb_photo.jpg

DynamoDB Item:

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

     Logs (CloudWatch Example)
Event received: {...}
Processing image from bucket: input-bucket, key: photo.jpg
Original image size: 1920x1080
Processed image size: 200x113
Metadata stored successfully in DynamoDB.

     Key Learnings

Event-driven architecture with S3 triggers

Image manipulation using Pillow in Lambda layers

Metadata management via DynamoDB

End-to-end serverless design pattern

     Future Enhancements

Add SNS or SES notification after processing

Include additional image filters (e.g., grayscale, compression)

Add API Gateway to trigger Lambda manually

Enable user uploads through a web interface

