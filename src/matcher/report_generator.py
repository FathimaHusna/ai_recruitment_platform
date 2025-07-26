import io
import pandas as pd
from typing import List
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .models import JobMatch

class ReportGenerator:
    """Generate PDF and CSV reports"""
    
    @staticmethod
    def generate_pdf_report(matches: List[JobMatch], resume_name: str) -> bytes:
        """Generate PDF report of job matches"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        story.append(Paragraph(f"Job Recommendations for {resume_name}", title_style))
        story.append(Spacer(1, 20))
        
        summary_text = f"Generated on: {datetime.now().strftime('%B %d, %Y')}<br/>Total Matches: {len(matches)}"
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        for i, match in enumerate(matches, 1):
            job_header = f"{i}. {match.title} - {match.company_type}"
            story.append(Paragraph(job_header, styles['Heading2']))
            
            details = f"""
            <b>Category:</b> {match.category}<br/>
            <b>Location:</b> {match.location}<br/>
            <b>Compatibility:</b> {match.similarity_score:.1%}<br/>
            <b>Salary Range:</b> {match.salary_range}<br/>
            """
            story.append(Paragraph(details, styles['Normal']))
            
            if match.match_reasons:
                reasons_text = "<b>Why this matches:</b><br/>" + "<br/>".join([f"• {reason}" for reason in match.match_reasons])
                story.append(Paragraph(reasons_text, styles['Normal']))
            
            if match.matching_skills:
                skills_text = f"<b>Matching Skills:</b> {', '.join(match.matching_skills[:5])}"
                story.append(Paragraph(skills_text, styles['Normal']))
            
            story.append(Spacer(1, 15))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def generate_csv_report(matches: List[JobMatch]) -> str:
        """Generate CSV report of job matches"""
        data = []
        for match in matches:
            data.append({
                'Job Title': match.title,
                'Category': match.category,
                'Company Type': match.company_type,
                'Location': match.location,
                'Compatibility Score': f"{match.similarity_score:.1%}",
                'Salary Range': match.salary_range,
                'Matching Skills': '; '.join(match.matching_skills),
                'Missing Skills': '; '.join(match.missing_skills),
                'Match Reasons': '; '.join(match.match_reasons),
                'Job Summary': match.job_summary[:200] + '...' if len(match.job_summary) > 200 else match.job_summary
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)