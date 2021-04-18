import boto3
import json
from datetime import datetime

def create_stack_in_acc(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN):
    access_key_id= ACCESS_KEY
    secret_key= SECRET_KEY
    token = SESSION_TOKEN
    session = boto3.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_key,
    aws_session_token = token)
    s3 = boto3.client('s3',region_name='ap-southeast-1')
    response = s3.list_buckets()
    obj = s3.get_object(Bucket='testawscf01',Key='sample_ec2_template.json')
    template_raw_data = obj["Body"].read().decode('utf-8')

    cfn = boto3.client('cloudformation',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_key,
    aws_session_token = token 
    )
    current_ts = datetime.now().isoformat().split('.')[0].replace(':','-')
    stackname = 'ec2-template-lambda-ig' + current_ts
    capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
    print('after capabilities')
    try:
        template_params = json.loads(template_raw_data)
        # print(template_params)
        print('calling stack data')
        stackdata = cfn.create_stack(
            StackName=stackname,
            DisableRollback=True,
            TemplateURL='https://testawscf01.s3-ap-southeast-1.amazonaws.com/sample_ec2_template.json',
            #    Parameters=template_params,
            Capabilities=capabilities)
        print(stackdata)
        return stackdata
    except Exception as e:
        print(str(e))
        return null

def sts_assume_role_of_acc(aws_acc_id , role_name):
    sts_conn = boto3.client('sts')
    role_arn = 'arn:aws:iam::' + aws_acc_id+':role/'+ role_name
    # 'arn:aws:iam::711926560829:role/aws-lambda-cf'
    acct_b = sts_conn.assume_role(RoleArn=role_arn,
    RoleSessionName='cross_acct_lambda'
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    create_stack_in_acc(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN)

def lambda_handler(event, context):
    aws_acc_id = event['queryStringParameters']['account_id']
    role_name =event['queryStringParameters']['role_name']
    sts_assume_role_of_acc(aws_acc_id , role_name)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://s3-ap-southeast-1.amazonaws.com,https://1i51n04p12.execute-api.ap-southeast-1.amazonaws.com',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Resources have been deployed')
    }
