import boto3
import csv
import pandas as pd
import json

def process_names_with_bedrock(csv_file_path, knowledge_base_id, output_excel_path):

    bedrock_runtime = boto3.client(
            service_name = "bedrock-agent-runtime",
            region_name = "us-east-2",
            aws_access_key_id='ASIA3FLD26ANKO34QVEH', 
            aws_secret_access_key='QsBpUMWk8VP7fBFagQrsknmJgFjXuHA7RKLWDvyk',
            aws_session_token = 'IQoJb3JpZ2luX2VjEEoaCXVzLWVhc3QtMSJGMEQCICntC3q1k43IorvojMbErjVWWSGzkn34AGOCHDBG41OuAiAnQFdGEvhXivnB0PpfsW5+joDu1qBiZ2cknHAv7RzFWyr8AgjD//////////8BEAAaDDc2NzM5NzkxNjY5OCIMwL1DmAlFMW5Y8HM4KtAC1EB2dOD9XmOmEZ4kYdfje6Uh0w7KCTUlG1QDQe89uJEUqWHCWUVbD4myfmYtuJQVY3PUGMY4MGBjEHLNbGrJt4V8bJVgqZLE67+ZrU6B7BYbU7S39bHjzLrSb8ZuiSRDrVvWrFLw9eCgqp/aUvl6hX4ce3iZqjZgrxKeqf7vbkZkoQfbaBhCKH5/JVw8aH5G09HhXQMhhlbEMDkTKGosLYOOR38TaV+PRBCuusSn0HJIxwIIO+ZzLA2883oSRosCSeZpx2RgVTmd+DN72mdDlVzocPqLd+TdfWS6/LtJvirUFl3lfzsLDhd5uqMSXZ7Cm9Fw3M+x6jLsLvZMyFv5MIzSDQUdw0Dts+o60GoDi7Civ8e+w67Y3UBahVMUfEex2fBuVvHctCRTOm9aEvVclyAx//KkuvKeNOPTIZgOJm+ZosCCsY/TeAnCiE+GVuslMNyo5b8GOqgBpYjVd3I/kyZBF9BtAqN3tBDR6y++3iwrsPVMJE8XtUmqFuNACN+7OIG+feu+LYcN6oSfkvtDZlHNYOOifp+0gtXnOM7Pds77oDw34ePmZnPg6wMih6fZlff8qZqKr/ChW4iOD14yGpSrkhZrVqsfWJ6akpzsT797HwaKOEjw4mC/mMjXOXB/k6goKWBwB0L7aE8kzeC9pxt9n47//YcR6noni+4R/8y1'
        )

    results = []
    row_counter = 1

    try:
      with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
              name = row.get('name')

              if name:
                  try:
                      input = f"Is {name} present in knowledge base?"
                      response = bedrock_runtime.retrieve_and_generate(
                            input = {
                                "text" : input
                            },
                            retrieveAndGenerateConfiguration = {
                                "type" : "KNOWLEDGE_BASE",
                                "knowledgeBaseConfiguration" : {
                                    "knowledgeBaseId" : knowledge_base_id,
                                    "modelArn" : "meta.llama3-3-70b-instruct-v1:0"
                                }
                            }
                        )
                      
                    #   response_body = json.loads(response['body'].read().decode('utf-8'))
                      citations = response['citations']
                      response_text = citations[0]['generatedResponsePart']['textResponsePart']['text']

                      print("Logging for row - ", row_counter)

                      results.append({
                          'Id': row_counter,
                          'Name': name,
                          'Description': response_text
                      })
              
                  except Exception as bedrock_err:
                      print(f"Error querying Bedrock for name '{name}': {bedrock_err}")
                      results.append({
                          'Id': row_counter,
                          'Name': name,
                          'Description': f"Bedrock Query Failed: {bedrock_err}"
                      })

                  row_counter+=1
              
            #   if row_counter > 1:
            #       break
              


    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return

    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)
    print(f"Results saved to {output_excel_path}")

csv_file = 'random.csv'  
knowledge_base_id = 'ATL1AK6PSO'  
excel_output = 'bedrock_results.xlsx' 

process_names_with_bedrock(csv_file, knowledge_base_id, excel_output)
