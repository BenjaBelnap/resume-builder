import React from 'react';
import { Resume as ResumeType } from '../types/Resume';
import './Resume.css';

interface ResumeProps {
  data: ResumeType;
}

const Resume: React.FC<ResumeProps> = ({ data }) => {
  return (
    <div className="resume-container" id="resume">
      <div className="resume-paper">
        {/* Header */}
        <header className="resume-header">
          <h1 className="name">{data.name}</h1>
          <h2 className="title">{data.title}</h2>
          <div className="contact-info">
            <span>{data.contact.email}</span>
            <span>{data.contact.phone}</span>
            <span>{data.contact.location}</span>
          </div>
          <div className="portfolio-links">
            {data.portfolio.map((item, index) => (
              <React.Fragment key={index}>
                {item.GitHub && (
                  <a href={item.GitHub} target="_blank" rel="noopener noreferrer">
                    GitHub
                  </a>
                )}
                {item.YouTube && (
                  <a href={item.YouTube} target="_blank" rel="noopener noreferrer">
                    YouTube
                  </a>
                )}
              </React.Fragment>
            ))}
            <a href={data.contact.linkedin} target="_blank" rel="noopener noreferrer">
              LinkedIn
            </a>
          </div>
        </header>

        {/* Statement */}
        <section className="section">
          <h3>Professional Statement</h3>
          <p className="statement">{data.statement}</p>
        </section>

        {/* Experience */}
        <section className="section">
          <h3>Experience</h3>
          {data.experience.map((exp, index) => (
            <div key={index} className="experience-item">
              <div className="experience-header">
                <div>
                  <h4>{exp.role}</h4>
                  <p className="company">{exp.company} - {exp.location}</p>
                </div>
                <span className="dates">{exp.dates}</span>
              </div>
              <ul className="details">
                {exp.details.map((detail, detailIndex) => (
                  <li key={detailIndex}>{detail}</li>
                ))}
              </ul>
            </div>
          ))}
        </section>

        {/* Education */}
        <section className="section">
          <h3>Education</h3>
          {data.education.map((edu, index) => (
            <div key={index} className="education-item">
              <div className="education-header">
                <div>
                  <h4>{edu.degree}</h4>
                  <p className="school">{edu.school} - {edu.location}</p>
                </div>
                <span className="dates">{edu.dates}</span>
              </div>
            </div>
          ))}
        </section>

        {/* Skills */}
        <section className="section">
          <h3>Skills</h3>
          <div className="skills-grid">
            <div className="skill-category">
              <h4>Programming Languages</h4>
              <ul>
                {data.skills.languages.map((lang, index) => (
                  <li key={index}>{lang}</li>
                ))}
              </ul>
            </div>
            <div className="skill-category">
              <h4>Concepts</h4>
              <ul>
                {data.skills.concepts.map((concept, index) => (
                  <li key={index}>{concept}</li>
                ))}
              </ul>
            </div>
            <div className="skill-category">
              <h4>Certifications</h4>
              <ul>
                {data.skills.certifications.map((cert, index) => (
                  <li key={index}>{cert}</li>
                ))}
              </ul>
            </div>
            <div className="skill-category">
              <h4>Tools & Technologies</h4>
              <ul>
                {data.skills.tools.map((tool, index) => (
                  <li key={index}>{tool}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* Projects */}
        <section className="section">
          <h3>Projects</h3>
          <div className="projects-list">
            {data.projects.map((project, index) => (
              <span key={index} className="project-item">{project}</span>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Resume;
