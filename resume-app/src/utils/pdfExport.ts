import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export const exportToPDF = async (filename: string = 'resume.pdf') => {
  const element = document.getElementById('resume');
  if (!element) {
    throw new Error('Resume element not found');
  }

  // Add PDF export class for styling
  document.body.classList.add('pdf-export');

  try {
    // Configure html2canvas for high quality output
    const canvas = await html2canvas(element, {
      scale: 2, // Higher resolution
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      width: element.offsetWidth,
      height: element.offsetHeight,
    });

    // Calculate dimensions for US Letter (8.5" x 11")
    const imgWidth = 8.5;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    // Create PDF in portrait mode with US Letter dimensions
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'in',
      format: 'letter'
    });

    // Add the image to PDF
    const imgData = canvas.toDataURL('image/png');
    pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);

    // If content is longer than one page, handle pagination
    if (imgHeight > 11) {
      let position = 11; // Start of second page
      
      while (position < imgHeight) {
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, -position, imgWidth, imgHeight);
        position += 11;
      }
    }

    // Save the PDF
    pdf.save(filename);
  } finally {
    // Remove PDF export class
    document.body.classList.remove('pdf-export');
  }
};

export const printResume = () => {
  window.print();
};
