# import requests
# import xml.etree.ElementTree as ET
# import json
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer
# import numpy as np

# # Function to clean and preprocess text
# def preprocess_text(text):
#     noise_words = [".",",", " ", "", "-", "/","~","@","#","$","%","^","*","(",")",
#                    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
#                    "co", "co.", "llc", "ltd", "rd", "st", "dr", "cir", "corp","bank",
#                    "as","al", "el", "the", "of", "a", "an", "for", "", "apt", "and",
#                    "st", "dr", "road", "rd", "llc", "bldg", ".", "-", ",","po.","po",
#                    "post box", "postbox","no","no.", "cir", "al", "el", "the",
#                    "of", "an", "a", "for", "", "P O Box", "bank", "apt", "and"]
#     words = text.lower().split()
#     cleaned_words = [word for word in words if word not in noise_words]
#     return ' '.join(cleaned_words)

# # Function to calculate cosine similarity between two texts
# def calculate_cosine_similarity(text1, text2):
#     if not text1 or not text2:
#         return 0.0
#     vectorizer = CountVectorizer().fit_transform([text1, text2])
#     vectors = vectorizer.toarray()
#     return cosine_similarity(vectors)[0][1]

# # Function to calculate composite score
# def calculate_composite_score(name_score, city_score, country_score, is_beneficiary_us):
#     if not city_score or not country_score:
#         composite_score = (name_score * 0.90) + (city_score * 0.1) + (country_score * 0.1)    
#     elif not city_score and not country_score:
#         composite_score = (name_score * 1) 
#     else:
#        composite_score = (name_score * 0.7) + (city_score * 0.1) + (country_score * 0.2)
    
#     if is_beneficiary_us:
#         composite_score += 10  # Extra weightage for US beneficiary
#     return min(composite_score, 100)

# # Function to parse SDN XML data with namespace handling
# def parse_sdn_data(xml_content):
#     namespaces = {'ns': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'}
#     root = ET.fromstring(xml_content)
#     sdn_list = []
#     for entry in root.findall('.//ns:sdnEntry', namespaces):
#         first_name = entry.find('ns:firstName', namespaces).text if entry.find('ns:firstName', namespaces) is not None else ''
#         last_name = entry.find('ns:lastName', namespaces).text if entry.find('ns:lastName', namespaces) is not None else ''
#         full_name = f"{first_name} {last_name}".strip()
        
#         # Handle multiple addresses
#         addresses = entry.findall('.//ns:address', namespaces)
#         city = ''
#         country = ''
#         for address in addresses:
#             city = address.find('ns:city', namespaces).text if address.find('ns:city', namespaces) is not None else city
#             country = address.find('ns:country', namespaces).text if address.find('ns:country', namespaces) is not None else country
        
#         sdn_entry = {
#             'name': full_name,
#             'city': city,
#             'country': country
#         }
#         sdn_list.append(sdn_entry)
#     return sdn_list


# # Function to match transaction data with SDN data and calculate scores
# def match_transaction_with_sdn(transaction_data, sdn_data):
#     matches = []
#     for item in transaction_data['items']:
#         if item['skipScanning'].lower() == 'no':
#             item_name = preprocess_text(item['name'])
#             item_city = preprocess_text(item['city']) if 'city' in item else ''
#             item_country = preprocess_text(item['country']) if 'country' in item else ''
#             is_beneficiary_us = item['type'] == 'Beneficiary' and item_country.lower() == 'us'

#             for sdn_entry in sdn_data:
#                 sdn_name = preprocess_text(sdn_entry['name'])
#                 sdn_city = preprocess_text(sdn_entry['city'])
#                 sdn_country = preprocess_text(sdn_entry['country'])

#                 name_score = calculate_cosine_similarity(item_name, sdn_name) * 100
#                 city_score = calculate_cosine_similarity(item_city, sdn_city) * 100 if item_city else 0
#                 country_score = calculate_cosine_similarity(item_country, sdn_country) * 100 if item_country else 0

#                 composite_score = calculate_composite_score(name_score, city_score, country_score, is_beneficiary_us)

#                 if composite_score > 50:
#                     matches.append({
#                         'type': item['type'],
#                         'item_name': item['name'],
#                         'sdn_name': sdn_entry['name'],
#                         'composite_score': composite_score,
#                         'name_score': name_score,
#                         'city_score': city_score,
#                         'country_score': country_score
#                     })
#     return matches

# # Function to determine risk rating based on composite score
# def determine_risk_rating(composite_scores):
#     if len(composite_scores) == 0:
#         return 'low'
#     avg_composite_score = np.mean(composite_scores)
#     if avg_composite_score > 90:
#         return 'high'
#     elif avg_composite_score > 70:
#         return 'medium'
#     else:
#         return 'low'

# # Main function to process transaction data and generate output
# def process_transaction(transaction_json_url, sdn_xml_url):
#     # Load transaction JSON data from file
#     with open(transaction_json_url, 'r') as f:
#         transaction_data = json.load(f)
    
#     # Load SDN XML data from file
#     with open(sdn_xml_path, 'r') as f:
#         sdn_data_content = f.read()

#     sdn_data = parse_sdn_data(sdn_data_content)

#     # Match transaction data with SDN data and calculate scores
#     matches = match_transaction_with_sdn(transaction_data, sdn_data)

#     # Calculate overall composite score and risk rating
#     composite_scores = [match['composite_score'] for match in matches]
#     overall_composite_score = np.mean(composite_scores) if composite_scores else 0
#     risk_rating = determine_risk_rating(composite_scores)

#     # Generate output table
#     output_table = []
#     for match in matches:
#         output_table.append([
#             match['type'],
#             match['item_name'],
#             match['sdn_name'],
#             match['composite_score'],
#             match['name_score'],
#             match['city_score'],
#             match['country_score']
#         ])

#     # Print the output table and other details
#     print("Matches with score over 80:")
#     print("Type\tItem Name\tSDN Name\tComposite Score\tName Score\tCity Score\tCountry Score")
#     for row in output_table:
#         print("\t".join(map(str, row)))

#     print(f"\nOverall Composite Score: {overall_composite_score}")
#     print(f"Risk Rating: {risk_rating}")

# # Example usage with URLs (replace with actual URLs)
# input_json_path = './input.json'
# sdn_xml_path = './try_sdn.xml'
# process_transaction(input_json_path, sdn_xml_path)

# import csv
# import re
# import pandas as pd

# # Input and Output file paths
# input_file = "filtered_output.csv"   # Change this to your actual CSV file
# output_file = "output.xlsx"

# # Function to extract special characters from a string
# def extract_special_characters(text):
#     return "".join(re.findall(r"[^\w\s]", text))  # Finds all non-alphanumeric, non-space characters

# # List to store extracted data
# data = []

# # Read the CSV file and process lines
# with open(input_file, "r", newline="", encoding="utf-8") as infile:
#     reader = csv.reader(infile)
    
#     for row_number, row in enumerate(reader, start=1):  # Start from row 1
#         line_content = ",".join(row)  # Combine all columns into one string (in case of multiple columns)
#         special_chars = extract_special_characters(line_content)
#         data.append([row_number, line_content, special_chars])

# # Convert to DataFrame
# df = pd.DataFrame(data, columns=["Row Number", "Content", "Special Characters"])

# # Save as Excel
# df.to_excel(output_file, index=False)

# print(f"Excel file '{output_file}' created successfully! 🚀")



# import json
# import csv
# import os

# def create_json_file(data, filename="data.json"):
    
#     if not isinstance(data, list):
#         raise TypeError("Input data must be a list of dictionaries.")

#     processed_data = []
#     expected_keys = ["name", "addresses", "programs", "source"]

#     for person_data in data:
#         if not isinstance(person_data, dict):
#             print(f"Warning: Skipping non-dictionary item in input data: {person_data}")
#             continue

#         processed_person = {key: "" for key in expected_keys}

#         for key in expected_keys:
#             if key in person_data and person_data[key] is not None:
#                 processed_person[key] = person_data[key]

#         processed_data.append(processed_person)

#     try:
#         with open(filename, 'w') as f:
#             json.dump(processed_data, f, indent=4)
#         print(f"Successfully created JSON file: {filename}")
#     except IOError as e:
#         print(f"An error occurred while writing the JSON file '{filename}': {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred during JSON writing: {e}")

# def read_csv_file(csv_filename="input.csv"):
#     data = []
#     if not os.path.exists(csv_filename):
#         print(f"Error: CSV file '{csv_filename}' not found.")
#         return data 

#     try:
#         with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             if reader.fieldnames is None:
#                  print(f"Error: CSV file '{csv_filename}' appears to be empty or missing headers.")
#                  return []

#             print(f"CSV Headers found: {reader.fieldnames}")
#             print("Expected headers: name, address, program (case-insensitive)")

#             for row in reader:
#                 normalized_row = {k.lower(): v for k, v in row.items() if k}
#                 data.append(normalized_row)

#         print(f"Successfully read {len(data)} rows from {csv_filename}")

#     except FileNotFoundError:
#         print(f"Error: CSV file '{csv_filename}' not found.")
#     except csv.Error as e:
#          print(f"An error occurred while reading the CSV file '{csv_filename}': {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred during CSV reading: {e}")

#     return data

# def main():
#     csv_file = "consolidated-trim.csv"
#     json_file = "output.json" 

#     # Read data from the CSV file
#     data_from_csv = read_csv_file(csv_file)

#     if data_from_csv:
#         create_json_file(data_from_csv, json_file)
#     else:
#         print("No data read from CSV. JSON file creation skipped.")


# if __name__ == "__main__":
#     main()



import json

# File paths
input_file = 'output.json'    # Replace with your input file name
output_file = 'output.jsonl'  # Desired output file name

# Load JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write JSONL file
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in data:
        json_line = json.dumps(entry)
        f.write(json_line + '\n')

print(f"Conversion complete! Saved to {output_file}")
