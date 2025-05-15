# 🏥 Healthcare Database Analytics Project

This project models and analyzes healthcare provider data using a normalized SQL schema, an ETL pipeline in Python, and an interactive dashboard built with Streamlit. It simulates real-world workflows—starting from raw CSV ingestion to a cloud-hosted Oracle Autonomous Data Warehouse (ADW), enabling SQL-based analytics and visual storytelling.

---

##  Project Structure

healthcare_db_analytics_project/
├── data/ # Raw and cleaned data, SQL files, metadata
│ ├── raw_csv/
│ ├── clean_csv/
│ ├── dataframes.pkl
│ ├── query_long_descriptions.txt
│ └── sql_files/
│
├── docs/ # GitHub Pages site
│ ├── assets/
│ ├── notebooks/ # Rendered HTML notebooks for ETL walkthrough
│ ├── sql_files/
│ ├── demo.html
│ └── index.md
│
├── streamlit_dashboard/ # Interactive dashboard
│ ├── dashboard.py
│ └── requirements.txt
│
├── .gitignore
├── LICENSE
├── README.md
└── .env.example # Environment variable template


---

## 🗃️ Dataset

- **Source**: [Kaggle – Healthcare Management System](https://www.kaggle.com/datasets/anouskaabhisikta/healthcare-management-system)
- **Tables Modeled**:
  - `PATIENT`
  - `DOCTOR`
  - `APPOINTMENT`
  - `BILLING`
  - `MEDICAL_PROCEDURE`

---

## ⚙️ Technologies Used

| Purpose          | Tool                         |
|------------------|------------------------------|
| Data Processing  | Python (Pandas, NumPy)       |
| ETL + SQL        | Oracle ADW + `oracledb`      |
| Dashboard        | Streamlit                    |
| Hosting          | GitHub Pages, Streamlit Cloud|
| Styling          | HTML + Cayman CSS            |

---

## 🔄 Workflow Overview

### 1. **ETL Pipeline** (`notebooks/`)
- Load raw CSVs, inspect and clean data
- Standardize datatypes and resolve referential integrity
- Format tables for SQL compatibility
- Output: Clean `.csv`, `.pkl`, and metadata `.txt`

### 2. **Schema & Load to Oracle ADW**
- Define relational schema using SQL DDL
- Upload clean data to Oracle using parameterized INSERTs
- Use `.env` for secure credential management

### 3. **SQL Analytics**
- Write analytical queries (stored in `sql_files/`)
- Build views for reuse (e.g., patient billing, doctor procedures)
- Maintain human-readable descriptions (`query_long_descriptions.txt`)

### 4. **Dashboard Interface**
- Use Streamlit to present query results visually
- Embed charts, KPIs, and filters for exploration
- Deploy via Streamlit Cloud

---

## 🌐 Live Demos

- 📊 **Interactive Dashboard**: [Streamlit App](https://share.streamlit.io/...) *(Coming Soon)*
- 🧾 **GitHub Pages Site**: [Project Overview](https://matthew-martin1184.github.io/healthcare_db_analytics_project/)

---

## 🔐 Security

- Sensitive credentials are stored in a local `.env` file
- `.env.example` provided for guidance
- `.gitignore` excludes real credentials
- Read-only demo credentials available upon request

---

## 🧠 Key Learning Outcomes

- Design and implementation of normalized SQL schemas
- Secure and automated ETL pipeline development
- Integration of cloud databases with Python applications
- Dashboard deployment for SQL-driven analysis

---

## 📬 Contact

**Matthew Martin**  
Graduate Student, M.S. in Analytics  
📫 [mattmartin1184@gmail.com](mailto:mattmartin1184@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/matthew-martin1184/)

---
