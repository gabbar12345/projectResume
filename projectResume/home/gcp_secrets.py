# from google.cloud import secretmanager
# import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/rahulsingh594/Documents/Rahul/ResumeProject/my-project1-417010-f658b1ea1104.json"

# def access_secret_version(project_id, secret_id, version_id="latest"):
#     """
#     Access the payload for the given secret version if one exists. The version
#     can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
#     """

#     # Create the Secret Manager client.
#     client = secretmanager.SecretManagerServiceClient()

#     # Build the resource name of the secret version.
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

#     # Access the secret version.
#     response = client.access_secret_version(name=name)

#     # Return the decoded payload.
#     payload = response.payload.data.decode("UTF-8")
#     return payload

# # Usage example:
# project_id = "my-project1-417010"
# secret_id = "openai-key"
# # api_key = access_secret_version(project_id, secret_id)
# # print("Retrieved API Key:", api_key)


# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

# import boto3
# from botocore.exceptions import ClientError
# import json


# def get_secret():

#     secret_name = "my_secret_api"
#     region_name = "us-east-1"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     secret = get_secret_value_response['SecretString']
#     return json.loads(secret)


#     # Your code goes here.