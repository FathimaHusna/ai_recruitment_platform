# Recruitment Platform - Task 3: Job Matching and User Interface

## Introduction

- Task 3 develops an AI-powered recruitment platform as a Streamlit web application, enabling users to upload resumes, process them with an LLM, and receive job recommendations using Retrieval Augmented Generation (RAG). Resumes (PDF, DOCX, TXT) are parsed using OpenAI’s API, stored in MongoDB Atlas, and matched against job descriptions from Task 2 using RAG with TF-IDF vectorization and LLM-generated match reasons. The app features an intuitive, responsive UI for displaying results and exporting reports in PDF/CSV formats, streamlining the job search process.

## Key Processes

### 1. Resume Upload:

- Users upload resume files (PDF, DOCX, TXT) via the Streamlit UI.

- Validates file formats and provides user feedback.

#### Output: Uploaded resume file.

### 2. CV Processing:

- The ResumeProcessor class extracts text from resumes using PyPDF2 or python-docx.

- Uses OpenAI’s API to parse text into structured data (e.g., name, email, technical/soft skills, experience).

- Stores processed resumes in MongoDB Atlas recruitment_platform.resumes.

#### Output: A ProcessedResume object stored in MongoDB.

### 3. Job Recommendation:

- The RAGJobMatcher class retrieves job descriptions from MongoDB Atlas recruitment_platform.job_descriptions.

- Uses RAG: TF-IDF vectorization for similarity scoring, augmented with LLM-generated match reasons.

- Returns the top-k matching jobs based on skills, experience, and keywords.

#### Output: A list of JobMatch objects with job details, scores, and match reasons.

4. Result Display and Export:

- Displays extracted resume details and job matches in a responsive UI with filters (category, location, compatibility score).

- The ReportGenerator class creates PDF and CSV reports for download.

#### Output: Interactive UI and downloadable PDF/CSV reports.