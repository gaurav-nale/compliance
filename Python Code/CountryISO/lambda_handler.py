import boto3
import uuid
import json

bedrock_client = boto3.client(
    service_name = "bedrock-agent-runtime",
    region_name = "us-east-2",
    config=boto3.session.Config(connect_timeout=10, read_timeout=60)
)

AGENT_ID = "HVONSZGGK6"
AGENT_ALIAS_ID = "VX6AZZIMCE"
SESSION_ID = str(uuid.uuid4())

def lambda_handler(event, context):
    print("Event : ", event)
    request_body = event.get('requestBody', {})
    input_text = request_body.get('InputText')

    print("Input Text : ", input_text)
    
    if not input_text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing input_text in event"})
        }

    try:
        response = bedrock_client.invoke_agent(
        agentId = AGENT_ID,             
        agentAliasId = AGENT_ALIAS_ID,  
        sessionId = SESSION_ID,                
        inputText = input_text
        )

        eventstream = response.get('completion')

        if eventstream is None:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "No completion response from Bedrock"})
            }

        print("Response : ", response)
        

        for events in eventstream:
            chunk = events.get('chunk', {})        
            chunk_bytes = chunk.get('bytes', '')

            print("Chunk Bytes : ", chunk_bytes)
            
            if chunk_bytes:
                try:
                    decoded_bytes = chunk_bytes.decode('utf-8')
                    apiResponse = {
                        'statusCode' : 200,
                        'body' : json.dumps({
                            "input" : input_text,
                            "response" : decoded_bytes
                        })
                    }
                except UnicodeDecodeError:
                    apiResponse = {
                        'statusCode' : 400,
                        'body' : json.dumps({
                            "input" : input_text,
                            "response" : "Error decoding bytes: {chunk_bytes}"
                        })
                    }
            else:
                apiResponse = {
                        'statusCode' : 400,
                        'body' : json.dumps({
                            "input" : input_text,
                            "response" : "No bytes found in the chunk."
                        })
                    }

    except Exception as e:
        print("Error invoking the agent : ", e)
        apiResponse = {
                        'statusCode' : 500,
                        'body' : json.dumps({
                            "input" : input_text,
                            "response" : "Error invoking the agent",
                            "error" : str(e)
                        })
                    }
    
    return apiResponse
