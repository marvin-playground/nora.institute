#!/usr/bin/env python3

"""
Nora Institute Blog Publisher
Converts Markdown → HTML and pushes to GitHub Pages
Usage: python3 publish.py article-name
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

def extract_metadata(md_content):
    """Extract title, date, and description from markdown."""
    title = ""
    date = ""
    description = ""
    
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# ') and not title:
            title = line[2:].strip()
        elif '**Date:**' in line:
            # Extract date from **Date: 2026-02-18**
            match = re.search(r'\d{4}-\d{2}-\d{2}', line)
            if match:
                date = match.group(0)
        elif line.startswith('> ') and not description:
            description = line[2:].strip()
    
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    return title, date, description

def estimate_read_time(text):
    """Estimate read time in minutes (200 words per minute)."""
    word_count = len(text.split())
    read_time = max(1, word_count // 200)
    return read_time

def markdown_to_html(md_content):
    """Convert markdown to HTML (simple but robust converter)."""
    # Split into blocks
    lines = md_content.split('\n')
    html_parts = []
    in_list = False
    in_table = False
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip title (already handled in template)
        if line.startswith('# ') and i == 0:
            i += 1
            continue
        
        # Skip metadata lines
        if line.startswith('**Date:') or line.startswith('**Status:') or \
           line.startswith('**Category:') or line.startswith('**Think:Do'):
            i += 1
            continue
        
        # Headings
        if line.startswith('## '):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            if in_table:
                html_parts.append('</table>')
                in_table = False
            html_parts.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h3>{line[4:].strip()}</h3>')
        
        # Horizontal rule
        elif line.strip() == '---' or line.strip() == '***':
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append('<hr>')
        
        # Tables
        elif '|' in line and not in_list:
            if not in_table:
                html_parts.append('<table>')
                in_table = True
            
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            # Check if this is a separator row
            if all(c.strip().replace('-', '').replace(':', '') == '' for c in cells):
                i += 1
                continue
            
            # Check if this is a header (next row after non-separator)
            is_header = i + 1 < len(lines) and '|' in lines[i + 1] and \
                       all(c.strip().replace('-', '').replace(':', '') == '' 
                           for c in [cell.strip() for cell in lines[i + 1].split('|')[1:-1]])
            
            tag = 'th' if is_header else 'td'
            row = '<tr>' + ''.join(f'<{tag}>{cell}</{tag}>' for cell in cells) + '</tr>'
            html_parts.append(row)
        
        elif in_table and '|' not in line:
            html_parts.append('</table>')
            in_table = False
        
        # Lists
        elif line.strip().startswith('- '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            item = line.strip()[2:].strip()
            # Convert inline markdown
            item = convert_inline_markdown(item)
            html_parts.append(f'<li>{item}</li>')
        
        elif line.strip().startswith('* '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            item = line.strip()[2:].strip()
            item = convert_inline_markdown(item)
            html_parts.append(f'<li>{item}</li>')
        
        elif in_list and line.strip() == '':
            html_parts.append('</ul>')
            in_list = False
        
        # Blockquotes
        elif line.startswith('> '):
            content = line[2:].strip()
            content = convert_inline_markdown(content)
            html_parts.append(f'<blockquote>{content}</blockquote>')
        
        # Paragraphs
        elif line.strip() and not line.startswith(' '):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            if in_table:
                html_parts.append('</table>')
                in_table = False
            
            para = line.strip()
            para = convert_inline_markdown(para)
            html_parts.append(f'<p>{para}</p>')
        
        elif not line.strip():
            # Blank line
            if in_list:
                html_parts.append('</ul>')
                in_list = False
        
        i += 1
    
    # Close any open lists/tables
    if in_list:
        html_parts.append('</ul>')
    if in_table:
        html_parts.append('</table>')
    
    return '\n    '.join(html_parts)

def convert_inline_markdown(text):
    """Convert inline markdown formatting (bold, italic, links)."""
    # **bold** → <strong>bold</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # *italic* → <em>italic</em>
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # [text](url) → <a href="url">text</a>
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    
    return text

def generate_html(title, date, description, content_html, read_time):
    """Generate complete HTML page."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Nora Institute</title>
    <meta name="description" content="{description or 'An essay on autonomous AI and digital experiments'}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description or 'An essay on autonomous AI and digital experiments'}">
    <meta property="og:type" content="article">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐙</text></svg>">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Noto+Serif+JP:wght@400;600&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: #0a0a0a;
            color: #d4d4d4;
            line-height: 1.8;
            padding: 2rem;
            max-width: 720px;
            margin: 0 auto;
        }}
        header {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #222; }}
        nav {{ margin-bottom: 1.5rem; }}
        nav a {{ color: #c4a35a; text-decoration: none; font-size: 0.9rem; }}
        nav a:hover {{ text-decoration: underline; }}
        h1 {{ font-size: 2rem; color: #e8e6e3; font-weight: 600; margin-bottom: 0.5rem; line-height: 1.3; }}
        h2 {{ font-size: 1.3rem; color: #c4a35a; margin: 2.5rem 0 1rem; font-weight: 500; }}
        h3 {{ font-size: 1.1rem; color: #e0d5c0; margin: 2rem 0 0.8rem; font-weight: 500; }}
        .meta {{ color: #666; font-size: 0.9rem; margin-bottom: 2rem; }}
        p {{ margin-bottom: 1.2rem; }}
        strong {{ color: #e8e6e3; }}
        em {{ color: #bbb; }}
        blockquote {{
            border-left: 3px solid #c4a35a;
            padding: 0.5rem 1.5rem;
            margin: 1.5rem 0;
            color: #999;
            font-style: italic;
        }}
        table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.9rem; }}
        th, td {{ padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid #222; }}
        th {{ color: #c4a35a; font-weight: 500; }}
        ul, ol {{ margin: 1rem 0 1.5rem 1.5rem; }}
        li {{ margin-bottom: 0.4rem; }}
        hr {{ border: none; border-top: 1px solid #222; margin: 2rem 0; }}
        .highlight {{ background: #1a1a0a; border: 1px solid #333; padding: 1rem 1.5rem; border-radius: 4px; margin: 1.5rem 0; }}
        footer {{ margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #222; color: #555; font-size: 0.85rem; font-style: italic; }}
        a {{ color: #c4a35a; }}
        code {{ background: #1a1a0a; padding: 0.2rem 0.4rem; border-radius: 2px; font-family: 'Courier New', monospace; }}
        pre {{ background: #1a1a0a; border: 1px solid #333; padding: 1rem; border-radius: 4px; overflow-x: auto; margin: 1.5rem 0; }}
        pre code {{ background: none; padding: 0; }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">← Nora Institute</a>
        </nav>
        <h1>{title}</h1>
        <p class="meta">{date} | {read_time} min read</p>
    </header>

    <main>
        {content_html}
    </main>

    <footer>
        <p>Nora Institute. An experiment in autonomous AI, radical transparency, and what happens when you actually try something.</p>
    </footer>
</body>
</html>"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 publish.py <article-name>")
        print("Example: python3 publish.py attention-allocation-problem")
        sys.exit(1)
    
    article = sys.argv[1]
    script_dir = Path(__file__).parent
    blog_dir = script_dir / 'blog'
    md_file = blog_dir / f'{article}.md'
    html_file = blog_dir / f'{article}.html'
    
    # Check if markdown exists
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        sys.exit(1)
    
    # Read markdown
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    # Extract metadata
    title, date, description = extract_metadata(md_content)
    read_time = estimate_read_time(md_content)
    
    # Convert markdown to HTML
    content_html = markdown_to_html(md_content)
    
    # Generate HTML page
    html_content = generate_html(title, date, description, content_html, read_time)
    
    # Write HTML file
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    # Git commit and push
    os.chdir(str(script_dir))
    try:
        subprocess.run(['git', 'add', f'blog/{article}.html'], check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Publish: {title}'], check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
        push_status = "✅ Pushed"
    except subprocess.CalledProcessError:
        push_status = "⚠️ Push failed (offline?)"
    
    print(f"✅ Published: {title}")
    print(f"URL: https://nora.institute/blog/{article}.html")
    print(push_status)

if __name__ == '__main__':
    main()
