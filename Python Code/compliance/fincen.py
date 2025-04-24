import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.fincen.gov/resources/statutes-and-regulations/311-special-measures"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Locate the correct table using its ID
table = soup.find('table', id='special-measures-table')

# Extract rows
rows = table.find_all('tr')

# Prepare CSV
with open('fincen.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow(['Entity', 'Finding', 'Notice of Proposed Rulemaking', 'Final Rule', 'Rescinded'])

    for row in rows[1:]:  # skip the header row
        cells = row.find_all('td')
        if not cells or len(cells) < 1:
            continue

        entity = cells[0].get_text(strip=True)

        def extract_link_or_text(cell):
            a = cell.find('a')
            if a and a.get('href'):
                href = a['href']
                return f"https://www.fincen.gov{href}" if not href.startswith("http") else href
            return cell.get_text(strip=True)

        finding = extract_link_or_text(cells[1]) if len(cells) > 1 else ''
        nprm = extract_link_or_text(cells[2]) if len(cells) > 2 else ''
        final_rule = extract_link_or_text(cells[3]) if len(cells) > 3 else ''
        rescinded = extract_link_or_text(cells[4]) if len(cells) > 4 else ''

        writer.writerow([entity, finding, nprm, final_rule, rescinded])

print("✅ Successfully saved 'fincen.csv' with rulemaking table data.")
