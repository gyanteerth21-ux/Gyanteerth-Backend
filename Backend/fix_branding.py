import base64
import os

def run_fix():
    # Load Logo
    with open('logo.png', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    data_url = f'data:image/png;base64,{b64}'
    
    # Old Cloudinary URL to replace
    old_url = 'https://res.cloudinary.com/dosahgtni/image/upload/v1773465717/Gyanteerth-removebg-preview_t5ap3i.png'
    
    t_dir = os.path.join('utils', 'email_templates')
    files = ['otp_design.py', 'courseactive.py', 'coursecreate.py', 'wecome_trainer_design.py', 'welcome_design.py']
    
    for filename in files:
        path = os.path.join(t_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Replace existing link if found
        if old_url in content:
            content = content.replace(old_url, data_url)
            print(f"Updated link in {filename}")
        
        # 2. Special case for welcome_design.py (inject header)
        if filename == 'welcome_design.py' and '<h1>Welcome to Gyanteerth</h1>' in content:
            new_header = f'<img src="{data_url}" style="width:180px;" alt="Gyanteerth"/>'
            content = content.replace('<h1>Welcome to Gyanteerth</h1>', new_header)
            content = content.replace('.header {', '.header { background: linear-gradient(90deg,#1db954,#00a86b) !important; ')
            print(f"Injected header into {filename}")

        # 3. Special case for courseactive.py (inject header)
        if filename == 'courseactive.py' and '<!-- Header -->' in content:
            branded_header = f'''
          <!-- Branded Header -->
          <tr>
            <td style="background:linear-gradient(90deg,#1db954,#00a86b);padding:30px;text-align:center;">
              <img src="{data_url}" style="width:180px;" alt="Gyanteerth"/>
            </td>
          </tr>
        '''
            content = content.replace('<!-- Header -->', branded_header)
            print(f"Injected header into {filename}")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    run_fix()
