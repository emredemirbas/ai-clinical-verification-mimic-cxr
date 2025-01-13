#!/usr/bin/env python3

import argparse
import json
import random
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Randomly sample reports from a JSON file.")
    parser.add_argument("--reports_path", required=True, help="Path to the JSON file containing the reports.")
    parser.add_argument("--output_path", required=True, help="Path to the output JSON file for sampled reports.")
    parser.add_argument("--number", type=int, required=True, help="Number of reports to sample.")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read reports from JSON
    with open(args.reports_path, 'r', encoding='utf-8') as f:
        all_reports = json.load(f)
    
    total_reports = len(all_reports)

    # Number of samples requested
    sample_count = args.number

    if sample_count <= 0:
        raise ValueError("Number of reports to sample must be greater than 0.")
    if sample_count > total_reports:
        raise ValueError(f"Requested sample size ({sample_count}) is greater than the total number of reports ({total_reports}).")

    # Randomly sample the specified number of reports
    sampled_reports = random.sample(all_reports, sample_count)

    # Write sampled reports to output JSON
    with open(args.output_path, 'w', encoding='utf-8') as out_f:
        json.dump(sampled_reports, out_f, indent=4, ensure_ascii=False)

    print(f"Successfully sampled {sample_count} reports out of {total_reports} and saved to '{args.output_path}'.")

if __name__ == "__main__":
    main()
