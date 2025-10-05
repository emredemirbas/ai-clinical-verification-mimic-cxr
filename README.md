# Clinical Verification of AI Models for Radiology Report Annotation

This repository accompanies the research paper:

> **Clinical Verification of AI Models for Radiology Report Annotation Using a Physician-Annotated MIMIC-CXR**  
> *Presented at the 9th IEEE International Symposium on Innovative Approaches in Smart Technologies (ISAS 2025)*  
> [View Paper on IEEE Xplore](https://ieeexplore.ieee.org/document/11101953)

---

## Overview

This project provides the **evaluation results and analysis scripts** used to benchmark  
multiple AI labelers—including **Google Gemini**, **OpenAI GPT-4o**, **CheXpert**,  
and lightweight local models (**DeepSeek-R1**, **Phi-4**)—on radiology report annotation tasks.  

All evaluations were performed against a **physician-validated subset** of the **MIMIC-CXR** dataset,  
focusing on **13 common thoracic findings**.  
The repository includes model outputs (JSON) and metric computation notebooks  
for comparing labeling accuracy, precision, recall, and F1-scores across models.  

---

## Key Findings

- **Gemini** achieved the best overall balance between precision and recall.  
- **CheXpert** performed strongly in well-defined categories (e.g., Lung Opacity) but lacked adaptability.  
- **GPT-4o** showed high precision in some critical findings (e.g., Pneumothorax).  
- **Lightweight local LLMs** (DeepSeek, Phi-4) underperformed due to hardware and domain-training limits.  
- **Rare findings** (e.g., Pleural Other) remained difficult to detect,  
  highlighting the effects of dataset imbalance on model sensitivity.

---

## Repository Contents

- `data/` – Contains model outputs and processed evaluation subsets (no raw MIMIC data).  
- `evaluation-metrics/` – Jupyter notebooks for calculating and visualizing metrics.  
- `gpt_labeler.py`, `gemini_labeler.py` – Scripts used during labeling phase (for reproducibility).  

---

## Authors

**Ömer Faruk Özüyağlı**, **Emre Demirbaş**, **Buse Nur İleri**, **Ebubekir Alatepe**,  
**Yasin Durusoy**, **M. Fatih Demirci**  
Department of Computer Engineering, Ankara Yıldırım Beyazıt University  
and Oteo Health Technologies

---

> *This repository contains evaluation artifacts only.  
> All experiments were conducted using the physician-labeled MIMIC-CXR dataset under PhysioNet license.*
