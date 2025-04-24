import mysql.connector
import boto3
import uuid
import json

def fetch_data_from_DB(name):
    conn = mysql.connector.connect(
        host = "finzly-bankos-uat.cls02uuoqpas.us-east-1.rds.amazonaws.com",
        port = 3309,
        user = "gaurav_nale",
        password = "YDTRT1Tbji7AUhRW",
        database = "galaxy_compliance_mcbankny_ai"
    )

    try:
        cursor = conn.cursor(dictionary = True)

        cursor.execute("""
    SELECT actioned_by, audit_description, source_system, action FROM `screening_audit`
    WHERE `last_updated_date` BETWEEN %s AND %s
    AND `actioned_by` = %s
    LIMIT 500
""", ("2025-02-19 20:44:43", "2025-03-20 20:44:43", name))

        result = cursor.fetchall()

        return result
    
    finally:
        cursor.close()
        conn.close()

def get_bedrock_response(data):
    bedrock_runtime = boto3.client(
            service_name = "bedrock-agent-runtime",
            region_name = "us-east-2",
            aws_access_key_id='ASIA3FLD26ANOB7YBSPL', 
            aws_secret_access_key='ecAd95VLnbNJAQO9X9GQv3WXtEcPcPcMB0UQbYoZ',
            aws_session_token = 'IQoJb3JpZ2luX2VjEFQaCXVzLWVhc3QtMSJHMEUCIQCFbYEuKfu6ofxAEcq/QDB0Trdg50+n2/0jXA/MdW1jGAIgGKTtyMjdBcZXVwd4vIMCcWAakzOAtMLIEtGRK11HFL8q/AII3f//////////ARAAGgw3NjczOTc5MTY2OTgiDG2TJ86w4w8aZ1xg+SrQAm4S9Whnm88ePfoOOXDJQoTxd/7K7Efae9zM03UC3Oj6UCdgqu7N3NDRXldc3KlMMyCHPOLrlOaydRZ9re0bsMtAPtIGQ/fraos7TT8dHFXpmJZ9sOLjAy9FMEOv2e3Emuxcz+u0zJ+axPXESuxMhZ8w4z3GSkFZr3HmGmHBP6lvfxxJE3kt9nLv+XWKg7JgUU/Kzg8KmrLrNfvdPuhTuR6QS8efuxyCv37Dk/VqOqvqZVb1FWiXsqWSjIOjxGu5ZIKOdG0nxkSDLNGxgCsfzibmH6wB1WZyTLKlNXz9Q+0wPaU/AsM1vpbC0UyFvVETCb5HryBqRU2dRVNmCn8Fu0wLv1Az/Y9LF2mWOBO99Tgo1l6/yhGU31I586oaLo2+vmuJYuuBslh5Fhv5qe9hqVqlXTDMbTwLmWPUhvzf330H+qeXT0N0UT4wg/D4OVxFOjC545/ABjqnAUN8LGLDPVKN+4JLPtuuLkhnojRuOxGwOWbdV1G0r7FIVV3AEYr1X+Cpf/1yzHiHameaCoGNV3Go8QbsqoQfo83vczYlymeGQDatWlBy0ailTA5v6EJxSldtojYPFZZxKHTqlzs4Z5nc25w2j0ec+Ch7pFpBBWZu6Yt9o1hSMKjQsQjaxN5yZM4gEJxE5rBt+CxZgSIHGPUN5N6yvyQMfWQY3rHl76pF'
        ) 
    
    response = bedrock_runtime.invoke_agent(
        agentId = 'FPHXFKRCFK',
        agentAliasId = 'FTSCUD0BEI',
        sessionId = str(uuid.uuid4()), 
        inputText = json.dumps(data)
    )

    completion = response['completion']
    response_body = ""

    for events in completion:
        if "chunk" in events and "bytes" in events['chunk']:
            chunk_data = events['chunk']['bytes'].decode('utf-8')
            response_body += chunk_data

    return response_body

name = "sleung@mcbankny.com"
data = fetch_data_from_DB(name)

print("Data Received: ",len(data))

summarize_text = get_bedrock_response(data)

print(summarize_text)