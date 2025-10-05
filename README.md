# Clinical Verification of AI Models for Radiology Report Annotation

This repository accompanies the research paper:

> **Clinical Verification of AI Models for Radiology Report Annotation Using a Physician-Annotated MIMIC-CXR**  
> *Presented at the 9th IEEE International Symposium on Innovative Approaches in Smart Technologies (ISAS 2025)*  
> [View Paper on IEEE Xplore]([https://ieeexplore.ieee.org/](https://ieeexplore.ieee.org/document/11101953))

---

## Overview

This project investigates the **clinical reliability of AI models** in **radiology report annotation**,  
benchmarking several **Large Language Models (LLMs)** — including GPT-4, Gemini, Phi-4, and DeepSeek-R1 —  
against **physician-labeled MIMIC-CXR** datasets.

The repository contains:
- AI-generated and ground-truth labeled reports  
- Evaluation notebooks for accuracy, precision, recall, and F1 metrics  
- Labeling pipelines for GPT-based and Gemini-based experiments

---

## 🧠 Models Evaluated

| Model | Provider | Mode |
|:------|:----------|:-----|
| GPT-4 | OpenAI | API |
| Gemini 1.5 Pro | Google | API |
| DeepSeek-R1 Distill | Local (HuggingFace) | Offline |
| Phi-4 | Local (HuggingFace) | Offline |

---

> 🧾 *For academic use only. Dataset usage complies with the PhysioNet MIMIC-CXR license.*
