import boto3
import pandas as pd
import io
import hashlib
import config
import aurora_db

s3_client = boto3.client(
    service_name = 's3',
    region_name = "us-east-2",
    aws_access_key_id='ASIA3FLD26ANPITGQCPL', 
    aws_secret_access_key='CCwrXg8+sygd7lzKy7bqsMBFGbffCNAVRNIduQ8S',
    aws_session_token = 'IQoJb3JpZ2luX2VjEEgaCXVzLWVhc3QtMSJHMEUCIQDxNck8NlpVjFv020KUO27TlnFuWebrEPp0dRSAcuW2bgIgF7qO+836fsASwNWv3L/O5w2aycBQ9kBTgzg+nZdsxpIq/AIIkf//////////ARAAGgw3NjczOTc5MTY2OTgiDBGmylIyK+wPeTJmpCrQAqeSido+WSypfrA2j2UQn5pqC329bWY25D9lQZ/0JzTghfj98Zd/PECLuFoNr/2ImHu8Q7ADzC5uYGoRnNzCEOmJbzu/uINW+nxjANNHvvM9Dr1l73nXa5e9kiw1FTqKfPOSaB7EU48vHaAuXGCmjCGipiEBUbiyzoy0TTBXpOCTCnAfgOUgahjvbbWZV+VFe76TBxkzDxIUMMYatcZxxQ01N4hlGkHdrRmT0er74pg/e0fnpCMIDFRiLW7tiCTzjIcVwybQuw8k59FuIJ7LdErv4klGa3rksMesPXs12iE7fMbglhaWwX5rsjzH7m9SMScm9dRC06Tttua/KIx9kZJ8X+R8he49SAWbVU8oTgp8Y1UOgpJOCtKivfczjxqCPFujKDzXeLAsfK30keoym2h/lhvP3QVIl6jkFGLdBihqsH9KBwWJ4etuX/Z7rozf7TDmkby+BjqnAZLQPjMGMKznQGJQNlAN3xZQujjGIVWGxWFoGEZhqEH5gbNzgiPZC3M1uE2klo6bXZKj+ur2AKBm2r3fDttC1RW0vPNMvHL7ZP7uLYvJrYIaNwGzf3DJRhJF41aE0PtsA4v9o5mHOd/upm5KecfaxMHiqwkY7FF81AhwpBpRqy4qfXhdm+3v8vT/OT7GJczzLTrnvWdDSwRmNpIxKtFGj6bE59xk08MB'
    )

def get_s3_document_content():
    response = s3_client.get_object(Bucket=config.S3_BUCKET_1, Key=config.S3_KEY_1)
    csv_content = response['Body'].read().decode('utf-8')
    return csv_content

def calculate_row_hash(row):
    row_str = ",".join(map(str, row.values))
    return hashlib.md5(row_str.encode()).hexdigest()


def process_updated_lines_into_aurora():
    csv_content = get_s3_document_content()
    df = pd.read_csv(io.StringIO(csv_content))

    df[config.ID_COLUMN] = df.apply(calculate_row_hash, axis = 1)

    existing_hashes = aurora_db.get_existing_hashes()
    new_rows = df[~df[config.ID_COLUMN].isin(existing_hashes)]

    if not new_rows.empty:
        aurora_db.insert_vectors(new_rows)
    else:
        print("No new rows found in S3 File")


process_updated_lines_into_aurora()