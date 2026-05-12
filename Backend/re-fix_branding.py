import base64
import os

def run_fix():
    # Load FULL Logo Data
    with open('logo.png', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    data_url = f'data:image/png;base64,{b64}'
    
    t_dir = os.path.join('utils', 'email_templates')
    files = ['otp_design.py', 'courseactive.py', 'coursecreate.py', 'wecome_trainer_design.py', 'welcome_design.py']
    
    for filename in files:
        path = os.path.join(t_dir, filename)
        if not os.path.exists(path):
            print(f"Skipping {filename} - not found")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        updated = False
        for line in lines:
            # Look for ANY img tag with src starting with data: or cloudinary
            if '<img' in line and 'src=' in line:
                # Precision replace for the src attribute
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
            print(f"SUCCESS: Fully updated logo in {filename}")
        else:
            print(f"WARNING: No logo tag found in {filename}")

if __name__ == "__main__":
    run_fix()
