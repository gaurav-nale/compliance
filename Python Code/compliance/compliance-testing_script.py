# import pandas as pd
# import json
# import asyncio
# import aiohttp
# from aiohttp import ClientSession
# import random

# API_URL = "http://127.0.0.1:5000/call_api"
# EXCEL_PATH = "testcases.xlsx"
# INPUT_COLUMN = "Input"
# OUTPUT_COLUMN = "Output-AI"
# ID_COLUMN = "ID"
# BATCH_SIZE = 5  # Parallel requests per batch

# MAX_RETRIES = 3
# INITIAL_DELAY_SECONDS = 1.0 

# def create_bedrock_input(row):
#     items = [{
#         "type": row.get("type", " "),
#         "name": row.get("name", " "),
#         "address1": row.get("address", " "),
#         "city": row.get("city", " "),
#         "state": row.get("state", " "),
#         "country": row.get("country", " "),
#         "countryCode":row.get("countryCode"," "),
#         "zipCode":row.get("zipCode"," "),
#         "skipScanning": "no"
#     }]
#     return json.dumps({"items": items})

# # Send a single request
# async def send_request(session: ClientSession, id_value, input_value):
#     # try:
#     #     print(f"🔄 Sending request for ID: {id_value}")
#     #     payload = {"items": input_value}
#     #     headers = {"Content-Type": "application/json"}

#     #     async with session.post(API_URL, json=payload, headers=headers) as resp:
#     #         resp.raise_for_status()
#     #         result = await resp.json()
#     #         print(f"✅ Success for ID: {id_value}")
#     #         return id_value, json.dumps(result, indent=1)
#     # except Exception as e:
#     #     print(f"Error for ID: {id_value} - {str(e)}")
#     #     return id_value, f"Error: {str(e)}"
    
#     payload = {"items": input_value}
#     headers = {"Content-Type": "application/json"}

#     for attempt in range(MAX_RETRIES + 1):
#         try:
#             print(f"🔄 Attempt {attempt + 1}/{MAX_RETRIES + 1} - Sending request for ID: {id_value}")
#             async with session.post(API_URL, json=payload, headers=headers, timeout=30) as resp:

#                 if resp.status == 500 or resp.status == 504:
#                     if attempt < MAX_RETRIES:
#                         delay = INITIAL_DELAY_SECONDS * (2 ** attempt)
#                         sleep_time = delay + random.uniform(0, delay * 0.1)

#                         print(f"⚠️ Received API Gateway Timeout Error for ID: {id_value}. Attempt {attempt + 1}. Retrying in {sleep_time:.2f} seconds...")
#                         await asyncio.sleep(sleep_time)
#                         continue
#                     else:
#                         print(f"Max retries ({MAX_RETRIES}) reached for ID: {id_value} after 503: API Gateway Timeout error.")
#                         return id_value, f"Error: Max retries exceeded after 503 status"

#                 resp.raise_for_status()

#                 result = await resp.json()
#                 print(f"✅ Success for ID: {id_value} on attempt {attempt + 1}")
#                 return id_value, json.dumps(result, indent=1)

#         except aiohttp.ClientResponseError as e:
#             print(f"HTTP Error for ID: {id_value} (Status: {e.status}) - {e.message}. No retry attempted.")
#             return id_value, f"Error: HTTP {e.status} - {e.message}"
#         except asyncio.TimeoutError:
#             print(f"Timeout Error for ID: {id_value} on attempt {attempt + 1}. No retry attempted.")
#             return id_value, "Error: Request Timeout"
#         except aiohttp.ClientConnectionError as e:
#             print(f"Connection Error for ID: {id_value} on attempt {attempt + 1} - {str(e)}. No retry attempted.")
#             return id_value, f"Error: Connection Error - {str(e)}"
#         except Exception as e:
#             print(f"Unexpected Error for ID: {id_value} on attempt {attempt + 1} - {type(e).__name__}: {str(e)}. No retry attempted.")
#             return id_value, f"Error: Unexpected - {type(e).__name__}: {str(e)}"

#     print(f"Failed for ID: {id_value} after all attempts, reason unclear.")
#     return id_value, f"Error: Failed after {MAX_RETRIES + 1} attempts, final state unknown."

# # Process one batch at a time
# async def process_in_batches(data_tuples):
#     results = {}
#     async with aiohttp.ClientSession() as session:
#         total = len(data_tuples)
#         for i in range(0, total, BATCH_SIZE):
#             batch = data_tuples[i:i+BATCH_SIZE]
#             batch_ids = [id_ for id_, _ in batch]
#             print(f"\n🚀 Starting batch {i//BATCH_SIZE + 1} (IDs: {batch_ids})")
#             tasks = [send_request(session, id_, input_val) for id_, input_val in batch]
#             responses = await asyncio.gather(*tasks)
#             for id_, result in responses:
#                 results[id_] = result
#             print(f"✅ Finished batch {i//BATCH_SIZE + 1}")
#     return results

# def process_excel(filepath):
#     try:
#         df = pd.read_excel(filepath)

#         # Ensure required columns
#         if ID_COLUMN not in df.columns or INPUT_COLUMN not in df.columns or OUTPUT_COLUMN not in df.columns:
#             print("ERROR: Excel file must have columns: ID, Input, Output-AI")
#             return

#         df[OUTPUT_COLUMN] = df[OUTPUT_COLUMN].astype(object)

#         data = []
#         for index, row in df.iterrows():
#             id_val = row[ID_COLUMN]
#             output_val = row[OUTPUT_COLUMN]

#             # Skip already processed rows
#             if pd.notna(output_val):
#                 print(f"⏩ Skipping already processed ID: {id_val}")
#                 continue

#             input_val = row[INPUT_COLUMN]
#             data.append((id_val, input_val))

#             # if id_val > 41:
#             #     break

#         if not data:
#             print("✅ All rows already processed. Nothing to do.")
#             return

#         print(f"\nTotal IDs to process: {len(data)}")
#         results = asyncio.run(process_in_batches(data))

#         # Update DataFrame with results
#         for id_val, result in results.items():
#             df.loc[df[ID_COLUMN] == id_val, OUTPUT_COLUMN] = result

#         # Save to Excel
#         df.to_excel(filepath, index=False)
#         print(f"\n✅ Done. Results written to: {filepath}")

#     except FileNotFoundError:
#         print("File not found:", filepath)
#     except Exception as e:
#         print("Error:", str(e))

# if __name__ == "__main__":
#     process_excel(EXCEL_PATH)


# Testing for Tej Data
import pandas as pd

import json
import asyncio
import aiohttp
from aiohttp import ClientSession

API_URL = "http://127.0.0.1:5000/call_api"
EXCEL_PATH = "TestData_202504021057_1.csv"
# High-Risk Countries
# EXCEL_PATH = "high risk countries.csv"
OUTPUT_COLUMN = "Score-Bedrock-12"
ID_COLUMN = "ID"
BATCH_SIZE = 10  
RESULT_EXCEL_PATH = "TestData_Results_Bedrock.xlsx"

def create_bedrock_input(row):
    """Creates the input format for Bedrock based on the CSV row."""
    items = [{
        "type": row.get("type", " "),
        "name": row.get("name", " "),
        "address1": row.get("address", " "),
        "city": row.get("city", " "),
        "state": row.get("state", " "),
        "country": row.get("country", " "),
        "countryCode":row.get("countryCode"," "),
        "zipCode":row.get("zipCode"," "),
        "skipScanning": "no"
    }]
    return json.dumps({"items": items})

# Send a single request
async def send_request(session: ClientSession, id_value, input_value):
    try:
        print(f"🔄 Sending request for ID: {id_value}")
        payload = {"items": input_value}
        headers = {"Content-Type": "application/json"}

        async with session.post(API_URL, json=payload, headers=headers) as resp:
            resp.raise_for_status()

            try:
                result_json = await resp.json(content_type=None)
            except Exception as e:
                text_resp = await resp.text()
                print(f"❌ ID: {id_value} - JSON parse error. Raw: {text_resp}")
                return id_value, (f"JSON Error: {str(e)}", None)

            # ✅ Handle if it's a dict
            if isinstance(result_json, dict):
                score = result_json.get("body", {}).get("body", {}).get("Response", {}).get("score", None)
                print(f"✅ ID: {id_value} - Score: {score}")
                return id_value, (score if score is not None else "No score", result_json)

            # ✅ Handle if it's a list
            elif isinstance(result_json, list):
                if result_json and isinstance(result_json[0], dict) and "score" in result_json[0]:
                    score = result_json[0]["score"]
                    print(f"✅ ID: {id_value} - Score (from list): {score}")
                    return id_value, (score, result_json)
                else:
                    print(f"⚠️ ID: {id_value} - List without score. Data: {result_json}")
                    return id_value, ("Score not found in list", result_json)

            # ⚠️ If it's a string or anything else
            elif isinstance(result_json, str):
                print(f"⚠️ ID: {id_value} - Got string response: {result_json}")
                return id_value, (f"String response: {result_json}", result_json)

            else:
                print(f"⚠️ ID: {id_value} - Unexpected response type: {type(result_json)}")
                return id_value, ("Unexpected type", result_json)
            
    except Exception as e:
        print(f"Error for ID: {id_value} - {str(e)}")
        return id_value, (f"Error: {str(e)}", None)

# Process one batch at a time
async def process_in_batches(data_tuples):
    results = {}
    async with aiohttp.ClientSession() as session:
        total = len(data_tuples)
        for i in range(0, total, BATCH_SIZE):
            batch = data_tuples[i:i+BATCH_SIZE]
            batch_ids = [id_ for id_, _ in batch]
            print(f"\n🚀 Starting batch {i//BATCH_SIZE + 1} (IDs: {batch_ids})")
            tasks = [send_request(session, id_, input_val) for id_, input_val in batch]
            responses = await asyncio.gather(*tasks)
            for id_, result in responses:
                results[id_] = result
            print(f"✅ Finished batch {i//BATCH_SIZE + 1}")
    return results

def process_excel(filepath):
    try:
        df = pd.read_csv(filepath)

        if ID_COLUMN not in df.columns:
            df.insert(0, ID_COLUMN, range(1, len(df) + 1))  # Add ID column if missing

        if OUTPUT_COLUMN not in df.columns:
            df[OUTPUT_COLUMN] = None

        df[OUTPUT_COLUMN] = df[OUTPUT_COLUMN].astype(object)

        data = []
        for index, row in df.iterrows():
            id_val = row[ID_COLUMN]
            output_val = row[OUTPUT_COLUMN]

            if pd.notna(output_val):
                print(f"⏩ Skipping already processed ID: {id_val}")
                continue

            input_val = create_bedrock_input(row)
            data.append((id_val, input_val))

        if not data:
            print("✅ All rows already processed. Nothing to do.")
            return

        print(f"\n🧠 Total IDs to process: {len(data)}")
        results = asyncio.run(process_in_batches(data))

        score_map = {}
        json_rows = []

        for id_val, (score, full_json) in results.items():
            score_map[id_val] = score
            json_rows.append({
                ID_COLUMN: id_val,
                "Response_JSON": json.dumps(full_json, indent=2) if full_json else "None"
            })

        for id_val, score in score_map.items():
            df.loc[df[ID_COLUMN] == id_val, OUTPUT_COLUMN] = score

        df.to_csv(filepath, index=False)
        print(f"✅ Scores updated in CSV: {filepath}")

        json_df = pd.DataFrame(json_rows)
        json_df.to_excel(RESULT_EXCEL_PATH, index=False)
        print(f"📁 Full JSON responses saved to Excel: {RESULT_EXCEL_PATH}")

    except FileNotFoundError:
        print("❌ File not found:", filepath)
    except Exception as e:
        print("❌ Error:", str(e))

if __name__ == "__main__":
    process_excel(EXCEL_PATH)
