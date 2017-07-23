import boto3
import paramiko
import os
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
# def lambda_handler():
    logger.info(event)
    print(event)

    msg = event['Records'][0]['Sns']['Message']
    # msg = {'ref':"refs/heads/master"}
    read = json.loads(msg)
    logger.info(read)
    print(read)
    
    try:
        logger.info("Connecting to S3")
        print("Connecting to S3")
        s3_client = boto3.client('s3')
        logger.info("S3 connected")
        print("S3 connected")
        
        logger.info("Downloding ssh key file")
        print("Downloding ssh key file")
        s3_client.download_file(os.environ['server_keys_bucket'], os.environ['key'], '/tmp/keyname.pem')
        os.chmod("/tmp/keyname.pem", 400)
        logger.info("Download complete")
        print("Download complete")

        branch = read['ref']
        kss_env = os.environ['ENV']
        # kss_env = 'master'
        
        if branch == "refs/heads/"+kss_env:
            logger.info("SSH to EC2 server")
            print("SSH to EC2 server")
            k = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            host= os.environ['host']

            try:
                logger.info("Connecting to " + host)
                print("Connecting to " + host)
                c.connect( hostname = host, username = os.environ['user'], pkey = k )
                logger.info("Connected to " + host)
                print("Connected to " + host)
            except botocore.exceptions.ClientError as e:
                logger.error(e)
                print e

            commands = [
                "aws s3 cp s3://"+os.environ['scripts_bucket']+"/"+os.environ['script_file']+" ./serverScript.sh --region "+os.environ['script_bucket_region'],
                "chmod 700 ./serverScript.sh",
                "./serverScript.sh"
                ]

            for command in commands:
                logger.info("Executing {}".format(command))
                print("Executing {}".format(command))
                stdin , stdout, stderr = c.exec_command(command)
                logger.info(stdout.read())
                logger.info(stderr.read())
    except Exception as e:
        logger.error(e)
        print e

    return event
