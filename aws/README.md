# AWS Lambda Migration - LeagueStat

This folder contains the AWS Lambda-ready components for the LeagueStat project. It replaces local `.env` and SQLite usage with secure, scalable AWS services: **Secrets Manager**, **RDS (MySQL)**, and **Lambda** for automated scraping.

----------------------------------------------------------------------

## 📁 Folder Overview

| File | Purpose |
|------|---------|
| `lambda_function.py`    | Main AWS Lambda entry point. Logs in, scrapes match data, inserts into RDS |
| `aws_secrets.py`        | Helper to retrieve credentials securely from AWS Secrets Manager |
| `database_rds.py`       | Handles database connection to MySQL RDS instance |
| `requirements.txt`      | Minimal dependencies for AWS Lambda packaging |
| `zip_lambda.sh`         | Shell script to build and zip the Lambda deployment package |

----------------------------------------------------------------------

## 🌐 Lambda Environment Variables

Set these in the AWS Lambda console under **Configuration → Environment variables**:

| Key       | Description                |
|-----------|----------------------------|
| `RDS_HOST` | RDS endpoint URL           |
| `RDS_USER` | MySQL username             |
| `RDS_PASS` | MySQL password             |

----------------------------------------------------------------------

## 💻 Local Testing (Optional)

Create a `.env` file in this folder:

```env
RDS_HOST=your-rds-endpoint.amazonaws.com
RDS_USER=your-db-user
RDS_PASS=your-db-password