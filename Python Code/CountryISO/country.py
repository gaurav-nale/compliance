import boto3
import json
from datetime import datetime


bedrock_client = boto3.client(
    service_name = "bedrock-agent-runtime",
    region_name = "us-east-2",
    aws_access_key_id='ASIA3FLD26ANIRBJ54XZ', 
    aws_secret_access_key='AfZG2Xrihq2N+GuQgciB61X6KxT5fYX1eJyKqBRA',
    aws_session_token = 'IQoJb3JpZ2luX2VjEK///////////wEaCXVzLWVhc3QtMSJHMEUCIFBlwySfEgP4Evdab1ypMxnEpiOSUgDDv5WnfQB5R+B0AiEA884hAmK8fJ9auf7drI4FyKAQqChabAfAwLYWr7LlX20q/AII2P//////////ARAAGgw3NjczOTc5MTY2OTgiDAHLZE5eg0fpqJIebCrQAo+UAfUzfHp+s1dLtnexDxFSdExN3phwt4Q3ReA4Lm7Tk6K1Ran454pDJO4pBYs1IMDtBFqpVAcXAJOt295sc+9qoyetbggbuxIuLHukAc0HJDDhlDaYIALmHlvaE5YQ7plgnO8iyv+KFRcREiJRbcGfbbvjufQww1UYY8QbeGOxk2t8AHoAklz26qJuHyPIPO26QBoU/6alf5VuzPFQqSiiJk14D5KZ86+lgGKzM5q02CA+mHP5B9r82yxDp4fEvJTB0t1ike/MauZRg99zoUDW2W8TeEjbbWDSkF+CmLA8SyoiM7ZaFfmdFDUg9rb6fTD/iP2JcOfMsfHyXpl+0UScLtgirKdAF9/KukLyLj+H1AYQ4Vx76jeyzkinte6BKVAMIHk3EVokJIV6yu+lF23foYSGNuu62ooNw7AwJdGclZPEay4VuR3ELuuVNMtfRzDtquK9BjqnAbEF0OoZlUwDf/+r2UNI+KvvBliBfDtZz0HUhkErsPOZjA3HoqpEsmtMnjidVuGIM6ZB1Q0VapJ9gHVdwrbY0oAmRX3jXbIdeEu7l2rc0CS7Xg26suCwFII22sGSeJxIZfIP8eXE2h4X9TVO/WH0LCUeZ12Ow8MjO/wicoGFJyY69CicjoD288hLmwF7nHpek3ydDcTnEQb5Qx89zZsSPIxTTrX+po+l'
)

address_text = "2000 main St, Charlotte, NC, 28262, US"

prompt_text = f'''You have to act as an agent whose aim is to find the city, state, country from the {address_text} field.
It is not necessary that the address would be complete. There is chance that country can be misspelled or be present in ISO code. You need to understand the address and try to find the closest matching country based on city and state information present. The address can be any possible address from around the world.
You need to provide me with output which will havefloowing paramters. 
Output: 
status: some code that tells reliability of this data. (ACCURATE/PARTIALLY_ACCURATE, PROBABLE, FAILED)  **Just indicative.
postalAddress: 
  department;  
  subDepartment;
  streetName;
  buildingNumber;
  buildingName;
  floor;
  postBox;
  room;
  postCode;
  townName;
  townLocationName;
  districtName;
  countrySubDivision;
  country; //ISO Country code
  countryName
Our main goal is for townName and country as priority of findings.
Please do not provide any other details.
'''

# model_id = "amazon.titan-embed-text-v2:0"

# # Create payload for the model
# payload = {
#     'inputText': prompt_text
# }

# response = bedrock_client.invoke_model(
#     modelId=model_id,
#     body=json.dumps(payload)
# )

# response_body = json.loads(response["body"].read())

# print(response_body['results'][0]['outputText'])

prompt_text = 'Tell me about AEROCARIBBEAN AIRLINES'
knowledge_base_id = 'YJEVWBRMZE'

model_id = "amazon.titan-embed-text-v2:0"
# model_id = "amazon.titan-text-premier-v1:0"

payload = {
    "inputText" : prompt_text,
    # "retrievalConfig": {
    #         "retrievalMode": "AUTOMATIC"
    # }, 
    # "textGenerationConfig" : {
    #     "maxTokenCount" : 3072,
    #     "stopSequences" : [],
    #     "temperature" : 0.7,
    #     "topP" : 0.9
    #     }
}

response = bedrock_client.invoke_model(
    modelId = model_id,
    # knowledgeBaseId = knowledge_base_id,
    contentType = "application/json",
    accept = "application/json",
    body = json.dumps(payload)
)

response_body = json.loads(response["body"].read())
print(response_body)