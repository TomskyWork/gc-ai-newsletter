import boto3
import botocore

from aws.bedrock.ai_models import ai_models


def create_ai_summary(article_content,settings):
    # Initialize Bedrock client
    #session = boto3.session.Session()
    bedrock = boto3.client(service_name='bedrock-runtime', region_name=settings.aws_region)

    # Create prompt for summarization
    # TODO   CHANGE only 500 chars to summarize !!!!!
    # TODO it also has max tokens in prompt !!!
    prompt = f"""Please provide a short summary of the following text. Do not add any information that is not mentioned in the text below.
    <text>
    {article_content[:500]}
    </text>
    """

    # Create a converse request with our summarization task
    agent_request = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "temperature": 0.4,
            "topP": 0.9,
            "maxTokens": 500
        }
    }

    # Call Claude 3.7 Sonnet with Converse API
    try:
        response = bedrock.converse(
            modelId=ai_models["Claude 3.7 Sonnet"],
            messages=agent_request["messages"],
            inferenceConfig=agent_request["inferenceConfig"]
        )
        summary = response["output"]["message"]["content"][0]["text"]
        return summary


    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDeniedException':
            print(f"\x1b[41m{error.response['Error']['Code']}: {error.response['Error']['Message']}\x1b[0m")
            print("Please ensure you have the necessary permissions for Amazon Bedrock.")
        else:
            raise error