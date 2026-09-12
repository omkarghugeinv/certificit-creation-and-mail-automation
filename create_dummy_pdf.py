from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

def create_dummy_template():
    c = canvas.Canvas("dummy_template.pdf", pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Draw border
    c.setStrokeColorRGB(0.2, 0.5, 0.8)
    c.setLineWidth(10)
    c.rect(20, 20, width-40, height-40)
    
    # Draw Title
    c.setFont("Helvetica-Bold", 40)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawCentredString(width/2.0, height - 100, "CERTIFICATE OF PARTICIPATION")
    
    # Draw Subtitle
    c.setFont("Helvetica", 20)
    c.drawCentredString(width/2.0, height - 180, "This is proudly presented to:")
    
    c.save()
    print("Created dummy_template.pdf")

if __name__ == "__main__":
    create_dummy_template()
