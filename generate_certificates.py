import os
import csv
from PIL import Image, ImageDraw, ImageFont

def create_default_template(template_path):
    """Creates a basic certificate template if one doesn't exist."""
    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_color = (0, 102, 204)
    draw.rectangle([20, 20, 1180, 780], outline=border_color, width=10)
    
    # Load fonts
    try:
        # Windows typically has arial, adjust for other OS if needed
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_subtitle = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        
    title = "CERTIFICATE OF PARTICIPATION"
    subtitle = "This is proudly presented to:"
    
    # Draw text with anchor='mm' (middle-middle) for centering
    draw.text((600, 150), title, fill=border_color, font=font_title, anchor="mm")
    draw.text((600, 300), subtitle, fill='black', font=font_subtitle, anchor="mm")
    
    img.save(template_path)
    print(f"Created default template at {template_path}")

def generate_certificates(csv_file='students.csv', template_path='template.png', output_dir='certificates'):
    """Reads student data and generates a certificate for each."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(template_path):
        create_default_template(template_path)
        
    generated_data = []
    
    try:
        font_name = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        font_name = ImageFont.load_default()

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return []

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Check if Name column exists
        if 'Name' not in reader.fieldnames:
            print("Error: CSV must contain a 'Name' column.")
            return []
            
        for row in reader:
            name = row.get('Name')
            email = row.get('Email', '').strip()
            
            if not name:
                continue
                
            # Load template
            img = Image.open(template_path)
            draw = ImageDraw.Draw(img)
            
            # Draw student name (Centered)
            draw.text((600, 450), name, fill='black', font=font_name, anchor="mm")
            
            # Save the personalized certificate
            safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            cert_filename = f"{safe_name.replace(' ', '_')}_certificate.png"
            cert_path = os.path.join(output_dir, cert_filename)
            img.save(cert_path)
            
            print(f"Generated certificate for {name} -> {cert_path}")
            generated_data.append({
                'name': name,
                'email': email,
                'cert_path': cert_path
            })
            
    return generated_data

if __name__ == "__main__":
    generate_certificates()
