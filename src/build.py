#!/usr/bin/env python3
"""
LaTeX Resume and Cover Letter Builder
Compiles LaTeX templates to PDF and organizes output files.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class DocumentBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.resources_dir = self.project_root / "resources"
        self.templates_dir = self.resources_dir / "templates"
        self.output_dir = self.project_root / "output"
        self.temp_dir = self.project_root / "temp"
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def check_latex_installation(self):
        """Check if LaTeX is installed and available"""
        try:
            result = subprocess.run(['pdflatex', '--version'], 
                                  capture_output=True, text=True, check=True)
            print("✓ LaTeX installation found")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ LaTeX installation not found")
            print("Please install a LaTeX distribution (TeX Live, MiKTeX, etc.)")
            return False
    
    def compile_latex(self, tex_file: Path, output_name: str = None):
        """Compile a LaTeX file to PDF"""
        if not tex_file.exists():
            print(f"✗ Template file not found: {tex_file}")
            return False
        
        if output_name is None:
            output_name = tex_file.stem
        
        print(f"📄 Compiling {tex_file.name}...")
        
        # Copy template to temp directory for compilation
        temp_tex = self.temp_dir / tex_file.name
        shutil.copy2(tex_file, temp_tex)
        
        # Copy profile image if it exists (needed for resume)
        profile_image = self.project_root / "resources" / "images" / "profile.png"
        if profile_image.exists():
            temp_image = self.temp_dir / "profile.png"
            shutil.copy2(profile_image, temp_image)
        
        try:
            # First pass
            result = subprocess.run([
                'pdflatex', 
                '-interaction=nonstopmode',
                '-output-directory', str(self.temp_dir),
                str(temp_tex)
            ], capture_output=True, text=True, cwd=self.temp_dir)
            
            if result.returncode != 0:
                print(f"✗ LaTeX compilation failed for {tex_file.name}")
                print("Error output:")
                print(result.stdout)
                print(result.stderr)
                return False
            
            # Move PDF to output directory
            pdf_file = self.temp_dir / f"{tex_file.stem}.pdf"
            output_pdf = self.output_dir / f"{output_name}.pdf"
            
            if pdf_file.exists():
                shutil.move(str(pdf_file), str(output_pdf))
                print(f"✓ Created {output_pdf}")
                return True
            else:
                print(f"✗ PDF not generated for {tex_file.name}")
                return False
                
        except Exception as e:
            print(f"✗ Error compiling {tex_file.name}: {e}")
            return False
    
    def build_resume(self):
        """Build the resume PDF"""
        resume_tex = self.templates_dir / "resume.tex"
        return self.compile_latex(resume_tex, "resume")
    
    def build_cover_letter(self):
        """Build the cover letter PDF"""
        # Check for both template and filled version
        cover_letter_tex = self.templates_dir / "coverletter.tex"
        template_tex = self.templates_dir / "coverletter_template.tex"
        
        if cover_letter_tex.exists():
            return self.compile_latex(cover_letter_tex, "coverletter")
        elif template_tex.exists():
            print("ℹ️  Cover letter template found but no filled version")
            print(f"   Use the template at: {template_tex}")
            print(f"   Save filled version as: {cover_letter_tex}")
            return False
        else:
            print("✗ No cover letter template found")
            return False
    
    def clean_temp_files(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            print("✓ Cleaned temporary files")
    
    def build_all(self):
        """Build all documents"""
        if not self.check_latex_installation():
            return False
        
        print("🔨 Building resume and cover letter...")
        print("=" * 50)
        
        success_count = 0
        
        # Build resume
        if self.build_resume():
            success_count += 1
        
        # Build cover letter
        if self.build_cover_letter():
            success_count += 1
        
        # Clean up
        self.clean_temp_files()
        
        print("=" * 50)
        if success_count > 0:
            print(f"✓ Built {success_count} document(s)")
            print(f"📁 Output directory: {self.output_dir}")
        else:
            print("✗ No documents were built successfully")
        
        return success_count > 0


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        builder = DocumentBuilder()
        
        if command == "resume":
            builder.check_latex_installation() and builder.build_resume()
        elif command == "coverletter" or command == "cover":
            builder.check_latex_installation() and builder.build_cover_letter()
        elif command == "clean":
            builder.clean_temp_files()
        elif command == "all":
            builder.build_all()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python build.py [resume|coverletter|clean|all]")
    else:
        # Default: build all
        builder = DocumentBuilder()
        builder.build_all()


if __name__ == "__main__":
    main()
