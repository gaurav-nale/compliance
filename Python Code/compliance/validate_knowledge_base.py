import boto3

def get_knowledge_base_information(knowledge_base_id, text_to_validate):
    try:
        bedrock_client = boto3.client(
            service_name = "bedrock-agent-runtime",
            region_name = "us-east-2",
            aws_access_key_id='ASIA3FLD26ANIBVWWMQD', 
            aws_secret_access_key='g5R+PZ1CZCAJ3+PvuyYN8OElsks+UrH6pb8sifUe',
            aws_session_token = 'IQoJb3JpZ2luX2VjEH0aCXVzLWVhc3QtMSJIMEYCIQC3uCeUuxgYMLTI8i1AndMHlb07CV58bxM+ol0iYKkswAIhAOaAJb1lXWuIcorhoM6I0bfsaRqBmYECVx2TGUVgXfcBKvwCCMb//////////wEQABoMNzY3Mzk3OTE2Njk4IgyKm3NiOJZAToet4A0q0AKiRq8upVThfSLaakljNEdDoFkpdx2smMr/xVJOCBnSxe3BDhbGa048AfSK+ATb+YHX+HTr4QKi+1b+jC0OlF/z99wF75yAJsMCe8mqzCJ4UJYkYSZ+Ml0Wa9Kk4gszppGBGkBgCO8Q5qxzkc0520s6bRkcQ70NkLL8emVL86z0l1KYwDsO+NToM5pFPTQPdUAZaK2tCRjP6ynSIV3CmvLJNttKF6BQTjg8K1s1tfKfKQpRaoqYQMWnuldIo2GCfoAU8hZM3xqrgEv/6dLGVqkfSf6EbqYT65O+NuRgBocw8+SJEmVuqGCJiTG5pV/Cm9ll+Mo8kyiKv+r6QmFXg/cfdqM3nbL9dB0Fknc9Lgc+4zhXjyFz9DAU6sGoYqMo/76/elMPNHbd2x2pRd3WMXhSLNgsrJwiG94EeujvXY5v2sTM4Akn1WOrRBqJllNNtM4w7ejHvgY6pgEdd8WhsEBYwtxSppzC3Wd8F0eZmNaQ8pL10J/LUrxGvAx9hr7gxz3Ck5Iyq0tOLJC0O6xO/GE51tLL9C3EtZG3Z0V/6zTLAfBUUiRqqhV2pzXrj2xXDVL142lIRefHybzM7he/EgkWpEbSGduu3KR24X+01WDAi8wG9NJRcL+SeBpKsTuS3XVPAD5u9lY1bbOS2RfEmlSt2PrloVGXTQl6OAR5M8K6'
        )

        response = bedrock_client.retrieve_and_generate(
            input = {
                "text" : text_to_validate
            },
            retrieveAndGenerateConfiguration = {
                "type" : "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration" : {
                    "knowledgeBaseId" : knowledge_base_id,
                    "modelArn" : "meta.llama3-3-70b-instruct-v1:0"
                }
            }
        )

        return response

    except Exception as e:
        print("Error: ", str(e))

knowledge_base_id = "EIGVGRJK8W"
text_to_validate = "Tisa Kish"

response = get_knowledge_base_information(knowledge_base_id, text_to_validate)

if response:
    citations = response['citations']
    print("Information is validated and is available in our knowledge base!!")
    print("Response: ")
    print(citations[0]['generatedResponsePart']['textResponsePart']['text'])
    
    if citations[0].get('retrievedReferences') and citations[0]['retrievedReferences'][0].get('content') and citations[0]['retrievedReferences'][0]['content'].get('text'):
        reference_text = citations[0]['retrievedReferences'][0]['content']['text']
        print("Data in the knowledge base:") 
        print(reference_text)
    else:
        print("Retrieved reference has no text content.")
else:
    print("The input is not present in the knowledge base")