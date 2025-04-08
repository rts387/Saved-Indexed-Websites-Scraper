# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 22:19:25 2025

@author: shook
"""
import os
import csv
import re
from bs4 import BeautifulSoup

# Folder containing downloaded HTML files
html_folder = "E:\thehub-via"
# Monikers to search for (case insensitive)
monikers = [r"\bBonesKoopa\b", r"\bOpiateKing88\b", r"\bSquirejim\b", r"\bDocmax36\b"]

# Email regex pattern (for matching emails)
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Output CSV file
output_csv = "moniker_association_datatheHUB.csv"

def extract_data_from_html(file_path):
    """Extract occurrences of monikers and associated data (emails, links, etc.)."""
    results = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text()

        # Debug: Print the first 500 characters of the text to verify it's being read correctly
        print(f"Text from {os.path.basename(file_path)}: {text[:500]}")

        # Find all email addresses in the text
        emails = re.findall(email_pattern, text)

        # Find occurrences of monikers and gather related data
        for moniker in monikers:
            # Use re.IGNORECASE to handle case insensitivity
            for match in re.finditer(moniker, text, re.IGNORECASE):
                # Extract context around the moniker
                start = max(0, match.start() - 50)  # 50 chars before the moniker
                end = min(len(text), match.end() + 50)  # 50 chars after the moniker
                context = text[start:end].replace("\n", " ").strip()

                # Find any links around the moniker (URLs might be relevant)
                links = [a['href'] for a in soup.find_all('a', href=True)]

                # Check if any emails are in the context around the moniker
                associated_emails = [email for email in emails if email in context]

                # Collect associated data
                results.append({
                    "Filename": os.path.basename(file_path),
                    "Moniker": match.group(),
                    "Emails": associated_emails,
                    "Context": context,
                    "Links": links
                })

    return results

def main():
    all_results = []
    
    # Iterate through all HTML files in the folder
    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            file_path = os.path.join(html_folder, filename)
            results = extract_data_from_html(file_path)

            # Debug: Print results found in this file
            if results:
                print(f"Results found in {filename}: {results}")
            all_results.extend(results)

    # Write results to CSV if there are any
    if all_results:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Filename", "Moniker", "Emails", "Context", "Links"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"Extraction complete. Results saved to {output_csv}")
    else:
        print("No results found to save.")

if __name__ == "__main__":
    main()