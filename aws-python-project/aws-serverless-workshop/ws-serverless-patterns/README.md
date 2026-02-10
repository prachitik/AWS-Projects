## WS Serverless Patterns – AWS SAM + Python

A hands-on implementation of AWS Serverless Patterns using AWS SAM, Python, and core AWS services including:

1. AWS Lambda

2. Amazon API Gateway

3. Amazon DynamoDB

4. Amazon Cognito

5. Amazon SNS / Event-driven patterns

6. CloudWatch Monitoring

This project is built by following AWS Workshop Labs and enhanced with troubleshooting, deployment validation, and runtime experimentation.

### Architecture Overview

This workshop implements:

#### Module 2 – Users Service

1. API Gateway → Lambda → DynamoDB 
2. REST endpoints for user CRUD
3. Infrastructure defined using SAM

#### Module 3 – Orders Service

1. Authenticated API Gateway

2. Lambda functions with Cognito authorizer

3. DynamoDB order persistence

#### Module 4 – User Profile Service

1. Event-driven architecture

2. Asynchronous processing

3. Address management with DynamoDB

4. Observability & monitoring

Project Structure
```
aws-serverless-workshop/
│
├── ws-serverless-patterns/
│   ├── users/
│   ├── orders/
│   ├── userprofile/
│   ├── module3_setup.sh
│   ├── module4_setup.sh
│   └── template.yaml
│
├── .venv/
└── README.md
```

Each module is independently deployable using AWS SAM.

#### Prerequisites

- macOS Monterey (12.x)

- Python 3.12

- AWS CLI configured

- AWS SAM CLI

- Docker Desktop

- Node.js (for CDK modules if used)

- AWS Account (Free Tier eligible)

#### Verify installation:
``
aws --version
sam --version
python3 --version
docker --version
``

#### Setup
1. Clone Repository
   ``
git clone https://github.com/prachitik/AWS-Projects.git
cd ws-serverless-patterns 
``

3. Create Virtual Environment
   ``
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``

4. Deploying a Module

Example for Users service:
``
cd users
sam build
sam deploy --guided 
``


Follow prompts:

Region: us-east-2

Stack name: ws-serverless-patterns-users

Confirm IAM changes: Yes

### Running Integration Tests

From module directory:
```
source .venv/bin/activate
pytest tests/integration -v 
```


To repeatedly test:
```
cmd="pytest tests/integration -v"
for i in $(seq 5); do $cmd; sleep 10; done 
```

### Authentication (Cognito)

Some modules require JWT tokens.

Obtain token:

Log in via Cognito Hosted UI

Extract ID token

Use in API calls:
```
TOKEN="Bearer <JWT_TOKEN>"
```

Example:
```
curl -X POST $API_URL \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "restaurantId":"rest-1","totalAmount":20 }'
```
### Troubleshooting Highlights
1. Lambda Import Error – No module named 'distutils'

  - Cause:  Python 3.12 removes distutils
  - Fix: Upgrade dependencies or replace distutils usage

  - Rebuild and redeploy:
    ```
    sam build
    sam deploy
    ```
2. 502 Bad Gateway

  - Usually means:

    -- Lambda crashed

    -- Import error

    -- Missing environment variable

    -- Check logs:
        ```
        aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"
        ```
3. Unauthorized (401)

  - Missing or expired JWT token

  - Incorrect Cognito configuration

4. Monitoring

  - CloudWatch:

  - Lambda invocation metrics

  - Errors

  - Duration

  - API Gateway logs

5. DynamoDB:

  - Table item count

On-demand billing mode

#### Key Learnings

- Infrastructure as Code using AWS SAM

- API Gateway + Lambda integration patterns

- Event-driven design

- Debugging Lambda runtime issues

- Managing Python 3.12 compatibility

- Handling authentication with Cognito

- CloudWatch troubleshooting

- Reserved concurrency experimentation

#### Improvements / Extensions

- Add CI/CD using GitHub Actions

- Add structured logging with AWS Powertools

- Add tracing with AWS X-Ray

- Add alarms for Lambda failures

- Implement rate limiting

#### Author

Prachiti Kulkarni
Backend Engineer | Cloud Enthusiast | AWS Certified

#### License

This project is based on AWS Serverless Workshop materials and adapted for learning purposes.


