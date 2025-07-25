# AI_Recruitement Platform

## Job Description Generator (Task 1)

### Overview

Task 1 requires generating 200 realistic dummy job descriptions across seven domains (Software Engineering, Data Science, DevOps, Machine Learning, Quality Assurance, Project Management, and Business Analytics) using the OpenAI API, with randomized company types, locations, and experience levels.

### Task 1 Processes

1. Setup Environment
- Install Python 3.7+ and required packages: 

```bash
pip install openai python-dotenv.
```
- Configure an OpenAI API key in a .env file: OPENAI_API_KEY=your-openai-api-key


2. Initialize Generator
- Create an instance of JobDescriptionGenerator with the API key:
```bash
import os
from job_description_generator import JobDescriptionGenerator
API_KEY = os.getenv("OPENAI_API_KEY")
generator = JobDescriptionGenerator(API_KEY)
```
3. Generate Single Job Description
- Use generate_single_jd to create a job description for a specific role, category, company type, location, and experience level. Example:
```bash
jd = generator.generate_single_jd(
    role="Data Scientist",
    category="Data Science",
    company_type="SaaS Company",
    location="Remote",
    experience_level="Mid Level"
)
if jd:
    import json
    print(json.dumps(jd, indent=2))
```
4. Generate 200 Job Descriptions
- Use generate_all_job_descriptions to create 200 job descriptions across the specified domains: 

- Software Engineering: Frontend Developer, Backend Developer, Full Stack Developer, etc.

- Data Science: Data Scientist, Data Analyst, Senior Data Scientist, etc.

- DevOps: DevOps Engineer, Site Reliability Engineer, Cloud Specialist, etc.

- Machine Learning: Machine Learning Engineer, AI Researcher, NLP Specialist, etc.

- Quality Assurance: QA Engineer, Test Automation Specialist, QA Manager, etc.

- Project Management: Project Manager, Scrum Master, Product Owner, etc.

- Business Analytics: Business Analyst, BI Specialist, Data Visualization Expert, etc.

```bash
job_descriptions = generator.generate_all_job_descriptions(num_descriptions=200)
```

5. Save Output
- Save the generated job descriptions to a JSON file:
```bash
generator.save_to_json(job_descriptions, "job_descriptions.json")
```
6. Validate and Test
- Validate inputs (roles, categories, etc.) using built-in checks.
- Test API connectivity:

```bash
def test_api_connection(self):
    try:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("API Test Successful:", response.choices[0].message.content)
    except Exception as e:
        print("API Test Failed:", str(e))
```

- Handle rate limits by adding retries in generate_single_jd.























