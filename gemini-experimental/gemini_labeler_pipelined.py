#!/usr/bin/env python3

import json
import os
import argparse
from tqdm import tqdm
import time
# If needed, install the dependencies:
#   pip install langchain-google-genai
#   pip install langchain-core
#   pip install tqdm

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
except ImportError:
    raise ImportError(
        "Please install required packages:\n"
        "  pip install langchain-google-genai langchain-core tqdm"
    )

####################################################
# Replace with your own Gemini (Google) API key or 
# set it in the environment: os.environ["GOOGLE_API_KEY"]
####################################################
gemini_api_key = ""
os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# The 14 key findings we need to analyze
FINDINGS = [
    "Atelectasis",
    "Cardiomegaly",
    "Consolidation",
    "Edema",
    "Enlarged Cardiomediastinum",
    "Fracture",
    "Lung Lesion",
    "Lung Opacity",
    "Pleural Effusion",
    "Pleural Other",
    "Pneumonia",
    "Pneumothorax",
    "Support Devices",
]

def analyze_report(report):
    """
    Analyzes a chest X-ray report and returns a dictionary of refined findings.
    - Keys: the 14 findings (strings).
    - Values: one of "Yes", "No", "Maybe", or "Undefined".
    Raises an exception if anything goes wrong, so the caller can skip this record.
    """
    # First LLM call: check if each finding is *mentioned* (positively or negatively).
    first_prompt = f"""Your task is to analyze a chest X-ray report and determine whether each of the following 14 findings is mentioned in the report. A finding is considered “mentioned” if the report explicitly states its presence, absence, or any related term (including synonyms or negative statements such as “no evidence of _____”). For example, a statement like “no pneumothorax” means that “Pneumothorax” is mentioned, so you must return "True" for that key.

When you receive the chest X-ray report, respond only with a single JSON object. That JSON object must contain exactly the 14 keys listed below. Each key must have either the string "True" or "False" as its value:

{{
"Atelectasis": "...",
"Cardiomegaly": "...",
"Consolidation": "...",
"Edema": "...",
"Enlarged Cardiomediastinum": "...",
"Fracture": "...",
"Lung Lesion": "...",
"Lung Opacity": "...",
"Pleural Effusion": "...",
"Pleural Other": "...",
"Pneumonia": "...",
"Pneumothorax": "...",
"Support Devices": "..."
}}

Where each ... is replaced by "True" if the finding is mentioned (positively or negatively) or "False" if it is not mentioned at all in the report.

Report: "{report}"
"""
    response = llm([HumanMessage(content=first_prompt)])
    
    # Parse the JSON from the LLM response
    content = response.content.strip()
    # Remove fenced code blocks, if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
    # Remove language spec if the response starts with "json" or similar
    if content.lower().startswith("json"):
        content = content.split("\n", 1)[1]
    
    mentioned_findings = json.loads(content)

    # Now refine each mentioned finding into "Yes", "No", or "Maybe"
    refined_findings = {}
    for finding, mentioned in mentioned_findings.items():
        if mentioned == "False":
            # If not mentioned at all, label as "Undefined"
            refined_findings[finding] = "Undefined"
        else:
            time.sleep(3.0)
            # If mentioned, ask the second prompt to check presence/absence
            second_prompt = f"""You are an expert radiologist. Given the following chest X-ray report and the fact that '{finding}' was mentioned (positively or negatively), determine if it is present ("Yes"), explicitly absent ("No"), or indeterminate ("Maybe").

Report: "{report}"

Respond with only one of these three words: "Yes", "No", or "Maybe".
"""
            response2 = llm([HumanMessage(second_prompt.strip())])
            resp_text = response2.content.strip()
            # If unexpected response, default to "Maybe"
            if resp_text not in ["Yes", "No", "Maybe"]:
                print(f"Unexpected response for '{finding}': '{resp_text}'")
                refined_findings[finding] = "Maybe"
            else:
                refined_findings[finding] = resp_text

    return refined_findings


def main():
    parser = argparse.ArgumentParser(
        description="Label chest X-ray reports using Gemini (Google Generative AI), with immediate JSON output and skipping problematic records."
    )
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output JSON file.")
    args = parser.parse_args()

    # Read the input data (a list of dicts, each with 'patient_id', 'study_id', 'content')
    with open(args.input_path, "r") as f:
        data = json.load(f)

    # Open the output file for streaming each record as soon as it's labeled.
    with open(args.output_path, "w") as out:
        out.write("[\n")  # Write the opening bracket of the JSON list

        # We'll keep a counter to determine if we need a comma before each record.
        record_count = 0

        for record in tqdm(data, desc="Labeling reports"):
            time.sleep(5.0)
            # Attempt to retrieve required fields
            try:
                patient_id = record["patient_id"]
                study_id = record["study_id"]
                content = record["content"]
            except KeyError as e:
                print(f"Missing key in record: {e}. Skipping this report.")
                continue

            # Try to label this record
            try:
                labels = analyze_report(content)
            except Exception as e:
                print(f"Error labeling record '{study_id}': {e}\nSkipping this report.")
                continue  # Skip this report entirely

            out_record = {
                "patient_id": patient_id,
                "report_name": study_id,
                "labels": labels
            }

            if record_count > 0:
                out.write(",\n")  # JSON formatting: comma + newline between items
            out.write(json.dumps(out_record, indent=4))
            record_count += 1

        out.write("\n]\n")  # Closing bracket for JSON list

    print(f"Labeling complete! Results saved to {args.output_path}")


if __name__ == "__main__":
    main()
