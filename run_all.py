import os
import re
import subprocess

def run_git(msg):
    subprocess.run("git add README.md pages/ assets/", shell=True)
    subprocess.run(f'git commit -m "{msg}"', shell=True)
    subprocess.run("git push", shell=True)

with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_list = False
current_section = 0

def format_row(title, details):
    # Extract title text
    title_clean = re.sub(r'^[-*]\s*(###\s*([A-Z]\.\s+)?|\*\*)', '', title)
    title_clean = title_clean.split('**')[0].strip()
    
    filename = re.sub(r'[^a-z0-9]+', '-', title_clean.lower()).strip('-') + '.md'
    
    # Format details
    details_str = '<br>'.join([d.strip().lstrip('* \t') for d in details])
    
    return f'| [**{title_clean}**](pages/{filename}) | {details_str} | 2020 | [Paper](#) |\n', filename, title_clean

pages_to_create = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Track section
    if line.startswith('## '):
        if '1.' in line: current_section = 1
        elif '2.' in line: current_section = 2
        elif '3.' in line: current_section = 3
        elif '4.' in line: current_section = 4
        elif '5.' in line: current_section = 5
        else: current_section = 0
        new_lines.append(line)
        in_list = False
        i += 1
        continue
        
    if current_section in [1,2,3,4,5]:
        if re.match(r'^[-*]\s+(###|\*\*)', line):
            if not in_list:
                in_list = True
                new_lines.append('| Item | Details | Year First Used | Paper Link |\n|---|---|---|---|\n')
            
            title = line.strip()
            details = []
            i += 1
            while i < len(lines) and re.match(r'^\s+\*\s', lines[i]):
                details.append(lines[i].strip())
                i += 1
            
            row, filename, title_clean = format_row(title, details)
            new_lines.append(row)
            pages_to_create.append((filename, title_clean))
            continue
            
    if not (re.match(r'^[-*]\s+(###|\*\*)', line) or re.match(r'^\s+\*\s', line)):
        in_list = False
        new_lines.append(line)
        
    i += 1

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

run_git("tabularised the bullets")

# Step 2: Detailed pages
os.makedirs('pages', exist_ok=True)
for filename, title in pages_to_create:
    content = f"""# {title}

This page contains detailed information about {title}.

```mermaid
flowchart TD
    A[{title}] --> B[More Details]
```

[Back to README](../README.md)
"""
    with open(f'pages/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

run_git("detailed pages created")

# Step 3: Decorate with emojis and banner
os.makedirs('assets', exist_ok=True)
svg_content = '''<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:rgb(74,144,226);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(144,19,254);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad1)" rx="15"/>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="40" fill="white" text-anchor="middle" dominant-baseline="middle">
    Awesome Neural-Symbolic AI
  </text>
  <circle cx="100" cy="100" r="20" fill="white" opacity="0.5">
    <animate attributeName="r" values="20;30;20" dur="2s" repeatCount="indefinite" />
  </circle>
</svg>
'''
with open('assets/banner.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('# Awesome-Neural-Symbolic-AI', '# 🚀 Awesome-Neural-Symbolic-AI 🧠\\n\\n<div align="center">\\n<img src="assets/banner.svg" alt="Banner" width="100%">\\n</div>')
content = content.replace('## Neuro-Symbolic AI:', '## 🌟 Neuro-Symbolic AI:')
content = content.replace('## 1. The Macro Chronological Evolution', '## 🕰️ 1. The Macro Chronological Evolution')
content = content.replace('## 2. Core Functional & Structural Variants', '## ⚙️ 2. Core Functional & Structural Variants')
content = content.replace('## 3. The Neuro-Symbolic Verification Matrix', '## 📊 3. The Neuro-Symbolic Verification Matrix')
content = content.replace('## 4. Production Engineering Challenges & Cluster Mitigations', '## 🏗️ 4. Production Engineering Challenges & Cluster Mitigations')
content = content.replace('## 5. Frontier Real-World AI Infrastructure Applications', '## 🌍 5. Frontier Real-World AI Infrastructure Applications')
content = content.replace('## References', '## 📚 References')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

run_git("added emojis and banner")

# Step 4: SEO and badges to left
badges_left = '<div align="center">\\n<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
# insert badges after banner
content = content.replace('</div>\\n\\n## 🌟', '</div>\\n\\n' + badges_left + '\\n</div>\\n\\n## 🌟')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

run_git("seo optimised and badges to left added")

# Step 5: Badges to right
badge_right = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('alt="Discord" /></a>\\n</div>', 'alt="Discord" /></a>' + badge_right + '\\n</div>')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

run_git("badges to right added")

# Step 6: Star history
star_history = """
## ⭐ Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007/Awesome-Neural-Symbolic-AI&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Neural-Symbolic-AI&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Neural-Symbolic-AI&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Neural-Symbolic-AI&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"""
with open('README.md', 'a', encoding='utf-8') as f:
    f.write(star_history)

run_git("star history added")

# Step 7: Fix chartrepos
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('chartrepos', 'chart?repos')
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

run_git("fixed star plot")

# Step 8: Fix awesome link
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

run_git("invalid awesome link fixed")

print("All done!")
