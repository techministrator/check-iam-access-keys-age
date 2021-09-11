# check-iam-access-keys-age

This function periodically checks all IAM users' access keys that are older than 30 days and send SES email notification to users' emails. 

This function requires the following:
- Verified SES Email which will be used to send email notification to individual user
- IAM user must have a **Tag Key that contains their email address**
- A CloudWatch Event or an EventBridge event with cron (based on your requirement) to run this function periodically. Take note that this function won't store any data to remember which IAM User Access Key it has sent noti email to in the last execution time. So be sure to apply the correct cron expression to run at your desired period. 
- Depends on the number of your IAM users, the Lambda Function Execution Timeout should be extend accordingly. if less than 100 users, 45 seconds is fine. RAM 128MB is enough. 

## Usage

For simplicity, install `serverless` CLI tool via this link: https://www.serverless.com/framework/docs/providers/aws/guide/installation/ <- very simple

Create lambda function

```sh
$ serverless deploy
```

If you receive Access Denied error, gradually add the required permissions shown up to your IAM User/Role or apply privileged permissions to run. 

---

**Note**: This function should be written in Async programming to speed up the checking time.