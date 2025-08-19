#!/usr/bin/env python3
"""
Resume PDF Generator
Generates a professional two-column PDF resume from YAML data
with preserved links and ATS-readable formatting.
"""

import yaml
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, FrameBreak, Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class CustomPageTemplate(PageTemplate):
    """Custom page template that draws a separator line"""
    
    def __init__(self, id, frames, **kwargs):
        PageTemplate.__init__(self, id, frames, **kwargs)
        
    def beforeDrawPage(self, canv, doc):
        """Draw the separator line at the bottom of the header"""
        # Calculate line position (at the bottom of the header)
        margin = 0.5 * inch
        header_height = 1.6 * inch
        # Draw line at the exact bottom of the header area
        line_y = letter[1] - margin - header_height
        
        # Draw horizontal line spanning full width
        canv.setStrokeColorRGB(0.16, 0.5, 0.73)  # #2980B9 in RGB
        canv.setLineWidth(1)
        canv.line(margin, line_y, letter[0] - margin, line_y)


class TwoColumnDocTemplate(BaseDocTemplate):
    """Custom document template with header and two-column layout"""
    
    def __init__(self, filename, **kwargs):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kwargs)
        
        # Define page margins
        margin = 0.5 * inch
        header_height = 1.6 * inch  # Space for header content
        total_width = letter[0] - 3 * margin  # Total available width for columns
        left_col_width = (total_width * 2) / 3   # 2/3 of total width
        right_col_width = total_width / 3        # 1/3 of total width
        
        # Header left frame (2/3 width for name, title, contact info)
        header_left_frame = Frame(
            margin, letter[1] - margin - header_height, left_col_width, header_height,
            leftPadding=0, rightPadding=10, topPadding=0, bottomPadding=0,
            id='header_left'
        )
        
        # Header right frame (1/3 width for image)
        header_right_frame = Frame(
            margin + left_col_width + margin, letter[1] - margin - header_height, right_col_width, header_height,
            leftPadding=10, rightPadding=0, topPadding=0, bottomPadding=0,
            id='header_right'
        )
        
        # Left column frame (2/3 width)
        left_frame = Frame(
            margin, margin, left_col_width, letter[1] - 2 * margin - header_height - 0.3 * inch,
            leftPadding=0, rightPadding=10, topPadding=0, bottomPadding=0,
            id='left'
        )
        
        # Right column frame (1/3 width)
        right_frame = Frame(
            margin + left_col_width + margin, margin, right_col_width, letter[1] - 2 * margin - header_height - 0.3 * inch,
            leftPadding=10, rightPadding=0, topPadding=0, bottomPadding=0,
            id='right'
        )
        
        # Create custom page template that draws the separator line
        template = CustomPageTemplate(id='headertwocol', frames=[header_left_frame, header_right_frame, left_frame, right_frame])
        self.addPageTemplates([template])


class ResumeGenerator:
    def __init__(self, yaml_file, output_file):
        self.yaml_file = yaml_file
        self.output_file = output_file
        self.styles = self._create_styles()
        
    def _create_styles(self):
        """Create custom styles for the resume"""
        styles = getSampleStyleSheet()
        
        # Main heading style
        styles.add(ParagraphStyle(
            name='Name',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=6,
            textColor=HexColor('#2C3E50'),
            fontName='Helvetica-Bold'
        ))
        
        # Title/subtitle style
        styles.add(ParagraphStyle(
            name='JobSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=12,
            textColor=HexColor('#34495E'),
            fontName='Helvetica'
        ))
        
        # Section heading style
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=16,
            spaceAfter=8,
            textColor=HexColor('#2980B9'),
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=HexColor('#2980B9'),
            borderPadding=0,
            leftIndent=0
        ))
        
        # Contact info style
        styles.add(ParagraphStyle(
            name='Contact',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=HexColor('#27AE60'),
            fontName='Helvetica'
        ))
        
        # Job title style
        styles.add(ParagraphStyle(
            name='JobTitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=HexColor('#2C3E50')
        ))
        
        # Company/dates style
        styles.add(ParagraphStyle(
            name='CompanyDates',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica-Oblique',
            textColor=HexColor('#7F8C8D')
        ))
        
        # Bullet point style
        styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            leftIndent=12,
            bulletIndent=0,
            fontName='Helvetica'
        ))
        
        # Skills style
        styles.add(ParagraphStyle(
            name='Skills',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            fontName='Helvetica'
        ))
        
        return styles
    
    def _load_yaml_data(self):
        """Load resume data from YAML file"""
        with open(self.yaml_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def _create_header_left_section(self, data):
        """Create left header with name, title, and contact information"""
        story = []
        
        # Name
        story.append(Paragraph(data['name'], self.styles['Name']))
        
        # Title
        story.append(Paragraph(data['title'], self.styles['JobSubtitle']))
        
        # Contact info - email and phone on same line
        contact = data.get('contact', {})
        contact_line1 = []
        if contact.get('email'):
            contact_line1.append(f'<a href="mailto:{contact["email"]}" color="#27AE60">{contact["email"]}</a>')
        if contact.get('phone'):
            contact_line1.append(contact['phone'])
        
        if contact_line1:
            story.append(Paragraph(' • '.join(contact_line1), self.styles['Contact']))
        
        # LinkedIn on next line
        if contact.get('linkedin'):
            linkedin_text = contact['linkedin'].replace('https://www.linkedin.com/in/', 'linkedin.com/in/')
            story.append(Paragraph(f'<a href="{contact["linkedin"]}" color="#27AE60">{linkedin_text}</a>', self.styles['Contact']))
        
        # Location on next line
        if contact.get('location'):
            story.append(Paragraph(contact['location'], self.styles['Contact']))
        
        return story
    
    def _create_header_right_section(self, data):
        """Create right header with image"""
        story = []
        
        # Check if image path is provided in the data
        image_path = data.get('image')[0]
        if image_path and os.path.exists(image_path):
            try:
                # Create image with appropriate sizing
                img = Image(image_path)
                # Scale image to fit in header (max 1.5 inch width, 1.6 inch height)
                img.drawHeight = 1.5 * inch
                img.drawWidth = 1.5 * inch
                story.append(img)
            except Exception as e:
                # If image fails to load, add a placeholder
                story.append(Paragraph("Image not available", self.styles['Contact']))
        else:
            # Add placeholder text or leave empty
            story.append(Paragraph("img here", self.styles['Contact']))
        
        return story
    
    def _create_skills_section(self, data):
        """Create skills section"""
        story = []
        story.append(Paragraph('SKILLS', self.styles['SectionHeading']))
        
        skills = data.get('skills', {})
        
        if skills.get('languages'):
            story.append(Paragraph('<b>Languages:</b>', self.styles['Skills']))
            story.append(Paragraph(', '.join(skills['languages']), self.styles['Skills']))
            story.append(Spacer(1, 6))
        
        if skills.get('concepts'):
            story.append(Paragraph('<b>Concepts:</b>', self.styles['Skills']))
            story.append(Paragraph(', '.join(skills['concepts']), self.styles['Skills']))
            story.append(Spacer(1, 6))
        
        if skills.get('tools'):
            story.append(Paragraph('<b>Tools:</b>', self.styles['Skills']))
            story.append(Paragraph(', '.join(skills['tools']), self.styles['Skills']))
            story.append(Spacer(1, 6))
        
        if skills.get('certifications'):
            story.append(Paragraph('<b>Certifications:</b>', self.styles['Skills']))
            story.append(Paragraph(', '.join(skills['certifications']), self.styles['Skills']))
        
        return story
    
    def _create_education_section(self, data):
        """Create education section"""
        story = []
        story.append(Paragraph('EDUCATION', self.styles['SectionHeading']))
        
        education = data.get('education', [])
        for edu in education:
            story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['JobTitle']))
            story.append(Paragraph(f"{edu['school']}, {edu['location']}", self.styles['CompanyDates']))
            if edu.get('dates'):
                story.append(Paragraph(edu['dates'], self.styles['CompanyDates']))
            story.append(Spacer(1, 8))
        
        return story
    
    def _create_about_section(self, data):
        """Create about/statement section"""
        story = []
        if data.get('statement'):
            story.append(Paragraph('ABOUT', self.styles['SectionHeading']))
            story.append(Paragraph(data['statement'], self.styles['Normal']))
        return story
    
    def _create_experience_section(self, data):
        """Create experience section"""
        story = []
        story.append(Paragraph('EXPERIENCE', self.styles['SectionHeading']))
        
        experience = data.get('experience', [])
        for exp in experience:
            # Job title and company
            story.append(Paragraph(f"{exp['role']} — {exp['company']}", self.styles['JobTitle']))
            
            # Location and dates
            location_dates = f"{exp.get('location', '')}"
            if exp.get('dates'):
                location_dates += f" • {exp['dates']}"
            story.append(Paragraph(location_dates, self.styles['CompanyDates']))
            
            # Details/bullet points
            if exp.get('details'):
                for detail in exp['details']:
                    story.append(Paragraph(f"• {detail}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 12))
        
        return story
    
    def _create_projects_section(self, data):
        """Create projects section"""
        story = []
        projects = data.get('projects', [])
        if projects:
            story.append(Paragraph('PROJECTS', self.styles['SectionHeading']))
            
            for project in projects:
                if isinstance(project, str):
                    story.append(Paragraph(f"• {project}", self.styles['BulletPoint']))
                else:
                    # Handle more complex project structure if needed
                    story.append(Paragraph(f"• {project.get('name', str(project))}", self.styles['BulletPoint']))
        
        # Portfolio links
        portfolio = data.get('portfolio', [])
        if portfolio:
            story.append(Paragraph('PORTFOLIO', self.styles['SectionHeading']))
            for item in portfolio:
                if isinstance(item, dict):
                    for platform, url in item.items():
                        story.append(Paragraph(f'<a href="{url}" color="#2980B9">{platform}</a>', self.styles['Skills']))
                elif isinstance(item, str):
                    # Handle simple string entries
                    if item.startswith('http'):
                        # Extract platform name from URL
                        platform = item.split('//')[1].split('/')[0].replace('www.', '').split('.')[0].title()
                        story.append(Paragraph(f'<a href="{item}" color="#2980B9">{platform}</a>', self.styles['Skills']))
                    else:
                        story.append(Paragraph(item, self.styles['Skills']))
        
        return story
    
    def generate_pdf(self):
        """Generate the PDF resume with two-column header and body"""
        data = self._load_yaml_data()
        
        # Create document
        doc = TwoColumnDocTemplate(self.output_file, pagesize=letter)
        
        # Build story elements
        story = []
        
        # Header left section (name, title, contact)
        story.extend(self._create_header_left_section(data))
        
        # Frame break to move to header right section
        story.append(FrameBreak())
        
        # Header right section (image)
        story.extend(self._create_header_right_section(data))
        
        # Frame break to move to left column
        story.append(FrameBreak())
        
        # Left column content
        story.extend(self._create_about_section(data))
        story.extend(self._create_experience_section(data))
        story.extend(self._create_education_section(data))
        
        # Frame break to move to right column
        story.append(FrameBreak())
        
        # Right column content
        story.extend(self._create_skills_section(data))
        story.extend(self._create_projects_section(data))
        
        # Build PDF
        doc.build(story)
        print(f"Resume generated successfully: {self.output_file}")


def main():
    """Main function"""
    yaml_file = "resume.yaml"
    output_file = "resume.pdf"
    
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found!")
        return
    
    generator = ResumeGenerator(yaml_file, output_file)
    generator.generate_pdf()


if __name__ == "__main__":
    main()
