![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

# 🏟️ Resilient EPL Data Pipeline
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
graph TD
    A[World Wide Web / FBref] -->|HTTP Request| B(Python Scraper Engine)
    B -->|BeautifulSoup| C{HTML Parser}
    C -->|Extraction| D[Raw DataFrame]
    D -->|Pandas Validation| E{Integrity Guard}
    E -->|Fails| F[Error Log/Skip]
    E -->|Passes| G[Clean CSV]
    G -->|Boto3 SDK| H[Amazon S3 Data Lake]
    H -->|Monitoring Script| I{Health Check}
    I -->|Stale/Small| J[Failure Alert]
    I -->|Verified| K[Production Ready Data]