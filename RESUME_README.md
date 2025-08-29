# Resume Builder

A Python-based tool that generates professional PDF resumes from YAML data with preserved links and ATS-readable formatting.

## Features

- **Header + two-column layout** matching modern resume designs
- **Preserved hyperlinks** in PDF output (email, LinkedIn, portfolio links)
- **ATS-readable formatting** with proper text structure
- **Clean, professional styling** with consistent typography
- **Easy customization** through YAML data file

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate your resume:**
   ```bash
   python resume_generator.py
   ```

   Or use the batch script on Windows:
   ```bash
   generate_resume.bat
   ```

## File Structure

- `resume.yaml` - Your resume data (edit this file with your information)
- `resume_generator.py` - Resume generator script
- `requirements.txt` - Python dependencies
- `generate_resume.bat` - Windows batch script for easy generation

## Generated Files

- `resume.pdf` - Your professional resume with header and two-column layout

## Layout

- **Header** (full width): Name, Title, Contact Info (email•phone, LinkedIn, location), About statement
- **Left Column**: About, Experience, Education
- **Right Column**: Skills, Projects, Portfolio

## YAML Structure

The `resume.yaml` file supports the following structure:

```yaml
name: Your Name
title: Your Job Title
statement: Brief professional statement

contact:
  email: your.email@example.com
  phone: "(123) 456-7890"
  linkedin: https://www.linkedin.com/in/yourprofile
  location: City, State

experience:
  - company: Company Name
    role: Job Title
    location: City, State
    dates: Month Year - Month Year
    details:
      - Achievement or responsibility
      - Another achievement

education:
  - school: University Name
    degree: Degree Type
    location: City, State
    dates: Year

skills:
  languages:
    - Python
    - JavaScript
  concepts:
    - Web Development
    - Data Analysis
  tools:
    - Git
    - Docker
  certifications:
    - Certification Name

projects:
  - Project Name 1
  - Project Name 2

portfolio:
  - GitHub: https://github.com/yourusername
  - YouTube: https://youtube.com/yourchannel
```

## ATS Compatibility

This tool generates PDFs that are optimized for Applicant Tracking Systems (ATS):

- Clean text structure without complex formatting
- Proper heading hierarchy
- Readable fonts and spacing
- Preserved contact links
- Standard section organization

## Customization

You can customize the styling by modifying the `_create_styles()` method in the generator script. The current version includes:

- Modern color scheme
- Professional typography
- Optimized spacing and layout
- Better visual hierarchy

## Links Preservation

Unlike web-based PDF exports, this tool properly preserves all hyperlinks:
- Email links (clickable mailto:)
- LinkedIn profile links
- Portfolio/website links
- All links remain functional in the PDF

## Requirements

- Python 3.7+
- reportlab>=4.0.0
- PyYAML>=6.0

## Usage Tips

1. **Edit the YAML file** with your information
2. **Run the generator** for best results
3. **Check the PDF** in a PDF viewer to verify links work
4. **Customize colors/fonts** in the Python script if needed
5. **Test with ATS systems** by uploading to job boards

The tool generates PDFs that are optimized for both visual appeal and ATS compatibility while maintaining all link functionality.
