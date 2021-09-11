import datetime
import os
import boto3
from botocore.exceptions import ClientError

TODAY = datetime.datetime.now().date() 
SES_EMAIL = os.environ['SES_EMAIL']
SES_REGION = os.environ['SES_REGION']
IAM_EMAIL_TAG_KEY = os.environ['IAM_EMAIL_TAG_KEY']

iam = boto3.client('iam') 
ses = boto3.client('ses', region_name=SES_REGION) 

# Send Notification Email via SES
def send_noti_email(user_email, access_key_id):
  ses.send_email(
    Source=SES_EMAIL,
    Destination={'ToAddresses': [user_email]},
    Message={
      'Subject': {'Data': ('Warning! Your IAM Access Key is over 30 days old')},
      'Body': {
        'Text': {
          'Data': 'Please create new access key to use and deactivate/remove this Access Key ID ' f'Access Keys: {access_key_id}'
        }
      }
    }
  )
  print("Done sending email")

# Check Access Key ID Creation Day with Current Date
def key_age_check(date_time):
  converted_dt = date_time.date() 
  time_diff = (TODAY - converted_dt).days
  return time_diff

# Check and Return User Tag Value based on IAM User Tags
def get_user_tag(user_name, tag_name):
  user_info = iam.get_user(UserName=user_name)['User']
  result = False
  if "Tags" in user_info:
    for tag in user_info['Tags']: 
      if tag['Key'] == tag_name: 
        result = tag['Value']
        break
  return result

# Main Lambda Function
def lambda_handler(event, context):
  try:
    user_list = iam.list_users()['Users']

    for user in user_list:
      user_name = user['UserName']
      print(user_name)
      user_email = get_user_tag(user_name, IAM_EMAIL_TAG_KEY)
      if user_email is False:
        print("This user has no email tag.")
        continue
      print(user_email)
      user_access_keys_list = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
      for access_key in user_access_keys_list:
        access_key_id = access_key['AccessKeyId']
        if access_key['Status'] == "Active":   # Active Key only
          if key_age_check(access_key['CreateDate']) > 30:   # Get Access Key Age and check if it is older than 30 days
            print('Access Key ID ' + access_key_id + ' of User ' + user_name + ' is over 30 days old')
            send_noti_email(user_email, access_key_id)

  except ClientError as err:
    print(err.response['Error']['Message'])

  except Exception as err:
    print(err)