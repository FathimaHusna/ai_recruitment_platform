# Recruitment Platform - Task 2: Job Description Processing and Database Storage

## Introduction

- Task 2 focuses on processing 200 job descriptions generated in Task 1 using an LLM (OpenAI’s ChatGPT) to extract structured data and store it in MongoDB Atlas. The extracted information includes job title, responsibilities, required skills, experience, location, and salary range. This phase builds on Task 1’s job description dataset and sets up the MongoDB database for job matching in Task 3, ensuring efficient data storage and retrieval for the AI-powered recruitment platform.

## Key Processes

### 1. Job Description Input:

- Loads 200 JSON job descriptions from data/job_descriptions/.

- Validates data using Pydantic models.

#### Output: List of validated JobListing objects.

### 2. LLM Processing:

- Uses OpenAI’s ChatGPT API to extract structured data (e.g., title, technical/soft skills, responsibilities, experience, location, salary).

- Ensures consistency and completeness of extracted fields.

#### Output: Structured JobListing objects with parsed data.

3. MongoDB Storage:

- Stores processed job descriptions in MongoDB Atlas recruitment_platform.job_descriptions.

- Creates indexes for efficient querying (e.g., on title, technical_skills).

#### Output: Populated MongoDB collection with 200 job descriptions.