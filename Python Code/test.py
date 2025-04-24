# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import xml.etree.ElementTree as ET
# import json

# # xml_sdn_data = "./try_sdn.xml"
# # # Parse the XML
# # strings = parse_xml(xml_sdn_data)
# # # Initialize the vectorizer
# # vectorizer = TfidfVectorizer()
# # # Transform XML parse data to vector data
# # tfidfVectorizer = vectorizer.fit_transform(strings)
# # # The compliance data we want to match
# # input = "AbuTeirMohammedIsmail"
# # # Transform input data to vector data
# # input_vector = vectorizer.transform([input])
# # # Calculate cosine similarity
# # similarity_matrix = cosine_similarity(input_vector, tfidfVectorizer)
# # print(similarity_matrix)


# def parse_element(element):
#     parsed_data = {}
#     # Extract specific child elements
#     for child in element:
#         if child.tag.endswith('firstName') or child.tag.endswith('lastName'):
#             parsed_data[child.tag.split('}')[-1]] = child.text.strip() if child.text else ''
#         elif child.tag.endswith('programList'):
#             parsed_data['programList'] = [program.text.strip() for program in child.findall('.//{*}program')]
#         elif child.tag.endswith('addressList'):
#             parsed_data['addressList'] = []
#             for address in child.findall('.//{*}address'):
#                 address_data = {}
#                 for addr_child in address:
#                     address_data[addr_child.tag.split('}')[-1]] = addr_child.text.strip() if addr_child.text else ''
#                 parsed_data['addressList'].append(address_data)
    
#     return parsed_data

# def parse_xml_to_dict(file_path):
#     # Parse the XML file
#     tree = ET.parse(file_path)
#     root = tree.getroot()
    
#     # Define the namespace
#     ns = {'ns': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'}
    
#     # Parse each sdnEntry element
#     parsed_data = []
#     for sdn_entry in root.findall('ns:sdnEntry', ns):
#         parsed_data.append(parse_element(sdn_entry))
    
#     return parsed_data

# def clean_data(data):
#     if isinstance(data, dict):
#         return {k: clean_data(v) for k, v in data.items() if v and clean_data(v)}
#     elif isinstance(data, list):
#         return [clean_data(item) for item in data if item and clean_data(item)]
#     else:
#         return data

# def get_vectordata(data):
#     vector_data = []
#     for entry in data:
#         vector = []
#         vector.append(entry.get('firstName', ''))
#         vector.append(entry.get('lastName', ''))
        
#         # Add program list details
#         for program in entry.get('programList', []):
#             vector.append(program)
        
#         # Add address details if available
#         if 'addressList' in entry:
#             for address in entry['addressList']:
#                 vector.append(address.get('uid', ''))
#                 vector.append(address.get('city', ''))
#                 vector.append(address.get('stateOrProvince', ''))
#                 vector.append(address.get('country', ''))
        
#         vector_data.append(vector)
#     return vector_data


# # Example usage
# file_path = 'consolidated.xml'
# parsed_data = parse_xml_to_dict(file_path)
# clean_dict = clean_data(parsed_data)

# # Save the dictionary to a JSON file
# with open('output.json', 'w') as f:
#     json.dump(clean_dict, f, indent=2)

# vector_data = get_vectordata(clean_dict)

# combined_data = [' '.join(vector) for vector in vector_data]
# vectorizer = CountVectorizer().fit(combined_data)
# vectors = vectorizer.transform(combined_data).toarray()

# # Input data
# input_data = "Jamileh Abdullah GAza"
# input_vector = vectorizer.transform([input_data]).toarray()
# # Calculate cosine similarity
# similarity_matrix = cosine_similarity(input_vector, vectors).flatten()
# print(similarity_matrix)

# import pandas as pd

# # 📌 Load the CSV file (Update this with your actual file path)
# file_path = "matched_data.csv"
# df = pd.read_csv(file_path, encoding="utf-8", dtype=str)  # Read all as strings to avoid conversion issues

# # ✅ Step 1: Check for Missing Values
# missing_values = df.isnull().sum()
# print("\n🔍 Missing Values Per Column:\n", missing_values)

# # 🔄 Fill missing values with "N/A" to prevent AWS Bedrock from skipping rows
# df.fillna("N/A", inplace=True)

# # ✅ Step 2: Check for Duplicate Rows
# duplicate_count = df.duplicated().sum()
# print(f"\n🛑 Duplicate Rows Found: {duplicate_count}")

# # 🔄 Remove duplicates (Optional: Uncomment if you want to remove them)
# # df.drop_duplicates(inplace=True)

# # ✅ Step 3: Detect Special Characters / Formatting Issues
# def detect_special_chars(value):
#     return any(ord(char) > 127 for char in str(value))  # Checks for non-ASCII characters

# special_chars = df.applymap(detect_special_chars).sum()
# print("\n⚠️ Special Character Issues Per Column:\n", special_chars)

# # ✅ Step 4: Save the Cleaned File
# cleaned_file_path = "cleaned_matched_data.csv"
# df.to_csv(cleaned_file_path, index=False, encoding="utf-8")

# print(f"\n✅ Cleaned CSV saved as: {cleaned_file_path}")


# import csv

# def reverse_csv(input_csv_file, output_csv_file):
#     """
#     Reverses the order of rows in a CSV file and writes the reversed content to a new CSV file.
#     The header row (if present) will also be moved to the end.

#     Args:
#         input_csv_file (str): Path to the input CSV file.
#         output_csv_file (str): Path to the new CSV file to be created with reversed content.
#     """
#     try:
#         with open(input_csv_file, 'r', newline='') as infile:
#             reader = csv.reader(infile)
#             header = next(reader, None)  # Read the header row if it exists
#             data_rows = list(reader)     # Read all remaining rows into a list

#         with open(output_csv_file, 'w', newline='') as outfile:
#             writer = csv.writer(outfile)
#             reversed_rows = data_rows[::-1]  # Reverse the list of data rows
#             writer.writerows(reversed_rows)  # Write the reversed data rows
#             if header:
#                 writer.writerow(header)    # Write the header row at the end

#         print(f"Successfully reversed '{input_csv_file}' and saved to '{output_csv_file}'.")

#     except FileNotFoundError:
#         print(f"Error: Input file '{input_csv_file}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     input_file = 'matched_data.csv'   # Replace 'your_input.csv' with the actual path to your CSV file
#     output_file = 'reversed_output.csv' # Replace 'reversed_output.csv' with the desired path for the reversed output CSV file

#     reverse_csv(input_file, output_file)


# import pandas as pd

# def find_matching_rows_excel_csv(excel_file, csv_file, output_csv_file, excel_name_column='Name', csv_name_column='name'):
#     """
#     Reads names from a specified column in an Excel file,
#     finds matching names in a specified column of a CSV file,
#     and writes the entire matching rows from the CSV file to a new CSV file.

#     Args:
#         excel_file (str): Path to the Excel file (containing names to search for).
#         csv_file (str): Path to the CSV file (to search within).
#         output_csv_file (str): Path to the new CSV file to be created with matching rows.
#         excel_name_column (str, optional): Name of the column in the Excel file containing names. Defaults to 'name'.
#         csv_name_column (str, optional): Name of the column in the CSV file containing names. Defaults to 'name'.
#     """
#     try:
#         # Read names from the Excel file
#         df_excel = pd.read_excel(excel_file)
#         if excel_name_column not in df_excel.columns:
#             print(f"Error: Column '{excel_name_column}' not found in '{excel_file}'.")
#             return
#         names_to_find = set(df_excel[excel_name_column].astype(str).str.strip().tolist())
#         print(f"Read {len(names_to_find)} names to search for from '{excel_file}'.")

#         # Read the CSV file
#         df_csv = pd.read_csv(csv_file)
#         if csv_name_column not in df_csv.columns:
#             print(f"Error: Column '{csv_name_column}' not found in '{csv_file}'.")
#             return

#         # Find matching rows in the CSV file
#         matched_rows = df_csv[df_csv[csv_name_column].astype(str).str.strip().isin(names_to_find)]
#         print(f"Found {len(matched_rows)} matching rows in '{csv_file}'.")

#         # Write the matched rows to a new CSV file
#         matched_rows.to_csv(output_csv_file, index=False)
#         print(f"Matched rows from '{csv_file}' written to '{output_csv_file}'.")

#     except FileNotFoundError:
#         print("Error: One or both of the specified files were not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     excel_file_path = 'name list.xlsx'  # Replace with the actual path to your Excel file
#     csv_file_path = 'matched_data.csv'   # Replace with the actual path to your CSV file
#     output_file_path = 'matching_data_60_rows.csv'  # Replace with the desired path for the output CSV file

#     # Ensure you have pandas installed: pip install pandas and openpyxl
#     # pip install pandas openpyxl
#     find_matching_rows_excel_csv(excel_file_path, csv_file_path, output_file_path)




import json
import csv
import random

def extract_random_names_to_csv_from_file(json_file_path, output_csv_path, num_names=1000):

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Ensure it's a valid JSON list.")
        return

    all_names = []
    for data in json_data_list:
        name = data.get('name')
        if name:
            all_names.append(name)

    if not all_names:
        print("No names found in the provided JSON data.")
        return

    num_available_names = len(all_names)
    num_to_extract = min(num_names, num_available_names)

    if num_to_extract < num_names:
        print(f"Warning: Only {num_available_names} names found, extracting all of them.")

    random_names = random.sample(all_names, num_to_extract)

    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name'])  # Write header row
            for name in random_names:
                writer.writerow([name])
        print(f"Successfully extracted {len(random_names)} random names to '{output_csv_path}'")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Example Usage:
if __name__ == "__main__":
    input_json_file = '1k_chunk_2.0.json'  # Replace with the actual path to your JSON file
    output_csv_file = 'random_names.csv'
    extract_random_names_to_csv_from_file(input_json_file, output_csv_file)
    # To extract a different number of names, you can specify the num_names argument:
    # extract_random_names_to_csv_from_file(input_json_file, output_csv_file, num_names=50)