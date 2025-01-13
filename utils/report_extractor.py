#!/usr/bin/env python3

import os
import re
import json
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract radiology report data into JSON.")
    parser.add_argument("--input_folder", required=True, help="Path to the input folder containing patient subfolders.")
    parser.add_argument("--output_file", required=True, help="Path for the output JSON file.")
    return parser.parse_args()

def extract_findings_and_impression(report_text):
    """
    Extract the 'FINDINGS' and 'IMPRESSION' text blocks from the report.
    The function returns a single string that merges the two sections.
    """

    # To keep it flexible, let's convert to uppercase for searching,
    # but still store the original text for the final output.
    report_upper = report_text.upper()

    # Patterns to match headings (we use a non-greedy capture of text until next heading or end)
    # We'll try to capture everything after "FINDINGS:" until "IMPRESSION:" or end,
    # and everything after "IMPRESSION:" until the end or next heading.
    findings_match = re.search(r'(FINDINGS:)(.*?)(?=IMPRESSION:|$)', report_upper, flags=re.DOTALL)
    impression_match = re.search(r'(IMPRESSION:)(.*)$', report_upper, flags=re.DOTALL)

    findings_text = ""
    impression_text = ""

    if findings_match:
        # We extract the corresponding part from the original text (case sensitive),
        # so let's figure out the actual start and end in original string.
        start_index = report_upper.find(findings_match.group(1))
        end_index = start_index + len(findings_match.group(1) + findings_match.group(2))
        findings_text = report_text[start_index:end_index]

        # Remove the heading label "FINDINGS:"
        findings_text = re.sub(r'(?i)^FINDINGS:\s*', '', findings_text.strip())

    if impression_match:
        # Similarly extract from the original text.
        start_index = report_upper.find(impression_match.group(1))
        # For the end, we take the length of the matched text from the `report_text`.
        end_index = start_index + len(impression_match.group(1) + impression_match.group(2))
        impression_text = report_text[start_index:end_index]

        # Remove the heading label "IMPRESSION:"
        impression_text = re.sub(r'(?i)^IMPRESSION:\s*', '', impression_text.strip())

    # Combine the findings and impression text
    combined = findings_text.strip() + "\n" + impression_text.strip()
    return combined.strip()

def main():
    args = parse_arguments()
    
    input_folder = args.input_folder
    output_file = args.output_file

    # List to hold all extracted data
    all_reports_data = []

    # We'll walk through all subfolders and files
    # If subfolder name matches p<patient_id> and file is s<study_id>.txt, we parse it.
    
    # Collect all .txt files of interest first
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            # Check if file ends with .txt
            if filename.lower().endswith(".txt"):
                # Confirm the parent folder matches pattern "p<number>" 
                # and filename matches pattern "s<number>.txt"
                base_folder_name = os.path.basename(root)  # e.g., "p1234"
                if (re.match(r'^p\d+$', base_folder_name) and 
                    re.match(r'^s\d+\.txt$', filename.lower())):
                    file_paths.append(os.path.join(root, filename))
    
    # Use a progress bar over the collected file paths
    for file_path in tqdm(file_paths, desc="Processing reports"):
        # Parse out patient_id and study_id from folder and file names
        folder_name = os.path.basename(os.path.dirname(file_path))  # e.g., p1234
        file_name = os.path.basename(file_path)                     # e.g., s5678.txt

        patient_id = folder_name[1:]  # remove leading 'p'
        study_id = file_name[1:file_name.lower().find('.txt')]  # remove leading 's' and trailing '.txt'

        # Read the .txt file content
        with open(file_path, 'r', encoding='utf-8') as f:
            report_text = f.read()

        # Extract the FINDINGS and IMPRESSION text
        content = extract_findings_and_impression(report_text)

        # Create an entry for JSON
        entry = {
            "patient_id": patient_id,
            "study_id": study_id,
            "content": content
        }
        all_reports_data.append(entry)

    # Write out to JSON file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(all_reports_data, out_f, indent=4, ensure_ascii=False)

    print(f"Extraction completed. {len(all_reports_data)} reports saved to {output_file}.")

if __name__ == "__main__":
    main()
