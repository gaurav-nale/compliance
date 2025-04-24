# Step 1: Generate Embeddings and Upsert to Pinecone

# import pandas as pd
# from pinecone import Pinecone, ServerlessSpec
# import boto3
# import os
# import json

# # --- Configuration ---
# PINECONE_API_KEY = "pcsk_6ExSnE_7Myg4KD6Gp1jTYefUPZPvneo1ud4g3NmjZdLeLNcUa7RSo2agnh12eDdKktB83y"  # Replace with your API key
# PINECONE_ENVIRONMENT = "us-east-1"  # Replace with your environment
# PINECONE_INDEX_NAME = "compliance-custom"  # Choose a name for your index
# CSV_FILE_PATH = "1k-chunk.csv"  # Path to your CSV file
# EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"  # Example Bedrock embedding model
# EMBEDDING_DIMENSION = 1536  # Dimension of the Titan Embeddings model (adjust if using a different model)
# PINECONE_CLOUD = "aws"
# PINECONE_REGION = "us-east-1" 

# # --- Initialize Pinecone ---
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # --- Create Pinecone Index if it doesn't exist ---
# index_names_response = pc.list_indexes()
# if index_names_response and hasattr(index_names_response, 'indexes'):
#     existing_index = next((i for i in index_names_response.indexes if i.name == PINECONE_INDEX_NAME), None)
#     if existing_index and existing_index.dimension != EMBEDDING_DIMENSION:
#         print(f"Index '{PINECONE_INDEX_NAME}' exists with dimension {existing_index.dimension}, but expected {EMBEDDING_DIMENSION}. Deleting and recreating...")
#         pc.delete_index(PINECONE_INDEX_NAME)
#         existing_index = None

#     if not existing_index:
#         pc.create_index(
#             name=PINECONE_INDEX_NAME,
#             dimension=EMBEDDING_DIMENSION,
#             metric="cosine",
#             spec=ServerlessSpec(
#                 cloud=PINECONE_CLOUD,
#                 region=PINECONE_REGION
#             )
#         )

# index = pc.Index(PINECONE_INDEX_NAME)

# # --- Initialize Bedrock Client for Embeddings ---
# bedrock = boto3.client(
#     "bedrock-runtime", 
#     region_name="us-east-1",
#     aws_access_key_id='ASIA3FLD26ANEIHG235K', 
#     aws_secret_access_key='rqfJprjDimLFOZAQpSu7vLBa0Utep//mWplCxlcY',
#     aws_session_token = 'IQoJb3JpZ2luX2VjEHQaCXVzLWVhc3QtMSJGMEQCIFedRcygq5NzH1aQbmIl031C3k+zol3W9Yad4O0fckdZAiAvHxwoMfcwiRJSd8pdf+EHhBj5mT+CHQSt6vELuXXACir8Agjc//////////8BEAAaDDc2NzM5NzkxNjY5OCIMdJ4BSkZVoPRF+vcmKtACkOudER2x114Hs+qarS42g5olzIItsApnMsx39vGkt3g8FqM5lTAw96kXCzemDbMWWYToIZikMnj6U9c9FlOKPtG4HMLUVJGk4jHbXm7OCmIoEDjs6F5sxXisFSFa5JL+jmKxzqZqCI5+3tHNmOh3bp1T5x3sxxZes3Pj4URq8A2Mqk18MhWTHK/Amnb+f8GR59+PcyvriqaQ7/5zktwoq97VEH+RmgLjvyd9UOdhGuRvNDQNXU2mnFkkEuFtFt5Rs1u52Xf7RKOCj1BJcUyt5IRFVx6L0p7lBDG925Av9QYrInC1QKDmyVwhr9JGOKfJ5UzAZJq9P1CLXYC+yy2OHJ67i7oiW7TSLVJ3Pp8Kdg0N+HS7x6lCrLoAEBVe7svHtRQXIB/IecI+wyAFz26WBXCpZ8PfxkNAf1Lbw4+QdBPcq1sOVnF/JRxdOuGu+VWsMOCYtr8GOqgB2lqLZQr7S3bny23Ovfj3WE/10IV6Hrlh/sFcCoz29cwfKRmItjNicoPWWk6D7aH8PPku6oFq3xYDHDaP6Shy0xsFOEPHeagG7ZVpl3hbCoil3HOX6o6NKyDlBNG3vAOWuhmxBMZU/MhCqjtwudlg4t4u4qSEMVbeI3CHv37HuMugql8uJ0mAbf5iafLBKuuFFe1uSH7wj8Aw+8rpEUzRmoU7j7M98sB6'
#     )

# # --- Function to generate embeddings using Bedrock ---
# def generate_bedrock_embedding(text, model_id=EMBEDDING_MODEL_ID, dimension=EMBEDDING_DIMENSION):
#     body = {"inputText": text}
#     # Check if the model supports configuring the output dimension
#     # if model_id == "amazon.titan-embed-text-v1":
#     #     body["embeddingConfig"] = {"outputEmbeddingLength": dimension}
#     response = bedrock.invoke_model(
#         body=json.dumps(body),
#         modelId=model_id,
#         accept="application/json",
#         contentType="application/json",
#     )
#     response_body = json.loads(response.get("body").read())
#     embedding = response_body.get("embedding")
#     # if embedding and len(embedding) != EMBEDDING_DIMENSION:
#     #     print(f"Warning: Embedding model '{model_id}' returned dimension {len(embedding)}, expected {EMBEDDING_DIMENSION}.")
#     return embedding

# # --- Read CSV data ---
# df = pd.read_csv(CSV_FILE_PATH)

# # --- Process data, generate embeddings, and upsert to Pinecone ---
# batch_size = 100
# for i in range(0, len(df), batch_size):
    # batch = df.iloc[i : i + batch_size]
    # vectors_to_upsert = []
    # for _, row in batch.iterrows():
    #     # Adjust this based on your CSV structure to create a text representation
    #     text_parts = []
    #     for col, value in row.items():
    #         if pd.isna(value):
    #             text_parts.append("")
    #         else:
    #             text_parts.append(str(value))
    #     text_to_embed = " ".join(text_parts)

    #     embedding = generate_bedrock_embedding(text_to_embed)
    #     if embedding:
    #         vector_id = str(row.get('_id', f"doc-{i + _}")) # Ensure _id is a string or generate a string ID
    #         # Convert all metadata values to strings or None
    #         metadata = {}
    #         for col, value in row.items():
    #             if pd.isna(value):
    #                 metadata[col] = ""
    #             elif isinstance(value, (int, float, bool)):
    #                 metadata[col] = value
    #             else:
    #                 metadata[col] = str(value)
    #         vectors_to_upsert.append((vector_id, embedding, metadata))
#         else:
#             print(f"Warning: Skipping upsert for row {i + _} due to missing embedding.")

#     if vectors_to_upsert:
#         index.upsert(vectors=vectors_to_upsert)


#     if vectors_to_upsert:
#         index.upsert(vectors=vectors_to_upsert)

# print(f"Upserted {len(df)} vectors to Pinecone index '{PINECONE_INDEX_NAME}'.")

# # --- Optional: Get index statistics ---
# stats = index.describe_index_stats()
# print(f"Pinecone index stats: {stats}")

# Step 2: Query knowledge base

# import json
# import os
# from pinecone import Pinecone, ServerlessSpec
# import boto3

# # --- Environment Variables (to be set in Lambda configuration) ---
# PINECONE_API_KEY = "pcsk_6ExSnE_7Myg4KD6Gp1jTYefUPZPvneo1ud4g3NmjZdLeLNcUa7RSo2agnh12eDdKktB83y"
# PINECONE_ENVIRONMENT = "us-east-1"
# PINECONE_INDEX_NAME = "compliance-custom"
# EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"
# BEDROCK_REGION = "us-east-1"

# # --- Initialize Pinecone ---
# pinecone_client = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
# index = pinecone_client.Index(PINECONE_INDEX_NAME)

# # --- Initialize Bedrock Client ---
# bedrock = boto3.client(
#     "bedrock-runtime", 
#     region_name=BEDROCK_REGION,
#     aws_access_key_id='ASIA3FLD26ANMIADPF6L', 
#     aws_secret_access_key='4bzZ6d3MfyHmcMC8Icj0sHHDpNFBiubb7Egpo0AL',
#     aws_session_token = 'IQoJb3JpZ2luX2VjEI7//////////wEaCXVzLWVhc3QtMSJHMEUCIQDBMRo7Z01lT7fmXMgin0xe/tUdbEY5qj4uyrWKLZaacgIgRTuKHH8MMtfHV5OtVv89GI9UD1o0yLt85EZeUZHoS0sq/AII9///////////ARAAGgw3NjczOTc5MTY2OTgiDCdRsuDxMeUilUZE2yrQApevHNbBuTlyNhtnpWJm1li+Udpu4+qmvHrVGxR7Gz0+FvXQbRNVoi7g+0OucjLGj83aM97YabXJwEploY5hGjGRmm7RVL7nOBiibYsOmJ3D6lW+PnxXwRMtYBH1gwM9ZwwvWMIwyvyqK2Sj2c7JoHp4Fi6b5EyeFAbIgZ1x0+QcKMlPsRB7USj5Lo5PIO57uJ6wyXhVwSqFpWPse/vhi4zLM51jC0bTWBEX7BBcJW/kEaa5CjxfZ8yvd1Gg02VvlQsefvapD2c9Ruw2qowG0aIARBPAgc9tqH8OdL1HL0BRI+F+weWfgC5hdg9wJ8RoAIsaNbQvJ8J4qcD+PkNTiFtB6+EKW+FfqIya6m/Fbm9tb841RgPY/jbRLUNwu5kqvLzPrnwIZPlHqhGQWitm0P305YyP77WPR6v+HvbcShcR0ei7j3iQxhYOevLNVCj6EjCBhLy/BjqnAVKU9J/GMhAKjrarKXR9VYo5WueHVH6W02YjQHYfa9mDj8eOGMetLWXpGkQDSVCGhQzqJmQCjFd1xmAkpZT0olBaydcsM/4aartxYvRAFohMMIbs9POkUYvnbiKvXa8FLghYxUYWbfvHAnTR+vgVhVRxIQ+jNtD87AO6lgiEvbQ9IH2bcSk/GD3EnjiTA0B14UBv04AhcwpclWYLVqevOvHrrXJdrGHV'
# )

# # --- Function to generate embeddings using Bedrock ---
# def generate_bedrock_embedding(text, model_id=EMBEDDING_MODEL_ID):
#     response = bedrock.invoke_model(
#         body=f'{{"inputText": "{text}"}}',
#         modelId=model_id,
#         accept="application/json",
#         contentType="application/json",
#     )
#     response_body = json.loads(response.get("body").read())
#     return response_body.get("embedding")

# def lambda_handler(event):
#     try:
#         query = event.get("query")
#         if not query:
#             return {
#                 "documents": [],
#                 "metadata": {"error": "Missing 'query' in the event."},
#             }

#         # Generate embedding for the query
#         query_embedding = generate_bedrock_embedding(query)

#         # Query Pinecone index
#         results = index.query(
#             vector=query_embedding,
#             top_k=5,  # Adjust as needed
#             include_metadata=True,
#         )

#         # Format the results for Bedrock
#         documents = []
#         for match in results.matches:
#             documents.append({
#                 "content": json.dumps(match.metadata),  # Or format as needed
#                 "metadata": {"source": match.id},  # Example metadata
#             })

#         return {"documents": documents, "metadata": {}}

#     except Exception as e:
#         print(f"Error: {e}")
#         return {"documents": [], "metadata": {"error": str(e)}}
    
# event = {
#   "query": "Is the name Government of the Russian Federation present in knowledge base?"
# }

# output = lambda_handler(event)
# print(output)

# Step 3: Sync Lambda Function
# import pandas as pd
# from pinecone import Pinecone, ServerlessSpec
# import boto3
# import json
# import os

# # --- Environment Variables (to be set in Lambda configuration) ---
# PINECONE_API_KEY =  "pcsk_6ExSnE_7Myg4KD6Gp1jTYefUPZPvneo1ud4g3NmjZdLeLNcUa7RSo2agnh12eDdKktB83y"
# PINECONE_ENVIRONMENT = "us-east-1"
# PINECONE_INDEX_NAME = "compliance-custom"
# CSV_FILE_PATH = "1k-chunk.csv"
# EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"
# BEDROCK_REGION = "us-east-1"

# # --- Initialize Pinecone ---
# pinecone_client = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
# index = pinecone_client.Index(PINECONE_INDEX_NAME)

# # --- Initialize Bedrock Client ---
# bedrock = boto3.client(
#     "bedrock-runtime", 
#     region_name=BEDROCK_REGION,
#     aws_access_key_id='ASIA3FLD26ANMIADPF6L', 
#     aws_secret_access_key='4bzZ6d3MfyHmcMC8Icj0sHHDpNFBiubb7Egpo0AL',
#     aws_session_token = 'IQoJb3JpZ2luX2VjEI7//////////wEaCXVzLWVhc3QtMSJHMEUCIQDBMRo7Z01lT7fmXMgin0xe/tUdbEY5qj4uyrWKLZaacgIgRTuKHH8MMtfHV5OtVv89GI9UD1o0yLt85EZeUZHoS0sq/AII9///////////ARAAGgw3NjczOTc5MTY2OTgiDCdRsuDxMeUilUZE2yrQApevHNbBuTlyNhtnpWJm1li+Udpu4+qmvHrVGxR7Gz0+FvXQbRNVoi7g+0OucjLGj83aM97YabXJwEploY5hGjGRmm7RVL7nOBiibYsOmJ3D6lW+PnxXwRMtYBH1gwM9ZwwvWMIwyvyqK2Sj2c7JoHp4Fi6b5EyeFAbIgZ1x0+QcKMlPsRB7USj5Lo5PIO57uJ6wyXhVwSqFpWPse/vhi4zLM51jC0bTWBEX7BBcJW/kEaa5CjxfZ8yvd1Gg02VvlQsefvapD2c9Ruw2qowG0aIARBPAgc9tqH8OdL1HL0BRI+F+weWfgC5hdg9wJ8RoAIsaNbQvJ8J4qcD+PkNTiFtB6+EKW+FfqIya6m/Fbm9tb841RgPY/jbRLUNwu5kqvLzPrnwIZPlHqhGQWitm0P305YyP77WPR6v+HvbcShcR0ei7j3iQxhYOevLNVCj6EjCBhLy/BjqnAVKU9J/GMhAKjrarKXR9VYo5WueHVH6W02YjQHYfa9mDj8eOGMetLWXpGkQDSVCGhQzqJmQCjFd1xmAkpZT0olBaydcsM/4aartxYvRAFohMMIbs9POkUYvnbiKvXa8FLghYxUYWbfvHAnTR+vgVhVRxIQ+jNtD87AO6lgiEvbQ9IH2bcSk/GD3EnjiTA0B14UBv04AhcwpclWYLVqevOvHrrXJdrGHV'
# )

# # --- Function to generate embeddings using Bedrock ---
# def generate_bedrock_embedding(text, model_id=EMBEDDING_MODEL_ID):
#     body = json.dumps({"inputText": text})
#     response = bedrock.invoke_model(
#         body=body,
#         modelId=model_id,
#         accept="application/json",
#         contentType="application/json",
#     )
#     response_body = json.loads(response.get("body").read())
#     return response_body.get("embedding")

# def lambda_handler():
#     try:
#         # --- Read CSV data ---
#         df = pd.read_csv(CSV_FILE_PATH)

#         # --- Process data, generate embeddings, and upsert to Pinecone ---
#         batch_size = 100
#         for i in range(0, len(df), batch_size):
#             batch = df.iloc[i : i + batch_size]
#             vectors_to_upsert = []
#             for _, row in batch.iterrows():
#                 text_to_embed = " ".join(row.astype(str).tolist())
#                 embedding = generate_bedrock_embedding(text_to_embed)
#                 vector_id = f"doc-{i + _}"
#                 metadata = {}
#                 for col, value in row.items():
#                     if pd.isna(value):
#                         metadata[col] = ""  # Convert NaN to an empty string
#                     elif isinstance(value, (int, float, bool)):
#                         metadata[col] = value
#                     else:
#                         metadata[col] = str(value)
#                 vectors_to_upsert.append((vector_id, embedding, metadata))

#             if vectors_to_upsert:
#                 index.upsert(vectors=vectors_to_upsert)

#         print(f"Successfully synced {len(df)} vectors to Pinecone index '{PINECONE_INDEX_NAME}'.")
#         return {"statusCode": 200, "body": json.dumps("Sync successful!")}

#     except Exception as e:
#         print(f"Error during sync: {e}")
#         return {"statusCode": 500, "body": json.dumps(f"Sync failed: {str(e)}")}
    

# lambda_handler()

# import boto3
# import uuid
# import json

# bedrock_client = boto3.client(
#     service_name = "bedrock-agent-runtime",
#     region_name = "us-east-2",
#     aws_access_key_id='ASIA3FLD26ANJZCBAPQC', 
#     aws_secret_access_key='t2BGIXrD5TCfbJ2KUhI67YXOUd4otOnrtqgczXwW',
#     aws_session_token = 'IQoJb3JpZ2luX2VjEJ///////////wEaCXVzLWVhc3QtMSJGMEQCIF1Q+w/Ou8R1Bg+2Qs2mbfbefMDU/dAPkMUSeF2eJB+IAiBhT6fQuPlDQ09CuJGattT6D+WqfQ/imAs1tGVgHAt26yr8AgjX//////////8BEAAaDDc2NzM5NzkxNjY5OCIMdAAXCJr22YwujxFaKtAC3wxW61mO4v2pUp+dELMne5mwgHK4Zs+qYL6F3bBcczS2Fjc/1z/I090b3jvvI6QvQM/BrI6+rCqlkH8qa/DU3VYnE5m64gx4ffAb/zeb95RB93PrwPY55xEIuSP+uTm1EYqueNjFDnhWYTC1wSMTcDvf5SBxbuUPujQzUQjsRUwm1TTsi8kFcDgvaevgG/bQa+7hI1A9zXp3hfrNetAJ+TKCe7i06J+tJzL0YmxZLR8L/Vb3DTkQOtdLinSfIZMvXD2bCo/BF4FlcBfoh2nDqoKr1rkhK7q8W0D44iB8G1Xptki50BgCIxCDEYGXPLXLlSk49O+0NZjlflbGRBCe6cxBuMkQDVXDi0C66YENOyr5rgq18dlk0bpE7FmQqHUIwztdpAgsQ4bZuklem9U5sTpkSDMBUMJLbUYNR933blfUPbLEPrYVytSRCXRm2q8fMMPylr4GOqgBhVlgGao/8ePV+j7ivyr2Nq4uQwfbpTSAZW+8/Jro+aUBlBDjtx5PpkfEorJSUZorX/54yuuQ3pTpnHuDLnIgPQVuXBxL+nyBERMd22akHeP41byrVjS4stNQ1GTC8IcR/falPAMqhOrw8G7Y3veGqozicbfxvTLI8fkJWMQb3kQWTxM/1B/HTb+QgA1mJzB4PgiCfD5afvYK0fEPloEfMxzS4XR6adLM'
# )

# bedrock_agent_info = boto3.client(
#     service_name = "bedrock-agent",
#     region_name = "us-east-2",
#     aws_access_key_id='ASIA3FLD26ANM7EV2P6B', 
#     aws_secret_access_key='RxWT3ATzJ8Kz4HLe1vAWG26PK5GR2KWaqCh2Xzok',
#     aws_session_token = 'IQoJb3JpZ2luX2VjEP///////////wEaCXVzLWVhc3QtMSJGMEQCIG5ECb8tXGjmZzHaNcYQm1P2WnZmLk9101ITnadfGFIdAiADzzPZIwSzALsxMPl8R1+p3e1nolLFk4lBPNjMpQBKJSrzAghHEAAaDDc2NzM5NzkxNjY5OCIM58qr/cROe3qk9XoqKtAC16/S2rwUCzo8mC3xoPMi93IagfHe9ZvPzpxK0bKd1NO9/G+he5cluAGTGf72yAXk1aErrwU663FjVyFA6Nds8OhpgraBrwkN+s1ThZf5c3DkYuxyO4nj9Q2hdoHSHt4a4julNVrsm3bTCIFv5EjAwNtkdY3NVibmSo+LEvcBOiOE+wcTHI9cK3RcO8V2myI28PBc3MQ8Sipq99fC+UUq8b8sh7ZqigG5DLSTWpsMDYNxtqBlMkLuWRllp9Gkp9xCL+dqIFxKkBjclMlnJ/jbXndQ9t5Hj6mjAOb3EcDSr+WJYDuIYNMUpdGmH9GUYZbwK/iGHXPd/Mx/oR9ASvwu1WQXcbqCduNsLhb+zAMR++fCzUrbMqCRK/u/u8/NcqoZR7LIjctYgurXpF0Ot/v8QwmB7+ZN+H/yNwJXyx+6jIr0jkf4JDSVFPUJd1ND1ci2MOn+q74GOqgB8edPeO6Q6DQi7y045OEDiCnpsNr2N5wLzQUFPhTAoegOE1tP+ZCBa93YqS1m2Vrp+8Zjk8itx/GXk5kkfOLWjNQWBnGT0kv0aLxq08o7KS/ivrfN/bd4FoUkYcp+xl6l2+Mj0lU0QcjIwCgnqH1rVfr1aU/i4Uf2rWfZ+KD6u9F+QlRQyhpkjW24MuWD7EoHvaCC0pYmrOY7DGJEn9KazNfQ18EGV+sm'
# )

# SESSION_ID = str(uuid.uuid4())

# inputText = "Ismail Abdul Haniya"

# try:
#     agent_config = bedrock_agent_info.get_agent(agentId = "5B230UJQCQ")

#     base_instructions = agent_config["agent"]["instruction"]
    
#     extra_instructions = "You need to answer strictly in French or Spanish"

#     combined_instructions = f"{base_instructions}\n{extra_instructions}"

#     update_response = bedrock_agent_info.update_agent(
#         agentId = "5B230UJQCQ",
#         agentName = 'agent-compliance-poc',
#         agentResourceRoleArn = 'arn:aws:bedrock:us-east-2:767397916698:agent/5B230UJQCQ',
#         foundationModel = 'anthropic.claude-3-5-haiku-20241022-v1:0',
#         instruction = combined_instructions
#     )

#     print(update_response)

# except Exception as e:
#     print("Error invoking the agent: ",e)


# import csv
# import json

# # Input and output file paths
# csv_file_path = "test.csv"       # Update with your CSV file name
# jsonl_output_path = "test.jsonl" # Output path for JSONL

# # The field from the CSV that should be used as the main text content
# content_field = "name"

# # Fields to include as metadata (all others except content)
# metadata_fields = [
#     "source", "entity_number", "type", "programs", "title", "addresses",
#     "federal_register_notice", "start_date", "end_date", "standard_order",
#     "license_requirement", "license_policy", "call_sign", "vessel_type",
#     "gross_tonnage", "gross_registered_tonnage", "vessel_flag",
#     "vessel_owner", "remarks", "source_list_url", "alt_names", "citizenships",
#     "dates_of_birth", "nationalities", "places_of_birth",
#     "source_information_url", "ids"
# ]

# # Convert CSV to JSONL
# with open(csv_file_path, mode="r", encoding="utf-8") as csv_file, \
#      open(jsonl_output_path, mode="w", encoding="utf-8") as jsonl_file:
    
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         text_content = row.get(content_field, "").strip()
#         metadata = {key: row.get(key, "").strip() for key in metadata_fields if row.get(key)}

#         json_object = {
#             "name": text_content,
#             "metadata": metadata
#         }

#         jsonl_file.write(json.dumps(json_object) + "\n")

# print(f"✅ Conversion complete: {jsonl_output_path}")


import json
import csv
import random

# Paths
input_file = 'test.jsonl'  # Replace with your actual .jsonl file path
output_file = 'random.csv'

# Read all lines from the JSONL file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Parse JSON objects
data = [json.loads(line) for line in lines]

# Randomly sample 1000 items (or fewer if the file has less than 1000)
sampled_data = random.sample(data, min(1000, len(data)))

# Write to CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name'])  # CSV header
    for item in sampled_data:
        writer.writerow([item.get('name', '')])

print(f"Sampled {len(sampled_data)} names and saved to {output_file}")
