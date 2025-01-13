import google.generativeai as genai
import json
import time

# GeminiAI API anahtarı
api_key = "AIzaSyANXX_m0XFeOCbZANq0VAVJVTsZfvTlr8g"

"""
Install the Google AI Python SDK:
$ pip install google.generativeai
"""

# Configure the API key
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
"""
You are given a chest X-ray report (FINDINGS + IMPRESSION). Your task is to classify the presence of 14 findings in this report:

    Atelectasis
    Cardiomegaly
    Consolidation
    Edema
    Enlarged Cardiomediastinum
    Fracture
    Lung Lesion
    Lung Opacity
    Pleural Effusion
    Pleural Other
    Pneumonia
    Pneumothorax
    Support Devices

Your response MUST be a single JSON object with these 14 keys and one of the following four label values for each key:

    "Yes" if there is strong evidence that the finding is present.
    "No" only if the report explicitly and clearly states the finding is NOT present (e.g., "no pleural effusion").
    "Maybe" if it is mentioned but remains unclear or indeterminate.
    "Undefined" if there is no mention at all of the finding in the report. (This is the default case.)

Do not include any other text, reasoning, explanations, disclaimers, or formatting besides the JSON object. Only provide the following structure (with appropriate labels for each key):

{
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
}

Replace the "..." with "Yes", "No", "Maybe", or "Undefined". No other text is allowed in the answer.


Wait for reports will be sent to you.
""",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, I understand. I'm ready to receive the radiology reports and will classify them according to your instructions, returning the JSON template with the appropriate answers. I will always return the full template, even if some fields are 'Undefined'.\n",
            ],
        },
    ]
)

print(type(chat_session))

def classify_reports_with_gemini(reports, chat_session, output_file):
    labelled_reports = []

    for report in reports:
        patient_id = report["patient_id"]
        report_name = report["study_id"]
        content = report["content"]

        try:
            time.sleep(1)
            response = chat_session.send_message(content)
            raw_response = response.text.strip("```").strip()

            # Remove invalid prefixes like 'json' and extract JSON object
            if raw_response.startswith("json"):
                raw_response = raw_response[len("json"):].strip()

            # Extract the first valid JSON object
            try:
                # Locate the start and end of the JSON object
                start_index = raw_response.find("{")
                end_index = raw_response.rfind("}") + 1
                if start_index == -1 or end_index == 0:
                    raise ValueError("No JSON object found in the response.")

                cleaned_response = raw_response[start_index:end_index]
                print(f"Extracted JSON: {cleaned_response}")

                labels = json.loads(cleaned_response)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"JSON decoding error for report {report_name} of patient {patient_id}: {e}")
                continue

            labelled_reports.append({
                "patient_id": patient_id,
                "report_name": report_name,
                "labels": labels
            })
        except Exception as e:
            print(f"Error processing report {report_name} for patient {patient_id}: {e}")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(labelled_reports, f, ensure_ascii=False, indent=4)

    return labelled_reports

if __name__ == "__main__":
    input_file = "/home/faruk/Desktop/404_research/gemini-deneme/random_sample.json"
    output_file = "/home/faruk/Desktop/404_research/gemini-deneme/output_reports.json"

    with open(input_file, "r", encoding="utf-8") as f:
        reports = json.load(f)

    classify_reports_with_gemini(reports, chat_session, output_file)
