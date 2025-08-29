#!/usr/bin/env python3
"""
ATS Compatibility Tester
Analyzes PDF resumes for ATS (Applicant Tracking System) readability
and provides a compatibility score with recommendations.
"""

import os
import re
from typing import Dict, List, Tuple
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class ATSTester:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_content = ""
        self.issues = []
        self.score = 0
        
    def extract_text(self) -> str:
        """Extract text from PDF using available libraries"""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        text = ""
        
        # Try pdfplumber first (more reliable for text extraction)
        if pdfplumber:
            try:
                with pdfplumber.open(self.pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text
            except Exception as e:
                print(f"pdfplumber extraction failed: {e}")
        
        # Fallback to PyPDF2
        if PyPDF2:
            try:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except Exception as e:
                print(f"PyPDF2 extraction failed: {e}")
        
        raise ImportError("No PDF text extraction library available. Install pdfplumber or PyPDF2.")
    
    def check_text_extraction(self) -> bool:
        """Check if text can be extracted from the PDF"""
        try:
            self.text_content = self.extract_text()
            if len(self.text_content.strip()) < 50:
                self.issues.append("❌ Very little text extracted - PDF might be image-based or have extraction issues")
                return False
            return True
        except Exception as e:
            self.issues.append(f"❌ Failed to extract text: {str(e)}")
            return False
    
    def check_contact_info(self) -> Dict[str, bool]:
        """Check for presence of essential contact information"""
        results = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        results['email'] = bool(re.search(email_pattern, self.text_content))
        
        # Phone pattern (various formats)
        phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4})'
        results['phone'] = bool(re.search(phone_pattern, self.text_content))
        
        # LinkedIn pattern
        linkedin_pattern = r'(linkedin\.com/in/|linkedin\.com)'
        results['linkedin'] = bool(re.search(linkedin_pattern, self.text_content, re.IGNORECASE))
        
        # Address/Location (basic check for city, state patterns)
        location_pattern = r'\b[A-Z][a-z]+,\s*[A-Z]{2}\b'
        results['location'] = bool(re.search(location_pattern, self.text_content))
        
        return results
    
    def check_section_headers(self) -> Dict[str, bool]:
        """Check for standard resume section headers"""
        sections = {
            'experience': r'\b(EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE)\b',
            'education': r'\b(EDUCATION|ACADEMIC BACKGROUND)\b',
            'skills': r'\b(SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)\b',
            'projects': r'\b(PROJECTS|PERSONAL PROJECTS)\b'
        }
        
        results = {}
        for section, pattern in sections.items():
            results[section] = bool(re.search(pattern, self.text_content, re.IGNORECASE))
        
        return results
    
    def check_formatting_issues(self) -> List[str]:
        """Check for common ATS formatting issues"""
        issues = []
        
        # Check for excessive special characters
        special_chars = re.findall(r'[^\w\s@.,()-]', self.text_content)
        if len(special_chars) > 20:
            issues.append("⚠️ High number of special characters detected - may cause parsing issues")
        
        # Check for proper spacing
        if re.search(r'\w{2,}\w{2,}', self.text_content):  # Words mashed together
            issues.append("⚠️ Potential text spacing issues detected")
        
        # Check for bullet points (should be simple)
        bullet_patterns = ['•', '▪', '▫', '◦', '‣']
        complex_bullets = [char for char in bullet_patterns if char in self.text_content]
        if len(complex_bullets) > 1:
            issues.append("⚠️ Multiple bullet point styles detected - use consistent simple bullets")
        
        # Check line length (very long lines might indicate formatting issues)
        lines = self.text_content.split('\n')
        long_lines = [line for line in lines if len(line) > 200]
        if long_lines:
            issues.append("⚠️ Very long text lines detected - may indicate formatting issues")
        
        return issues
    
    def check_keywords_and_content(self) -> Dict[str, any]:
        """Analyze content quality and keyword usage"""
        results = {}
        
        # Word count
        words = len(self.text_content.split())
        results['word_count'] = words
        
        if words < 100:
            results['word_count_issue'] = "❌ Very low word count - resume may be too brief"
        elif words > 1000:
            results['word_count_issue'] = "⚠️ High word count - consider condensing"
        else:
            results['word_count_issue'] = "✅ Good word count"
        
        # Check for action verbs (common in good resumes)
        action_verbs = [
            'achieved', 'developed', 'managed', 'created', 'implemented', 'designed',
            'led', 'improved', 'increased', 'reduced', 'optimized', 'built',
            'collaborated', 'coordinated', 'analyzed', 'streamlined'
        ]
        
        found_verbs = [verb for verb in action_verbs if verb.lower() in self.text_content.lower()]
        results['action_verbs'] = len(found_verbs)
        results['action_verbs_found'] = found_verbs[:5]  # Show first 5
        
        return results
    
    def calculate_score(self, contact_results: Dict, section_results: Dict, 
                       formatting_issues: List, content_results: Dict) -> int:
        """Calculate overall ATS compatibility score (0-100)"""
        score = 0
        
        # Text extraction (30 points)
        if len(self.text_content.strip()) > 50:
            score += 30
        
        # Contact information (20 points)
        contact_score = sum(contact_results.values()) * 5
        score += min(contact_score, 20)
        
        # Section headers (20 points)
        section_score = sum(section_results.values()) * 5
        score += min(section_score, 20)
        
        # Formatting (15 points)
        formatting_score = max(0, 15 - len(formatting_issues) * 3)
        score += formatting_score
        
        # Content quality (15 points)
        if content_results['word_count'] >= 100:
            score += 5
        if content_results['action_verbs'] >= 3:
            score += 5
        if 'Good word count' in content_results.get('word_count_issue', ''):
            score += 5
        
        return min(score, 100)
    
    def run_analysis(self) -> Dict:
        """Run complete ATS analysis"""
        print(f"🔍 Analyzing PDF: {self.pdf_path}")
        print("=" * 50)
        
        # Test text extraction
        text_extracted = self.check_text_extraction()
        
        if not text_extracted:
            return {
                'score': 0,
                'issues': self.issues,
                'recommendations': ["Fix text extraction issues before proceeding"]
            }
        
        # Run all checks
        contact_results = self.check_contact_info()
        section_results = self.check_section_headers()
        formatting_issues = self.check_formatting_issues()
        content_results = self.check_keywords_and_content()
        
        # Calculate score
        score = self.calculate_score(contact_results, section_results, formatting_issues, content_results)
        
        # Generate report
        return self.generate_report(score, contact_results, section_results, 
                                  formatting_issues, content_results)
    
    def generate_report(self, score: int, contact_results: Dict, section_results: Dict,
                       formatting_issues: List, content_results: Dict) -> Dict:
        """Generate comprehensive analysis report"""
        
        print(f"📊 ATS COMPATIBILITY SCORE: {score}/100")
        
        if score >= 85:
            print("🟢 EXCELLENT - Highly ATS compatible")
        elif score >= 70:
            print("🟡 GOOD - Minor improvements recommended")
        elif score >= 50:
            print("🟠 FAIR - Several issues need attention")
        else:
            print("🔴 POOR - Major improvements required")
        
        print("\n📋 DETAILED ANALYSIS:")
        print("-" * 30)
        
        # Contact Information
        print("📞 Contact Information:")
        for contact_type, found in contact_results.items():
            status = "✅" if found else "❌"
            print(f"  {status} {contact_type.title()}")
        
        # Section Headers
        print("\n📑 Section Headers:")
        for section, found in section_results.items():
            status = "✅" if found else "❌"
            print(f"  {status} {section.title()}")
        
        # Content Analysis
        print(f"\n📝 Content Analysis:")
        print(f"  📊 Word count: {content_results['word_count']}")
        print(f"  🎯 Action verbs found: {content_results['action_verbs']}")
        print(f"  ✍️ {content_results['word_count_issue']}")
        
        if content_results['action_verbs_found']:
            print(f"  💪 Action verbs: {', '.join(content_results['action_verbs_found'])}")
        
        # Formatting Issues
        if formatting_issues:
            print(f"\n⚠️ Formatting Issues:")
            for issue in formatting_issues:
                print(f"  {issue}")
        
        # General Issues
        if self.issues:
            print(f"\n❌ General Issues:")
            for issue in self.issues:
                print(f"  {issue}")
        
        # Recommendations
        recommendations = self.generate_recommendations(score, contact_results, 
                                                      section_results, formatting_issues)
        
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        
        return {
            'score': score,
            'contact_info': contact_results,
            'sections': section_results,
            'formatting_issues': formatting_issues,
            'content': content_results,
            'recommendations': recommendations,
            'text_length': len(self.text_content)
        }
    
    def generate_recommendations(self, score: int, contact_results: Dict,
                               section_results: Dict, formatting_issues: List) -> List[str]:
        """Generate specific recommendations based on analysis"""
        recommendations = []
        
        # Contact info recommendations
        missing_contact = [k for k, v in contact_results.items() if not v]
        if missing_contact:
            recommendations.append(f"Add missing contact information: {', '.join(missing_contact)}")
        
        # Section recommendations
        missing_sections = [k for k, v in section_results.items() if not v]
        if missing_sections:
            recommendations.append(f"Add standard section headers: {', '.join(missing_sections).upper()}")
        
        # Formatting recommendations
        if formatting_issues:
            recommendations.append("Address formatting issues to improve text parsing")
        
        # Score-based recommendations
        if score < 70:
            recommendations.append("Consider using simpler formatting with standard fonts")
            recommendations.append("Ensure consistent spacing and alignment")
            recommendations.append("Use standard bullet points (• or -)")
        
        if score < 50:
            recommendations.append("Review PDF generation settings for better text extraction")
            recommendations.append("Test with multiple ATS systems if possible")
        
        return recommendations


def main():
    """Main function to run ATS testing"""
    import sys
    from pathlib import Path
    
    # Default to looking in output directory
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "output"
    pdf_file = output_dir / "resume.pdf"
    
    # Allow command line argument for different PDF file
    if len(sys.argv) > 1:
        pdf_file = Path(sys.argv[1])
        if not pdf_file.is_absolute():
            pdf_file = output_dir / pdf_file
    
    if not pdf_file.exists():
        print(f"❌ PDF file not found: {pdf_file}")
        print("Please generate your resume first by running: python src/build.py")
        print(f"Expected location: {pdf_file}")
        return
    
    # Check for required libraries
    global pdfplumber, PyPDF2
    if pdfplumber is None and PyPDF2 is None:
        print("📦 Installing required libraries...")
        import subprocess
        import sys
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
            import pdfplumber
        except:
            print("❌ Failed to install pdfplumber. Please install manually:")
            print("pip install pdfplumber")
            return
    
    # Run ATS analysis
    tester = ATSTester(str(pdf_file))
    results = tester.run_analysis()
    
    print(f"\n🎯 SUMMARY:")
    print(f"Your resume scored {results['score']}/100 for ATS compatibility.")
    
    if results['score'] >= 85:
        print("🎉 Great job! Your resume should work well with most ATS systems.")
    elif results['score'] >= 70:
        print("👍 Good work! A few tweaks will make it even better.")
    else:
        print("🔧 Consider the recommendations above to improve ATS compatibility.")


if __name__ == "__main__":
    main()
