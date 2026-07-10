import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix multiple table headers
# We want to replace "\n\n| Item | Details | Year First Used | Paper Link |\n|---|---|---|---|\n" with just "\n"
bad_header = "\n| Item | Details | Year First Used | Paper Link |\n|---|---|---|---|\n"
content = content.replace("\n\n" + bad_header.lstrip(), "\n")

# Re-apply badges
badges = """
<div align="center">
<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a><a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>
</div>
"""
if "img.shields.io" not in content:
    content = content.replace('</div>\n## 🌟', '</div>\n' + badges + '\n## 🌟')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)
