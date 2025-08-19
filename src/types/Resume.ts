export interface Experience {
  company: string;
  role: string;
  location: string;
  dates: string;
  details: string[];
}

export interface Education {
  school: string;
  degree: string;
  location: string;
  dates: string;
}

export interface Contact {
  email: string;
  phone: string;
  linkedin: string;
  location: string;
}

export interface Skills {
  languages: string[];
  concepts: string[];
  certifications: string[];
  tools: string[];
}

export interface Resume {
  name: string;
  title: string;
  statement: string;
  contact: Contact;
  experience: Experience[];
  education: Education[];
  skills: Skills;
  projects: string[];
  portfolio: Array<{
    YouTube?: string;
    GitHub?: string;
  }>;
}
