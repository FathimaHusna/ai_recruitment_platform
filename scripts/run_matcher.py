import streamlit as st
from datetime import datetime
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.matcher.job_matcher import RAGJobMatcher
from src.matcher.resume_processor import ResumeProcessor
from src.matcher.report_generator import ReportGenerator
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_page_config():
    """Initialize page configuration with enhanced styling"""
    st.set_page_config(
        page_title="TalentMatch AI - Smart Recruitment Platform",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def load_custom_css():
    """Load enhanced custom CSS for better UI/UX"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .hero-section {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    /* Card Styles */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    .info-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 1.25rem;
        border-left: 4px solid #3b82f6;
        margin: 0.75rem 0;
    }
    
    .info-card h4 {
        color: #1e293b;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    /* Job Card Styles */
    .job-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .job-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    .job-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 30px rgba(59,130,246,0.15);
        transform: translateY(-2px);
    }
    
    .job-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .compatibility-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(16,185,129,0.3);
    }
    
    /* Skill Tags */
    .skill-tag {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        color: #1e40af;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #93c5fd;
        transition: all 0.2s ease;
    }
    
    .skill-tag:hover {
        background: linear-gradient(135deg, #bfdbfe, #93c5fd);
        transform: translateY(-1px);
    }
    
    .missing-skill-tag {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #dc2626;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #fca5a5;
    }
    
    .category-tag {
        background: linear-gradient(135deg, #e0f2fe, #b3e5fc);
        color: #0277bd;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .company-tag {
        background: linear-gradient(135deg, #f3e5f5, #e1bee7);
        color: #7b1fa2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    /* Progress Indicators */
    .progress-step {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e2e8f0;
        color: #64748b;
        font-weight: 600;
        margin: 0 auto 1rem auto;
        transition: all 0.3s ease;
    }
    
    .progress-step.active {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    }
    
    .progress-step.completed {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .modern-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_hero_section():
    """Display the hero section"""
    st.markdown("""
    <div class="hero-section fade-in-up">
        <div class="hero-title">🎯 TalentMatch AI</div>
        <div class="hero-subtitle">Transform your career with AI-powered job matching</div>
        <p style="font-size: 1rem; opacity: 0.8; margin-top: 1rem;">
            Upload your resume and discover personalized job opportunities that match your skills and aspirations
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_progress_indicator(current_step):
    """Display progress indicator"""
    steps = [
        ("1", "Upload Resume", "upload"),
        ("2", "Process & Extract", "process"),
        ("3", "Find Matches", "matches"),
        ("4", "View Results", "results")
    ]
    
    cols = st.columns(4)
    for i, (num, label, key) in enumerate(steps):
        with cols[i]:
            if i < current_step:
                status_class = "completed"
                icon = "✓"
            elif i == current_step:
                status_class = "active"
                icon = num
            else:
                status_class = ""
                icon = num
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="progress-step {status_class}">{icon}</div>
                <div style="font-size: 0.9rem; font-weight: 500; color: {'#3b82f6' if i <= current_step else '#64748b'};">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

def validate_environment():
    """Validate environment variables silently"""
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    database_name = os.getenv("DATABASE_NAME", "recruitment_platform")
    
    if not openai_api_key or not mongo_uri:
        st.error("🚫 Service temporarily unavailable. Please try again later.")
        logger.error("Missing OPENAI_API_KEY or MONGO_URI in environment variables.")
        st.stop()
    
    # Test MongoDB connection silently
    try:
        client = MongoClient(mongo_uri, server_api=ServerApi('1'), tls=True, tlsCAFile=certifi.where())
        client.admin.command('ping')
        client.close()
    except Exception as e:
        st.error("🚫 Service temporarily unavailable. Please try again later.")
        logger.error(f"MongoDB connection error: {e}")
        st.stop()
    
    return openai_api_key, mongo_uri, database_name

def display_resume_upload():
    """Display enhanced resume upload section"""
    st.markdown("""
    <div class="upload-section">
        <h3 style="color: #1e293b; margin-bottom: 1rem;">📄 Upload Your Resume</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Upload your resume in PDF, DOCX, or TXT format to get started
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Maximum file size: 10MB",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button("🚀 Process Resume", type="primary", use_container_width=True)
    
    return uploaded_file, process_button

def display_resume_info(resume):
    """Display extracted resume information in modern cards"""
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h4>👤 Contact Information</h4>
            <p><strong>Name:</strong> {resume.name or 'Not provided'}</p>
            <p><strong>Email:</strong> {resume.email or 'Not provided'}</p>
            <p><strong>Phone:</strong> {resume.phone or 'Not provided'}</p>
            <p><strong>Location:</strong> {resume.location or 'Not provided'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <h4>💼 Professional Summary</h4>
            <p><strong>Experience:</strong> {resume.experience_years} years</p>
            <p><strong>Summary:</strong> {resume.summary[:120] + '...' if len(resume.summary) > 120 else resume.summary}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="info-card">
            <h4>🎓 Qualifications</h4>
            <p><strong>Education:</strong> {len(resume.education)} qualification(s)</p>
            <p><strong>Certifications:</strong> {len(resume.certifications)} certificate(s)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Skills section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Technical Skills")
        if resume.technical_skills:
            skills_html = "".join([f"<span class='skill-tag'>{skill}</span>" for skill in resume.technical_skills])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No technical skills extracted")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 🤝 Soft Skills")
        if resume.soft_skills:
            skills_html = "".join([f"<span class='skill-tag'>{skill}</span>" for skill in resume.soft_skills])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No soft skills extracted")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_job_matches(matches):
    """Display job matches with enhanced UI"""
    if not matches:
        st.warning("⚠️ No matching jobs found. Try adjusting your search criteria.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <span class="metric-value">{len(matches)}</span>
            <div class="metric-label">Total Matches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = np.mean([match.similarity_score for match in matches])
        st.markdown(f"""
        <div class="metric-container">
            <span class="metric-value">{avg_score:.0%}</span>
            <div class="metric-label">Avg. Compatibility</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        categories = len(set([match.category for match in matches]))
        st.markdown(f"""
        <div class="metric-container">
            <span class="metric-value">{categories}</span>
            <div class="metric-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        locations = len(set([match.location for match in matches]))
        st.markdown(f"""
        <div class="metric-container">
            <span class="metric-value">{locations}</span>
            <div class="metric-label">Locations</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filters
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 🔧 Filter Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        categories = sorted(set([match.category for match in matches]))
        selected_category = st.selectbox("Category", ["All"] + categories)
    with col2:
        locations = sorted(set([match.location for match in matches]))
        selected_location = st.selectbox("Location", ["All"] + locations)
    with col3:
        min_score = st.slider("Minimum Compatibility", 0.0, 1.0, 0.0, 0.05)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_matches = matches
    if selected_category != "All":
        filtered_matches = [m for m in filtered_matches if m.category == selected_category]
    if selected_location != "All":
        filtered_matches = [m for m in filtered_matches if m.location == selected_location]
    filtered_matches = [m for m in filtered_matches if m.similarity_score >= min_score]
    
    if not filtered_matches:
        st.info("🔍 No jobs match the selected filters. Try adjusting your criteria.")
        return
    
    # Display job cards
    for i, match in enumerate(filtered_matches):
        st.markdown(f"""
        <div class="job-card fade-in-up">
            <div class="job-title">
                🏢 {match.title}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <div>
                    <span class="category-tag">{match.category}</span>
                    <span class="company-tag">{match.company_type}</span>
                </div>
                <div class="compatibility-badge">
                    {match.similarity_score:.0%} Match
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📍 Location:** {match.location}")
            st.markdown(f"**💰 Salary:** {match.salary_range}")
            
            if match.job_summary:
                st.markdown(f"**📝 Job Summary:**")
                st.markdown(f"{match.job_summary[:300]}...")
            
            if match.match_reasons:
                st.markdown("**✨ Why this matches you:**")
                for reason in match.match_reasons[:3]:
                    st.markdown(f"• {reason}")
        
        with col2:
            if match.matching_skills:
                st.markdown("**✅ Your Matching Skills:**")
                skills_html = "".join([f"<span class='skill-tag'>{skill}</span>" 
                                     for skill in match.matching_skills[:6]])
                st.markdown(skills_html, unsafe_allow_html=True)
            
            if match.missing_skills:
                st.markdown("**📚 Skills to Develop:**")
                missing_skills_html = "".join([f"<span class='missing-skill-tag'>{skill}</span>" 
                                              for skill in match.missing_skills[:4]])
                st.markdown(missing_skills_html, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    return filtered_matches

def display_export_section(filtered_matches, resume_name):
    """Display export options"""
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Export Your Results")
    st.markdown("Download your personalized job match report in your preferred format.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            pdf_data = ReportGenerator.generate_pdf_report(filtered_matches, resume_name)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name=f"job_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error("PDF generation temporarily unavailable")
            logger.error(f"PDF generation error: {e}")
    
    with col2:
        try:
            csv_data = ReportGenerator.generate_csv_report(filtered_matches)
            st.download_button(
                label="📊 Download CSV Report",
                data=csv_data,
                file_name=f"job_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        except Exception as e:
            st.error("CSV generation temporarily unavailable")
            logger.error(f"CSV generation error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main Streamlit application with enhanced UI/UX"""
    init_page_config()
    load_custom_css()
    
    # Validate environment silently
    openai_api_key, mongo_uri, database_name = validate_environment()
    
    # Hero section
    display_hero_section()
    
    # Determine current step
    current_step = 0
    if st.session_state.get('processed_resume'):
        current_step = 1
    if st.session_state.get('job_matches'):
        current_step = 3
    
    # Progress indicator
    display_progress_indicator(current_step)
    
    # Advanced settings in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Advanced Settings")
        top_k_jobs = st.slider("Number of Job Matches", 5, 20, 10, 
                              help="Select how many job recommendations to display")
        
        st.markdown("### 📊 Quick Stats")
        if st.session_state.get('processed_resume'):
            resume = st.session_state.processed_resume
            st.metric("Technical Skills", len(resume.technical_skills))
            st.metric("Experience", f"{resume.experience_years} years")
            st.metric("Certifications", len(resume.certifications))
    
    # Main content
    if current_step == 0:
        uploaded_file, process_button = display_resume_upload()
        
        if uploaded_file and process_button:
            with st.spinner("🔄 Processing your resume... This may take a moment."):
                try:
                    # Initialize matcher
                    matcher = RAGJobMatcher(openai_api_key, mongo_uri, database_name)
                    
                    # Extract text based on file type
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    if file_extension == 'pdf':
                        resume_text = ResumeProcessor.extract_text_from_pdf(uploaded_file)
                    elif file_extension == 'docx':
                        resume_text = ResumeProcessor.extract_text_from_docx(uploaded_file)
                    elif file_extension == 'txt':
                        resume_text = ResumeProcessor.extract_text_from_txt(uploaded_file)
                    else:
                        st.error("❌ Unsupported file format")
                        st.stop()
                    
                    if not resume_text.strip():
                        st.error("❌ Could not extract text from the resume. Please check the file format and try again.")
                        st.stop()
                    
                    # Process with LLM
                    processed_resume = matcher.process_resume_with_llm(resume_text)
                    if processed_resume:
                        st.session_state.processed_resume = processed_resume
                        st.success("✅ Resume processed successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to process resume. Please try again.")
                        
                except Exception as e:
                    st.error("❌ An error occurred while processing your resume. Please try again.")
                    logger.error(f"Resume processing error: {e}")
    
    elif current_step >= 1:
        st.markdown("## 👤 Resume Analysis Results")
        display_resume_info(st.session_state.processed_resume)
        
        st.markdown("## 🎯 Find Your Perfect Match")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True):
                with st.spinner("🔄 Searching for the best job matches... This may take a moment."):
                    try:
                        matcher = RAGJobMatcher(openai_api_key, mongo_uri, database_name)
                        job_matches = matcher.find_matching_jobs(st.session_state.processed_resume, top_k_jobs)
                        st.session_state.job_matches = job_matches
                        
                        if job_matches:
                            st.success(f"✅ Found {len(job_matches)} amazing job matches for you!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("⚠️ No matching jobs found. Try adjusting your search criteria.")
                    
                    except Exception as e:
                        st.error("❌ An error occurred while searching for jobs. Please try again.")
                        logger.error(f"Job matching error: {e}")
    
    if st.session_state.get('job_matches'):
        st.markdown("## 💼 Your Personalized Job Recommendations")
        filtered_matches = display_job_matches(st.session_state.job_matches)
        
        if filtered_matches:
            display_export_section(filtered_matches, st.session_state.processed_resume.name)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 3rem;">
        <p style="margin: 0; font-size: 0.9rem;">
            🚀 <strong>TalentMatch AI</strong> - Revolutionizing recruitment with artificial intelligence
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.7;">
            Powered by OpenAI GPT & Advanced Vector Search Technology
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()