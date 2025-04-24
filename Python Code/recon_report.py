# import json
# import boto3
# import pandas as pd
# import hashlib
# from io import BytesIO
# from datetime import datetime
# from rapidfuzz import fuzz
# import time
# import logging
# import requests
# import xlsxwriter
 
# # --- Logging Setup ---
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
 
# # --- Configuration ---
# OLD_CSV_BUCKET = 'previous-sdn-csv'
# OLD_CSV_KEY = 'sdn-kb-data/main.csv'
# NEW_CSV_BUCKET = 'new-sdn-csv'
# NEW_CSV_KEY = 'main_1.csv'
# REPORT_BUCKET = 'sdn-report'
# REPORT_KEY = f'sdn-diff-report-{datetime.now().strftime("%Y%m%d")}.xlsx'
 
# KB_ID = 'POKSUWTLBW'
# DATASOURCE_ID = 'YFH0BJ9HRJ'
 
# AWS_ACCESS_KEY = 'ASIA3FLD26ANCWULFAVY'
# AWS_SECRET_KEY = 'UoWUAsMrJoXVZPrsL0/p46tS0xwby2MYLJE7IDY/'
# AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJHMEUCIBlGMIXH9+Znpd0qNiPC4x28py4XRMMR+A6YmheOLveuAiEA023Rh1z3yojaotCW3etNX+LTwe/AJCcblKZCHOCYtdUqggMIfRAAGgw3NjczOTc5MTY2OTgiDEZ/nJa9yK6Ti16jEyrfAv1Oq5FbIr9phsFSSz6JA/+Et9Jsn63Kw+C/i3MOzEtO8YXg+Sc8a1yCl1LZGEuR3a8KlnlBfTTpilkzcw2WmOTlpm24WE0FCpMOdEIZCrJExGI9UDiN09R5LS9MRIWIoyoJRC+WTQtdD8fphqAtlZaYrkS0AJDfWFnd0P5F0nVZsvnFS6jKAyHYcYHQTFwckvi6rp0B+UpdxwMiderIXx80Z550JJQ4WDzDL8ehcMvm4tK1wdVDZSH1CqCiPskr8TcUwsko/2gXfshl9M20+ZwY45hzg+vKNDGD6m4DjjNOZ2kaetm1C7W1dP8cvlDMQphvJaqER+HxVPZV5NrrkKoxdXDAez9+iCsEWe+lMOoIXKmCNPN+SQ8kFPmfkpIki5xKDOBhk9jmuDS/xk5dncQpoAcfFW87UUIsMZ4sr0h8/vzSivJQcK4BPF85t9Ki6k8uGyl8wGR19mN4gx/zXjDXida/BjqmAaGQDRrqE/YcqrKr3N8STyIkShfIYyeCR1kDb6ue2A/K3xB9l44dVoCJy0cmodR5Yk86gW7YRbKvYRisC0fuL8JhY1dtkKHP76Ov2c8IAeHYHLkcvhoJiDOJbuuVWuCF59vcRK3zAU32riERWAWn9KE0wqZP1N2SdWUxQkSednviRq41cAX6XelJNuYO8y8O7OYfwZXODQ5OomCMu4CMKDfmCduZuX0='
 
# API_URL = "https://g9z9wv5is3.execute-api.us-east-2.amazonaws.com/dev/test-knowledge-base"
 
# def get_s3_client():
#     return boto3.client(
#         's3',
#         aws_access_key_id=AWS_ACCESS_KEY,
#         aws_secret_access_key=AWS_SECRET_KEY,
#         aws_session_token=AWS_SESSION_TOKEN,
#         region_name='us-east-2'
#     )
 
# def get_bedrock_client():
#     return boto3.client('bedrock-agent',
#                         aws_access_key_id=AWS_ACCESS_KEY,
#                         aws_secret_access_key=AWS_SECRET_KEY,
#                         aws_session_token=AWS_SESSION_TOKEN,
#                         region_name='us-east-2')
 
# def download_csv_from_s3(bucket, key):
#     s3 = get_s3_client()
#     obj = s3.get_object(Bucket=bucket, Key=key)
#     return pd.read_csv(obj['Body'])
 
# def hash_row(row):
#     row_str = '|'.join([str(v).strip().lower() for v in row.fillna('').values])
#     return hashlib.md5(row_str.encode()).hexdigest()
 
# def get_hashed_dataframe(df):
#     df_copy = df.copy()
#     df_copy['row_hash'] = df_copy.apply(hash_row, axis=1)
#     return df_copy
 
# def fuzzy_match_row(target_row, candidate_df, threshold=90):
#     best_score, best_match, best_idx = 0, None, None
#     columns = [c for c in target_row.index if c != 'row_hash']
#     target_str = '|'.join([str(v).strip().lower() for v in target_row[columns].fillna('')])
 
#     for idx, row in candidate_df.iterrows():
#         candidate_str = '|'.join([str(v).strip().lower() for v in row[columns].fillna('')])
#         score = fuzz.token_sort_ratio(target_str, candidate_str)
#         if score > best_score:
#             best_score, best_match, best_idx = score, row, idx
#     return (best_score, best_match, best_idx) if best_score >= threshold else (0, None, None)
 
# def compare_dataframes_with_fuzzy(old_df, new_df):
#     old_hashed = get_hashed_dataframe(old_df)
#     new_hashed = get_hashed_dataframe(new_df)
 
#     old_hashes = set(old_hashed['row_hash'])
#     new_hashes = set(new_hashed['row_hash'])
 
#     exact_added = new_hashed[~new_hashed['row_hash'].isin(old_hashes)]
#     exact_deleted = old_hashed[~old_hashed['row_hash'].isin(new_hashes)]
 
#     updated_records = []
#     confirmed_added = exact_added.copy()
#     confirmed_deleted = []
 
#     for idx, del_row in exact_deleted.iterrows():
#         score, match_row, match_idx = fuzzy_match_row(del_row, confirmed_added)
#         if match_row is not None:
#             updated_records.append(match_row)
#             confirmed_added = confirmed_added.drop(match_idx)
#         else:
#             confirmed_deleted.append(del_row)
 
#     updated_df = pd.DataFrame(updated_records)
#     deleted_df = pd.DataFrame(confirmed_deleted)
 
#     return confirmed_added, updated_df, deleted_df
 
# def replace_old_data_file():
#     s3 = get_s3_client()
#     try:
#         s3.head_object(Bucket=OLD_CSV_BUCKET, Key=OLD_CSV_KEY)
#         s3.delete_object(Bucket=OLD_CSV_BUCKET, Key=OLD_CSV_KEY)
#     except s3.exceptions.ClientError as e:
#         if e.response['Error']['Code'] != '404':
#             raise
#     s3.copy_object(Bucket=OLD_CSV_BUCKET, Key=OLD_CSV_KEY,
#                    CopySource={'Bucket': NEW_CSV_BUCKET, 'Key': NEW_CSV_KEY})
 
# def trigger_kb_sync():
#     client = get_bedrock_client()
#     response = client.start_ingestion_job(
#         knowledgeBaseId=KB_ID,
#         dataSourceId=DATASOURCE_ID
#     )
#     return response['ingestionJob']['ingestionJobId']
 
# def wait_for_ingestion_job(ingestion_id, max_wait_time=1200, check_interval=60):
#     client = get_bedrock_client()
#     start = time.time()
#     while time.time() - start < max_wait_time:
#         response = client.get_ingestion_job(
#             knowledgeBaseId=KB_ID,
#             dataSourceId=DATASOURCE_ID,
#             ingestionJobId=ingestion_id
#         )
#         status = response['ingestionJob']['status']
#         if status == 'COMPLETE':
#             return True
#         elif status in ['FAILED', 'STOPPED']:
#             return False
#         time.sleep(check_interval)
#     return False
 
# def check_kb_via_api(df):
#     kb_status = []
#     for _, row in df.iterrows():
#         name = row.get('name', '').strip()
#         if not name:
#             kb_status.append('No')
#             continue
#         try:
#             response = requests.post(API_URL, json={"name": name})
#             if response.status_code == 200:
#                 result = response.json()
#                 body = result.get('body', {})
#                 if isinstance(body, str):
#                     body = json.loads(body)
#                 found = body.get('found', False)
#                 kb_status.append('Yes' if found else 'No')
#             else:
#                 kb_status.append('No')
#         except Exception as e:
#             logger.error(f"Error querying KB API for '{name}': {e}")
#             kb_status.append('No')
#     df['Synced with KB'] = kb_status
#     return df
 
# def generate_report(added, updated, deleted, new_df):
#     summary = []
#     detail_rows = []
#     date = datetime.now().strftime('%Y-%m-%d')
 
#     def add_detail_rows(df, status):
#         return [{
#             'Program': row.get('programs', 'UNKNOWN'),
#             'Name': row.get('name', ''),
#             'Address': row.get('addresses', ''),
#             'Created Date': date,
#             'Status': status,
#             'Synced with KB': row.get('Synced with KB', 'No')
#         } for _, row in df.iterrows()]
 
#     detail_rows.extend(add_detail_rows(added, 'Created'))
#     detail_rows.extend(add_detail_rows(updated, 'Updated'))
#     detail_rows.extend(add_detail_rows(deleted, 'Deleted'))
 
#     all_programs = pd.concat([added, updated, deleted], ignore_index=True)['programs'].dropna().unique()
#     for program in all_programs:
#         added_count = len(added[added['programs'] == program]) if not added.empty else 0
#         updated_count = len(updated[updated['programs'] == program]) if not updated.empty else 0
#         deleted_count = len(deleted[deleted['programs'] == program]) if not deleted.empty else 0
 
#         sync_check_df = pd.concat([added, updated, deleted], ignore_index=True)
#         program_syncs = sync_check_df[sync_check_df['programs'] == program]['Synced with KB']
#         sync_status = 'Yes' if 'Yes' in program_syncs.values else 'No'
 
#         summary.append({
#             'Date': date,
#             'Program': program,
#             'Total_Records': added_count + updated_count + deleted_count,
#             'New_Added': added_count,
#             'Updated': updated_count,
#             'Deleted': deleted_count,
#             'Synced_with_KB': sync_status
#         })
 
#     summary.append({
#         'Date': date,
#         'Program': 'TOTAL',
#         'Total_Records': len(new_df),
#         'New_Added': len(added),
#         'Updated': len(updated),
#         'Deleted': len(deleted),
#         'Synced_with_KB': 'Yes' if 'Yes' in new_df.get('Synced with KB', 'No').values else 'No'
#     })
 
#     return pd.DataFrame(summary), pd.DataFrame(detail_rows)
 
# def upload_report_to_s3(summary_df, details_df):
#     s3 = get_s3_client()
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         summary_df.to_excel(writer, sheet_name='Summary Report', index=False)
#         details_df.to_excel(writer, sheet_name='Detailed Report', index=False)
#     output.seek(0)
#     s3.put_object(Bucket=REPORT_BUCKET, Key=REPORT_KEY, Body=output.getvalue())
#     logger.info(f"Excel report uploaded to s3://{REPORT_BUCKET}/{REPORT_KEY}")
 
# def main():
#     logger.info("=== SDN Comparison Process Started ===")
#     old_df = download_csv_from_s3(OLD_CSV_BUCKET, OLD_CSV_KEY)
#     new_df = download_csv_from_s3(NEW_CSV_BUCKET, NEW_CSV_KEY)
 
#     added, updated, deleted = compare_dataframes_with_fuzzy(old_df, new_df)
#     replace_old_data_file()
 
#     try:
#         ingestion_id = trigger_kb_sync()
#         if wait_for_ingestion_job(ingestion_id):
#             time.sleep(300)
#     except Exception as e:
#         logger.error(f"KB sync failed: {e}")
 
#     added = check_kb_via_api(added) if not added.empty else added
#     updated = check_kb_via_api(updated) if not updated.empty else updated
#     deleted = check_kb_via_api(deleted) if not deleted.empty else deleted
 
#     new_df = get_hashed_dataframe(new_df)
#     merged_sync_data = pd.concat([added, updated, deleted], ignore_index=True)
#     if 'row_hash' in merged_sync_data.columns and 'Synced with KB' in merged_sync_data.columns:
#         new_df = new_df.merge(merged_sync_data[['row_hash', 'Synced with KB']], on='row_hash', how='left')
#         new_df['Synced with KB'] = new_df['Synced with KB'].fillna('No')
 
#     summary_df, details_df = generate_report(added, updated, deleted, new_df)
#     upload_report_to_s3(summary_df, details_df)
#     logger.info("=== SDN Comparison Process Completed ===")
 
# if __name__ == '__main__':
#     main()
 
import csv
import hashlib

def hash_row(row):
    """
    Hash the content of a row to detect any changes.
    """
    return hashlib.md5(','.join(row).encode('utf-8')).hexdigest()

def compare_csv_files(file1, file2, output_diff_file='csv_diff_report.csv'):
    """
    Compare two CSV files line-by-line and log differences as Added, Deleted, or Updated.
    """
    diffs = []

    with open(file1, 'r', newline='', encoding='utf-8') as f1, \
         open(file2, 'r', newline='', encoding='utf-8') as f2:

        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        line_num = 1
        for row1, row2 in zip(reader1, reader2):
            h1, h2 = hash_row(row1), hash_row(row2)

            if h1 == h2:
                # Unchanged - skip if only changes are needed
                pass
            else:
                diffs.append((line_num, 'Updated', row1, row2))
            line_num += 1

        # Remaining lines in file1 (Deleted)
        for row1 in reader1:
            diffs.append((line_num, 'Deleted', row1, []))
            line_num += 1

        # Remaining lines in file2 (Added)
        for row2 in reader2:
            diffs.append((line_num, 'Added', [], row2))
            line_num += 1

    # Save differences to CSV
    with open(output_diff_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Line Number', 'Change Type', 'File1 Content', 'File2 Content'])
        for diff in diffs:
            writer.writerow(diff)

    print(f"Comparison complete. Differences written to '{output_diff_file}'. Total: {len(diffs)} changes.")

# Example usage:
compare_csv_files('1k-chunk.csv', '2k-chunk.csv')
