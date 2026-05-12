import base64
import os

def inject():
    logo_path = 'logo.png'
    if not os.path.exists(logo_path):
        print("Logo not found")
        return

    b64 = base64.b64encode(open(logo_path, 'rb').read()).decode()
    data_url = f'data:image/png;base64,{b64}'
    
    t_dir = os.path.join('utils', 'email_templates')
    
    # 1. Welcome Design
    welcome_path = os.path.join(t_dir, 'welcome_design.py')
    if os.path.exists(welcome_path):
        with open(welcome_path, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('<h1>Welcome to Gyanteerth</h1>', f'<img src="{data_url}" style="width:180px;" alt="Gyanteerth"/>')
        c = c.replace('.header {', f'.header {{ background: linear-gradient(90deg,#1db954,#00a86b) !important; ')
        with open(welcome_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated welcome_design.py")

    # 2. Course Active
    active_path = os.path.join(t_dir, 'courseactive.py')
    if os.path.exists(active_path):
        with open(active_path, 'r', encoding='utf-8') as f:
            c = f.read()
        header_row = f'''
          <!-- Branded Header -->
          <tr>
            <td style="background:linear-gradient(90deg,#1db954,#00a86b);padding:30px;text-align:center;">
              <img src="{data_url}" style="width:180px;" alt="Gyanteerth"/>
            </td>
          </tr>
        '''
        c = c.replace('<!-- Header -->', header_row)
        with open(active_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated courseactive.py")

if __name__ == "__main__":
    inject()
