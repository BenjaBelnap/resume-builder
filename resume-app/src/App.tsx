import React, { useState, useEffect } from 'react';
import yaml from 'js-yaml';
import Resume from './components/Resume';
import { Resume as ResumeType } from './types/Resume';
import { exportToPDF, printResume } from './utils/pdfExport';
import './App.css';

function App() {
  const [resumeData, setResumeData] = useState<ResumeType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadResumeData = async () => {
      try {
        const response = await fetch('../resume.yaml');
        if (!response.ok) {
          throw new Error('Failed to load resume data');
        }
        const yamlText = await response.text();
        const data = yaml.load(yamlText) as ResumeType;
        setResumeData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    loadResumeData();
  }, []);

  const handleExportPDF = async () => {
    try {
      await exportToPDF(`${resumeData?.name.replace(/\s+/g, '_')}_Resume.pdf`);
    } catch (err) {
      console.error('Failed to export PDF:', err);
      alert('Failed to export PDF. Please try again.');
    }
  };

  const handlePrint = () => {
    printResume();
  };

  if (loading) {
    return (
      <div className="app-loading">
        <h2>Loading Resume...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-error">
        <h2>Error Loading Resume</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (!resumeData) {
    return (
      <div className="app-error">
        <h2>No Resume Data Found</h2>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="app-controls">
        <button onClick={handleExportPDF} className="export-btn">
          Export to PDF
        </button>
        <button onClick={handlePrint} className="print-btn">
          Print
        </button>
      </div>
      <Resume data={resumeData} />
    </div>
  );
}

export default App;
