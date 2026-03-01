# ⚽ EPL-DATA-PIPELINE
### 🚀 Production-Grade ETL & Analytics System

<p align="center"> 
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python"/> 
  <img src="https://img.shields.io/badge/Docker-Containerized-blue?logo=docker"/> 
  <img src="https://img.shields.io/badge/AWS-S3%20%7C%20SNS-orange?logo=amazon-aws"/> 
  <img src="https://img.shields.io/badge/License-MIT-green"/> 
</p>

## 📌 Overview
A robust, cloud-native **Data Engineering pipeline** that automates the collection, transformation, and storage of English Premier League (EPL) standings. This system replaces fragile web scraping with a resilient REST API architecture, ensuring 99.9% data availability for downstream analytics.

---

## 🏗️ System Architecture


```mermaid
graph TD
    %% Ingestion Layer
    A[Football-Data.org API<br/><i>REST Endpoint</i>] -->|JSON Request| B(Python Fetcher Engine)
    B -->|json.load| C{Data Normalizer}
    
    %% Transformation Layer
    C -->|Extraction| D[Pandas DataFrame]
    D -->|Cleaning & Mapping| E{Integrity Guard}
    E -->|Passes| G[Processed CSV Asset]
    
    %% DevOps & Orchestration
    G -->|Docker Runtime| H[Containerized Pipeline]
    H -->|GitHub Actions| I[Automated Execution]
    
    %% Cloud & Notification Layer
    I -->|Boto3 SDK| J[(Amazon S3 Data Lake)]
    J -->|S3 Event Notification| K{Amazon SNS Topic}
    K -->|Email Alert| L[📧 Stakeholders Notified]

    style A fill:#00acee,stroke:#333,stroke-width:2px
    style J fill:#ff9900,stroke:#232f3e,stroke-width:2px
    style K fill:#ff9900,stroke:#232f3e,stroke-width:2px

## 🧱 Architectural Layers
1️⃣ Data Ingestion Layer (fetcher.py)
Technology: REST API Consumption via requests.

Features: X-Auth-Token authentication, automated JSON retrieval, and robust error handling for API rate limits.

2️⃣ Data Processing Layer (transformer.py)
Parsing: Flattening nested JSON structures using pd.json_normalize.

Transformation: Schema enforcement and column mapping (e.g., team.name → team) for analytics readiness.

3️⃣ Cloud & Orchestration
Automation: GitHub Actions daily execution.

Storage: Amazon S3 (Medallion Architecture: raw/ and curated/ layers).

Alerting: Amazon SNS triggers instant email notifications upon successful data persistence. 


## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Data Source** | `Football-Data.org API` |
| **Ingestion** | `Python`, `requests`, `python-dotenv` |
| **Processing** | `pandas`, `JSON` |
| **Cloud Storage** | `AWS S3` |
| **Alerting** | `Amazon SNS` |
| **Containerization** | `Docker` |
| **Orchestration** | `GitHub Actions` |

##🛡️ Engineering & DevOps Standards
🔒 Zero-Leakage Security
Credentials managed via .env (local) and GitHub Secrets (prod).

🐳 Containerization
Lightweight Dockerfile ensures environment parity.

📊 Professional Logging
Emoji-safe, structured logging via utils/logger.py.

🚀 Usage
Sync AWS Credentials: ./sync_lab.ps1

Run Pipeline:

PowerShell:
python src/fetcher.py
python src/transformer.py
python src/upload_to_s3.py

##🏆 Project Author Jacob Darkor Appiah
Data Engineer | Codveda Technologies Data Science Intern