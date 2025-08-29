# Resume Builder - LaTeX Edition

A professional resume and cover letter generator using LaTeX templates for high-quality PDF output.

## Overview

This project generates professional resumes and cover letters using LaTeX templates. It provides ATS-friendly formatting with a clean, modern design featuring a two-column header with profile image and single-column body layout.

## Features

- **LaTeX-based rendering** for professional typography and consistent formatting
- **Two-column header** with profile image support
- **Single-column body** for optimal readability and ATS compatibility
- **Automated build system** with Python script
- **ATS compatibility testing** with detailed analysis
- **Modular template system** for easy customization
- **AI-powered content tailoring** using structured prompts

## Project Structure

```
├── src/                           # Source code
│   ├── build.py                   # Main build script for LaTeX compilation
│   ├── ats_tester.py             # ATS compatibility analyzer
│   └── resume_generator.py       # Legacy Python-based generator
├── resources/                     # Templates and assets
│   ├── templates/                 # LaTeX templates
│   │   ├── resume.tex            # Main resume template
│   │   ├── coverletter_template.tex # Cover letter template
│   │   └── coverletter.tex       # Generated cover letter (optional)
│   ├── prompts/                   # AI assistance prompts
│   │   ├── ResumePrompt.txt      # Resume tailoring instructions
│   │   └── coverLetterPrompt.txt # Cover letter generation instructions
│   └── images/                    # Profile images and assets
│       └── profile.png           # Profile photo
├── output/                        # Generated PDF files
├── temp/                          # Temporary compilation files
├── generate_resume.bat           # Windows batch file for easy building
├── test_ats.bat                  # Windows batch file for ATS testing
└── requirements.txt              # Python dependencies
```

## Quick Start

### Windows (Batch Files)
```bash
# Generate resume and cover letter
.\generate_resume.bat

# Test ATS compatibility
.\test_ats.bat
```

### Manual Usage

#### Build Documents
```bash
# Install dependencies
pip install -r requirements.txt

# Build all documents (resume + cover letter)
python src/build.py

# Build specific document
python src/build.py resume
python src/build.py coverletter

# Clean temporary files
python src/build.py clean
```

#### Test ATS Compatibility
```bash
# Test default resume.pdf in output directory
python src/ats_tester.py

# Test specific PDF file
python src/ats_tester.py path/to/resume.pdf
```

## Usage Workflow

### 1. Edit Templates
- Modify `resources/templates/resume.tex` with your information
- Use `resources/templates/coverletter_template.tex` as base for cover letters

### 2. Build PDFs
- Run `python src/build.py` to compile LaTeX templates to PDF
- Output files are saved in `output/` directory

### 3. Test ATS Compatibility
- Run `python src/ats_tester.py` to analyze resume for ATS compatibility
- Get detailed feedback and recommendations

### 4. AI-Assisted Tailoring
Use the prompts in `resources/prompts/` with your preferred AI assistant to:
- Tailor resume content to specific job descriptions
- Generate customized cover letters
- Maintain consistent formatting and professional tone

## Technical Requirements

### LaTeX Distribution
- **Windows**: MiKTeX or TeX Live
- **macOS**: MacTeX
- **Linux**: TeX Live

### Python Packages
```bash
pip install pdfplumber  # For ATS testing
```

### Required LaTeX Packages
- `geometry` - Page layout
- `graphicx` - Image handling
- `hyperref` - Clickable links
- `xcolor` - Color definitions
- `enumitem` - List formatting
- `array` - Table formatting

## Customization

### Colors
Edit the color definitions in the LaTeX templates:
```latex
\definecolor{primary}{HTML}{2C3E50}    % Dark blue-gray
\definecolor{accent}{HTML}{2980B9}     % Blue
\definecolor{contact}{HTML}{27AE60}    % Green
\definecolor{subtitle}{HTML}{34495E}   % Gray
```

### Layout
Modify spacing, fonts, and section layouts in the template files under `resources/templates/`.

### Images
Replace `resources/images/profile.png` with your profile photo.

## Build System Features

The `src/build.py` script provides:
- **Automatic LaTeX compilation** with error handling
- **Multi-pass compilation** for complex documents
- **Temporary file management** 
- **Output organization** in dedicated directory
- **Command-line options** for specific builds

## ATS Testing Features

The `src/ats_tester.py` script analyzes:
- **Text extraction quality** from PDF
- **Contact information presence** 
- **Standard section headers**
- **Formatting compatibility**
- **Content quality metrics**
- **Overall compatibility score** (0-100)

## Legacy Components

- `src/resume_generator.py` - Python-based PDF generator using ReportLab
- Maintained for backward compatibility but LaTeX approach is recommended

## Design Features

- **Professional color scheme** using corporate blues and greens
- **ATS-friendly formatting** with proper heading structure
- **Clickable links** for email, LinkedIn, GitHub, and project URLs
- **Clean typography** with appropriate spacing and hierarchy
- **Responsive layout** that works well on different page sizes
