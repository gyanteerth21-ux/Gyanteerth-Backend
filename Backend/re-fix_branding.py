import base64
import os

def run_fix():
    # Load Logo Data
    with open('logo.png', 'rb') as f:
        raw_data = f.read()
        b64 = base64.b64encode(raw_data).decode()
    
    # Check if it's WebP or PNG
    if raw_data.startswith(b'RIFF') and b'WEBP' in raw_data[:12]:
        mime_type = "image/webp"
    else:
        mime_type = "image/png"
        
    data_url = f'data:{mime_type};base64,{b64}'
    print(f"Detected MIME type: {mime_type}")
    
    t_dir = os.path.join('utils', 'email_templates')
    files = ['otp_design.py', 'courseactive.py', 'coursecreate.py', 'wecome_trainer_design.py', 'welcome_design.py']
    
    for filename in files:
        path = os.path.join(t_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        updated = False
        for line in lines:
            if '<img' in line and 'src=' in line:
                start_marker = 'src="'
                end_marker = '"'
                start_idx = line.find(start_marker) + len(start_marker)
                end_idx = line.find(end_marker, start_idx)
                
                if start_idx > len(start_marker) and end_idx > -1:
                    new_line = line[:start_idx] + data_url + line[end_idx:]
                    new_lines.append(new_line)
                    updated = True
                    continue
            new_lines.append(line)
            
        if updated:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Updated {filename} with {mime_type} header")

if __name__ == "__main__":
    run_fix()
