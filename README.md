# ai-clinical-verification-mimic-cxr

Usage of GPT Labeler:

python3 gpt_labeler.py --input_path <> --output_path <> --prompt_path <> --model <> (default gpt-4, if you not want to specify model, do not pass that parameter.)

Usage of Gemini Labeler:

python3 gemini_labeler.py --input_path <> --output_path <> --prompt_path <>

Usage of Pipelined Gemini Labeler:

python3 gemini_labeler_pipelined.py --input_path <> --output_path <>

Usage of extract_reports_by_study_id: 
python extract_relevant_reports.py --csv_file <> --input_folder <> --output_file <>

  • csv_file: mimic-cxr-2.1.0-test-set-labeled.csv
  
  • input_folder: folder that contains all the reports, named "files"
  
  • output_file: relevant_reports.json

---
data

• relevant_reports.json: Contains raw data for 685 relevant reports, identified using patient_id and study_id from the mimic-cxr-2.1.0-test-set-labeled.csv file.

• mimic-cxr-2.1.0-test-set-labeled.csv: Ground truth dataset with labels for 687 reports.

• deepseek_r1_distill_local_output.json: Contains labeled outputs from the DeepSeek R1 Distill Local model.

• phi4_output.json: Contains labeled outputs from the Phi4 Local model.
