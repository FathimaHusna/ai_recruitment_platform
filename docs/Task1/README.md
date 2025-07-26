# Recruitment Platform - Task 1: Project Setup and Data Processing Foundation

## Introduction

- Task 1 involves generating 200 dummy job descriptions across various domains using the ChatGPT API, as the first step in building an AI-powered recruitment platform. The job descriptions cover roles in Software Engineering, Data Science, DevOps, Machine Learning, Quality Assurance, Project Management, and Business Analytics. Each description includes fields like title, responsibilities, required skills, experience, location, and salary range, saved as JSON files for use in subsequent tasks. This phase establishes a dataset of realistic job listings to enable resume processing and job matching in Tasks 2 and 3.

## Key Processes

### 1. Job Description Generation:

- Uses the ChatGPT API (via OpenAI’s Python client) to generate realistic job descriptions.

- Covers domains: Software Engineering (e.g., frontend, backend, full-stack developers), Data Science (e.g., data scientists, analysts), DevOps (e.g., DevOps engineers, SREs), Machine Learning (e.g., ML engineers, NLP specialists), Quality Assurance (e.g., QA engineers, test automation specialists), Project Management (e.g., project managers, scrum masters), and Business Analytics (e.g., business analysts, BI specialists).

- Each description includes title, category, company type, location, technical/soft skills, responsibilities, keywords, job summary, salary range, and experience years.

#### Output: 200 JSON files containing structured job descriptions.

### 2. Data Validation:

- Validates generated job descriptions to ensure completeness and consistency.

- Uses Pydantic models to enforce required fields and data types.

#### Output: Validated JobListing objects.

### 3. File Storage:

- Saves job descriptions as JSON files in a designated directory.

- Organizes files by domain for easy access in Task 2.

#### Output: JSON files stored in data/job_descriptions_dataset.json








