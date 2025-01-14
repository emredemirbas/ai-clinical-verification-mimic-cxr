import argparse
import json
import time
from tqdm import tqdm
import google.generativeai as genai

def classify_reports_with_gemini(reports, chat_session, output_file):
    labelled_reports = []

    for report in tqdm(reports, desc="Classifying Reports", unit="report"):
        patient_id = report["patient_id"]
        report_name = report["study_id"]
        content = report["content"]

        try:
            time.sleep(1)  # Rate-limiting: adjust as needed.
            response = chat_session.send_message(content)
            raw_response = response.text.strip("```").strip()

            # Remove any invalid prefix like 'json' and extract JSON object
            if raw_response.startswith("json"):
                raw_response = raw_response[len("json"):].strip()

            # Locate the first valid JSON object in the response
            start_index = raw_response.find("{")
            end_index = raw_response.rfind("}") + 1
            if start_index == -1 or end_index == 0:
                raise ValueError("No JSON object found in the response.")

            cleaned_response = raw_response[start_index:end_index]
            labels = json.loads(cleaned_response)

            labelled_reports.append({
                "patient_id": patient_id,
                "report_name": report_name,
                "labels": labels
            })

        except (ValueError, json.JSONDecodeError) as e:
            print(f"JSON decoding error for report {report_name} of patient {patient_id}: {e}")
        except Exception as e:
            print(f"Error processing report {report_name} for patient {patient_id}: {e}")

        # Write out partially updated results after each classification
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(labelled_reports, f, ensure_ascii=False, indent=4)

    return labelled_reports

def main():
    parser = argparse.ArgumentParser(description="Classify chest X-ray reports using Gemini (PaLM) API.")
    parser.add_argument('--prompt_path', type=str, required=True, help="Path to the .txt file containing the model prompt.")
    parser.add_argument('--input_path', type=str, required=True, help="Path to the input JSON file containing the reports.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to the output JSON file where classified reports will be saved.")
    args = parser.parse_args()

    # Read the prompt instructions from text file
    with open(args.prompt_path, "r", encoding="utf-8") as f_prompt:
        prompt_text = f_prompt.read()

    # Read the input JSON
    with open(args.input_path, "r", encoding="utf-8") as f_input:
        reports = json.load(f_input)

    # Configure the Gemini (PaLM) API with your key
    api_key = "AIzaSyANXX_m0XFeOCbZANq0VAVJVTsZfvTlr8g"
    genai.configure(api_key=api_key)

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Prepare the chat session with the initial instructions from the prompt file
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt_text],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, I understand. I'm ready to receive the radiology reports and will classify them according to your instructions, returning the JSON template with the appropriate answers. I will always return the full template, even if some fields are 'Undefined'.\n",
                ],
            },
        ]
    )

    # Perform classification
    classify_reports_with_gemini(reports, chat_session, args.output_path)

if __name__ == "__main__":
    main()
