# Resume Builder - LaTeX Edition

A professional resume and cover letter generator using LaTeX templates for high-quality PDF output.

## Overview

This project generates professional resumes and cover letters from structured data using LaTeX templates. It provides ATS-friendly formatting with a clean, modern design featuring a two-column header with profile image and single-column body layout.

## Features

- **LaTeX-based rendering** for professional typography and consistent formatting
- **Two-column header** with profile image support
- **Single-column body** for optimal readability and ATS compatibility
- **Modular template system** for easy customization
- **AI-powered content tailoring** using structured prompts

## Project Structure

```
├── latex/
│   ├── resume.tex              # Main resume LaTeX template
│   ├── coverletter_template.tex # Cover letter LaTeX template
│   └── coverletter.tex         # Generated cover letter
├── prompts/
│   ├── ResumePrompt.txt        # Instructions for resume tailoring
│   └── coverLetterPrompt.txt   # Instructions for cover letter generation
├── resume.yaml                 # Resume data (legacy format)
├── resume_generator.py         # Python-based PDF generator (legacy)
└── profile.png                # Profile image
```

## Usage

### Resume Generation

1. **Edit the LaTeX template**: Modify `latex/resume.tex` with your information
2. **Compile to PDF**: Use any LaTeX compiler (pdflatex, xelatex, etc.)
   ```bash
   pdflatex latex/resume.tex
   ```

### Cover Letter Generation

1. **Use the template**: Reference `latex/coverletter_template.tex`
2. **Follow the prompt**: Use `prompts/coverLetterPrompt.txt` for AI-assisted generation
3. **Compile to PDF**: 
   ```bash
   pdflatex latex/coverletter.tex
   ```

### AI-Assisted Tailoring

Use the prompts in the `prompts/` directory with your preferred AI assistant to:
- Tailor resume content to specific job descriptions
- Generate customized cover letters
- Maintain consistent formatting and professional tone

## Technical Requirements

- LaTeX distribution (TeX Live, MiKTeX, etc.)
- Required LaTeX packages:
  - `geometry` - Page layout
  - `graphicx` - Image handling
  - `hyperref` - Clickable links
  - `xcolor` - Color definitions
  - `enumitem` - List formatting
  - `multicol` - Multi-column layouts

## Legacy Components

- `resume.yaml` - Original YAML data structure
- `resume_generator.py` - Python-based PDF generator using ReportLab
- Batch files for automated generation

These are maintained for backward compatibility but the LaTeX approach is recommended for new projects.

## Design Features

- **Professional color scheme** using corporate blues and greens
- **Responsive layout** that works well on different page sizes
- **ATS-friendly formatting** with proper heading structure
- **Clickable links** for email, LinkedIn, GitHub, and project URLs
- **Clean typography** with appropriate spacing and hierarchy

## Customization

The LaTeX templates can be easily customized by modifying:
- Color definitions in the preamble
- Section layouts and spacing
- Typography choices
- Page margins and formatting

For consistent branding across documents, maintain the same color scheme and typography choices between resume and cover letter templates.
