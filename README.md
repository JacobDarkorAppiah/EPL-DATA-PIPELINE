![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

# 🏟️ Resilient EPL Data PipelineXIT

**Author:** [Jacob Darkor Appiah](https://github.com/JacobDarkorAppiah)
**Organization:** Codveda Technologies | Data Science Intern

## 📝 Overview
An automated, production-grade system for extracting and analyzing English Premier League data. This project focuses on **resilience**, **automation**, and **cloud-readiness**.

## 🛡️ Key Features
* **Hidden Data Extraction:** Custom BeautifulSoup logic to find tables in HTML comments.
* **Integrity Gate:** Mathematical validation ($W + D + L = MP$) using Pandas.
* **AWS Integration:** Data persistence in Amazon S3 for 99.9% availability.
* **Dockerized:** Fully containerized for one-click deployment.

## 🏗️ Architecture
```mermaid
graph LR
    A[FBref] --> B[Python Scraper]
    B --> C[Data Validation]
    C --> D[AWS S3 Storage]
    D --> E[ML Models]