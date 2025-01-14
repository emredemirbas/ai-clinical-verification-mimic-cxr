import argparse
import json
import asyncio
import time
from tqdm import tqdm
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key="")

async def classify_reports_with_chatgpt(reports, prompt_text, output_file, model="gpt-4"):
    """
    Classify chest X-ray reports using ChatGPT API.
    :param reports: List of report dictionaries (patient_id, study_id, content, etc.)
    :param prompt_text: Prompt instructions loaded from a text file.
    :param output_file: Path to save JSON output.
    :param model: OpenAI model name (default is 'gpt-4').
    """
    labelled_reports = []

    for report in tqdm(reports, desc="Classifying Reports", unit="report"):
        patient_id = report["patient_id"]
        report_name = report["study_id"]
        content = report["content"]

        try:
            # Prepare your messages for ChatGPT
            messages = [
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": content},
            ]

            # Call the OpenAI ChatCompletion API asynchronously
            response = await aclient.chat.completions.create(model=model,
            messages=messages,
            temperature=1,
            top_p=0.95,
            max_tokens=1024)

            # The response content is in choices[0].message.content
            raw_response = response.choices[0].message.content.strip("```").strip()

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

async def main():
    parser = argparse.ArgumentParser(description="Classify chest X-ray reports using ChatGPT API.")
    parser.add_argument('--prompt_path', type=str, required=True, help="Path to the .txt file containing the model prompt.")
    parser.add_argument('--input_path', type=str, required=True, help="Path to the input JSON file containing the reports.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to the output JSON file where classified reports will be saved.")
    parser.add_argument('--model', type=str, default="gpt-4", help="OpenAI model name (e.g., gpt-3.5-turbo, gpt-4).")
    args = parser.parse_args()

    # Read the prompt instructions from text file
    with open(args.prompt_path, "r", encoding="utf-8") as f_prompt:
        prompt_text = f_prompt.read()

    # Read the input JSON
    with open(args.input_path, "r", encoding="utf-8") as f_input:
        reports = json.load(f_input)

    # Configure the ChatGPT API

    # Perform classification
    await classify_reports_with_chatgpt(reports, prompt_text, args.output_path, model=args.model)

if __name__ == "__main__":
    asyncio.run(main())

