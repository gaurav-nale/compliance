import pandas as pd
import json
import numpy as np
import os
 
# Get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
 
# CSV file path
csv_file_path = os.path.join(current_dir, 'main_1k.csv')
 
# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)
 
# Replace NaN with None (which becomes null in JSON)
df = df.replace({np.nan: None})
 
# Convert to list of dictionaries
records = df.to_dict(orient='records')
 
# JSON output path
json_file_path = os.path.join(current_dir, '1k_chunk_2.0.json')
 
# Save as JSON with nulls correctly rendered
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2)
 
print(f"JSON file created at: {json_file_path}")

