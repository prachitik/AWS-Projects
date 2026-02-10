# Serverless Users API

A serverless REST API for user management built with AWS SAM, featuring JWT authentication via Amazon Cognito.

## Architecture

- **API Gateway**: REST API endpoints
- **Lambda Functions**: Business logic for user operations and JWT authorization
- **DynamoDB**: User data storage
- **Cognito**: User authentication and JWT token management

## Infrastructure Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Client    │───▶│ API Gateway  │───▶│ Lambda          │
│ Application │    │              │    │ Authorizer      │
└─────────────┘    └──────────────┘    └─────────────────┘
                           │                      │
                           │                      ▼
                           │            ┌─────────────────┐
                           │            │ Amazon Cognito  │
                           │            │ User Pool       │
                           │            └─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐    ┌─────────────────┐
                  │ Lambda Function │───▶│   DynamoDB      │
                  │ (Users API)     │    │ Users Table     │
                  └─────────────────┘    └─────────────────┘
```

## Data Flow

### Authentication Flow
1. **User Login**: Client authenticates with Cognito User Pool
2. **JWT Token**: Cognito returns JWT token
3. **API Request**: Client includes JWT token in Authorization header
4. **Token Validation**: Lambda Authorizer validates JWT with Cognito
5. **Access Grant**: Valid token allows API access

### API Request Flow
1. **Request**: Client sends HTTP request to API Gateway
2. **Authorization**: API Gateway invokes Lambda Authorizer
3. **Validation**: Authorizer validates JWT token with Cognito
4. **Processing**: Valid request routed to Users Lambda function
5. **Database**: Lambda function performs CRUD operations on DynamoDB
6. **Response**: Result returned through API Gateway to client

```
Client ──[JWT]──▶ API Gateway ──▶ Authorizer ──▶ Cognito
   ▲                   │              │
   │                   ▼              ▼
   └──[Response]── Users Lambda ──▶ DynamoDB
```

## API Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| GET | `/users` | List all users | Yes |
| POST | `/users` | Create new user | Yes |
| GET | `/users/{userid}` | Get user by ID | Yes |
| PUT | `/users/{userid}` | Update user | Yes |
| DELETE | `/users/{userid}` | Delete user | Yes |

## Prerequisites

- AWS CLI configured
- SAM CLI installed
- Python 3.12

## Deployment

```bash
# Build the application
sam build

# Deploy with guided prompts
sam deploy --guided

# Or deploy with parameters
sam deploy --parameter-overrides UserPoolAdminGroupName=apiAdmins
```

## Authentication

1. **Create a user in Cognito User Pool** (use output `UserPool` ID)
2. **Get JWT token**:
   ```bash
   aws cognito-idp initiate-auth \
     --auth-flow USER_PASSWORD_AUTH \
     --client-id <UserPoolClient> \
     --auth-parameters USERNAME=<email>,PASSWORD=<password> \
     --query 'AuthenticationResult.IdToken' \
     --output text
   ```
3. **Use token in API calls**:
   ```bash
   curl -H "Authorization: <jwt-token>" \
        https://<api-endpoint>/Prod/users
   ```

## Usage Examples

### Create User
```bash
curl -X POST https://<api-endpoint>/Prod/users \
  -H "Authorization: <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```

### Get All Users
```bash
curl https://<api-endpoint>/Prod/users \
  -H "Authorization: <jwt-token>"
```

## Local Testing

```bash
# Test with sample event
sam local invoke UsersFunction -e events/event-post-user.json

# Start local API
sam local start-api
```

## Cleanup

```bash
sam delete
```