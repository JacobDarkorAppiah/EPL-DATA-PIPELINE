```markdown
# Project Review: EPL Data Pipeline Phase 1

## ✅ Key Achievements
- **Pivoted Architecture**: Migrated from fragile HTML scraping (FBref) to a stable REST API (Football-Data.org) to bypass Cloudflare 403 blocks.
- **AWS Integration**: Built a functional "Local-to-Cloud" bridge using `boto3` and AWS Academy Learner Lab credentials.
- **Data Integrity**: Implemented a transformation layer that converts raw nested JSON into a structured CSV "Gold" dataset.
- **Security First**: Established a `.env` pattern and `.gitignore` safety net to prevent credential leaks.

## 🚧 Challenges Overcome
1. **The 403 Barrier**: FBref's bot protection was too aggressive for standard scrapers. 
   - *Solution*: Re-engineered the Ingestion Layer to use a professional API provider.
2. **Credential Expiry**: AWS Lab keys expire every 4 hours.
   - *Solution*: Developed a PowerShell automation script (`sync_lab.ps1`) to update the local AWS CLI instantly.

## 🔮 Future Roadmap (Phase 2)
- **AWS Glue/Athena**: Enable SQL-based analytics directly on the S3 Data Lake.
- **GitHub Actions**: Fully automate the Docker container to run on a daily schedule.
- **SNS Deep-Link**: Configure SNS to send the actual "Table Summary" in the email body.

---
**Date:** March 2026  
**Status:** Phase 1 Complete - Data Flowing to Cloud 🚀