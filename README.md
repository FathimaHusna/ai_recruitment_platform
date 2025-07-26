# ecruitment Platform - Task 2: Job Description Processor
## Task 3 Description
- Task 3 involves developing an AI-powered recruitment platform that automates job matching by processing resumes and matching them against job listings. Built using Streamlit, OpenAI, and MongoDB Atlas, the application allows users to upload a resume (PDF, DOCX, or TXT), extracts structured information using OpenAI’s language models, and matches it to job descriptions stored in a MongoDB database. The platform provides tailored job recommendations with compatibility scores, matching skills, and exportable reports in PDF and CSV formats. The goal is to streamline the job search process with an intuitive UI and robust AI-driven matching.

## Key Processes

### 1. Resume Processing:
- Users upload a resume file (PDF, DOCX, or TXT).
- The ResumeProcessor class extracts text and uses OpenAI’s API to parse it into structured data (e.g., name, email, technical skills, experience years)
#### Output: A ProcessedResume object containing extracted information.



### 2. Job Matching:
- The RAGJobMatcher class loads job listings from a MongoDB Atlas job_descriptions collection.

- Uses TF-IDF vectorization and cosine similarity to compute compatibility scores between the resume and jobs based on skills, experience, and keywords.

- Generates match reasons using OpenAI’s language model.



#### Output: A list of JobMatch objects with job details, scores, and matching/missing skills.



### 3. Report Generation:
- The ReportGenerator class creates PDF and CSV reports of job matches.

- Reports include job titles, compatibility scores, locations, salaries, and match reasons.

- Users can download reports via the Streamlit UI.

















