# Clinical Verification of AI Models for Radiology Report Annotation

This repository accompanies the research paper:

> **Clinical Verification of AI Models for Radiology Report Annotation Using a Physician-Annotated MIMIC-CXR**  
> *Presented at the 9th IEEE International Symposium on Innovative Approaches in Smart Technologies (ISAS 2025)*  
> [View Paper on IEEE Xplore](https://ieeexplore.ieee.org/document/11101953)

---

## Overview

This project investigates the **clinical reliability of AI models** in **radiology report annotation**,  
benchmarking several **Large Language Models (LLMs)** — including GPT-4, Gemini, Phi-4, and DeepSeek-R1 —  
against **physician-labeled MIMIC-CXR** datasets.

The repository contains:
- Model output files (annotations produced by GPT-4o, Gemini 1.5 Pro, Microsoft Phi4, and Deepseek-R1-Distill-
Llama-8B)  
- Evaluation scripts and Jupyter notebooks for metric computation and cross-model comparison  
- Processed subsets of the MIMIC-CXR dataset (no raw or ground-truth data included)

---

##  Models Evaluated

| Model | Provider | Mode |
|:------|:----------|:-----|
| GPT-4 | OpenAI | API |
| Gemini 1.5 Pro | Google | API |
| DeepSeek-R1 Distill | Local (HuggingFace) | Offline |
| Phi-4 | Local (HuggingFace) | Offline |

---

> *For academic use only. Dataset usage complies with the PhysioNet MIMIC-CXR license.*
