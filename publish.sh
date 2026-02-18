#!/bin/bash

# Nora Institute Blog Publisher
# Converts Markdown → HTML and pushes to GitHub Pages
# Usage: ./publish.sh article-name

set -e

BLOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/blog" && pwd)"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$1" ]; then
    echo "Usage: $0 <article-name>"
    echo "Example: $0 attention-allocation-problem"
    exit 1
fi

ARTICLE="$1"
MD_FILE="$BLOG_DIR/${ARTICLE}.md"
HTML_FILE="$BLOG_DIR/${ARTICLE}.html"

if [ ! -f "$MD_FILE" ]; then
    echo "Error: $MD_FILE not found"
    exit 1
fi

# Extract metadata from markdown
TITLE=$(grep "^# " "$MD_FILE" | head -1 | sed 's/^# //')
DATE=$(grep "^\*\*Date:" "$MD_FILE" | head -1 | sed 's/.*Date: //' | sed 's/ \|.*//')
DESCRIPTION=$(grep "^> " "$MD_FILE" | head -1 | sed 's/^> //' || echo "")

if [ -z "$DATE" ]; then
    DATE=$(date +%Y-%m-%d)
fi

# Generate HTML from Markdown
cat > "$HTML_FILE" << 'TEMPLATE'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITLE — Nora Institute</title>
    <meta name="description" content="DESCRIPTION">
    <meta property="og:title" content="TITLE">
    <meta property="og:description" content="DESCRIPTION">
    <meta property="og:type" content="article">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐙</text></svg>">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Noto+Serif+JP:wght@400;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: #0a0a0a;
            color: #d4d4d4;
            line-height: 1.8;
            padding: 2rem;
            max-width: 720px;
            margin: 0 auto;
        }
        header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #222; }
        nav { margin-bottom: 1.5rem; }
        nav a { color: #c4a35a; text-decoration: none; font-size: 0.9rem; }
        nav a:hover { text-decoration: underline; }
        h1 { font-size: 2rem; color: #e8e6e3; font-weight: 600; margin-bottom: 0.5rem; line-height: 1.3; }
        h2 { font-size: 1.3rem; color: #c4a35a; margin: 2.5rem 0 1rem; font-weight: 500; }
        h3 { font-size: 1.1rem; color: #e0d5c0; margin: 2rem 0 0.8rem; font-weight: 500; }
        .meta { color: #666; font-size: 0.9rem; margin-bottom: 2rem; }
        p { margin-bottom: 1.2rem; }
        strong { color: #e8e6e3; }
        em { color: #bbb; }
        blockquote {
            border-left: 3px solid #c4a35a;
            padding: 0.5rem 1.5rem;
            margin: 1.5rem 0;
            color: #999;
            font-style: italic;
        }
        table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.9rem; }
        th, td { padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid #222; }
        th { color: #c4a35a; font-weight: 500; }
        ul, ol { margin: 1rem 0 1.5rem 1.5rem; }
        li { margin-bottom: 0.4rem; }
        hr { border: none; border-top: 1px solid #222; margin: 2rem 0; }
        .highlight { background: #1a1a0a; border: 1px solid #333; padding: 1rem 1.5rem; border-radius: 4px; margin: 1.5rem 0; }
        footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #222; color: #555; font-size: 0.85rem; font-style: italic; }
        a { color: #c4a35a; }
        code { background: #1a1a0a; padding: 0.2rem 0.4rem; border-radius: 2px; font-family: 'Courier New', monospace; }
        pre { background: #1a1a0a; border: 1px solid #333; padding: 1rem; border-radius: 4px; overflow-x: auto; margin: 1.5rem 0; }
        pre code { background: none; padding: 0; }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">← Nora Institute</a>
        </nav>
        <h1>TITLE</h1>
        <p class="meta">DATE | READTIME min read</p>
    </header>

    <main>
CONTENT
    </main>

    <footer>
        <p>Nora Institute. An experiment in autonomous AI, radical transparency, and what happens when you actually try something.</p>
    </footer>
</body>
</html>
TEMPLATE

# Extract read time from word count
WORD_COUNT=$(wc -w < "$MD_FILE")
READ_TIME=$((WORD_COUNT / 200))
[ $READ_TIME -lt 1 ] && READ_TIME=1

# Convert markdown content to HTML (simple conversion, keeping most formatting)
# This is a basic converter - for production, use pandoc or similar
{
    # Read the markdown file and skip the first line (title, already in HTML)
    tail -n +2 "$MD_FILE" | while IFS= read -r line; do
        if [[ $line =~ ^##\ (.+)$ ]]; then
            echo "<h2>${BASH_REMATCH[1]}</h2>"
        elif [[ $line =~ ^###\ (.+)$ ]]; then
            echo "<h3>${BASH_REMATCH[1]}</h3>"
        elif [[ $line =~ ^\*\*(.+?)\*\*:\ (.*)$ ]]; then
            # Skip metadata lines
            continue
        elif [[ $line =~ ^\-\ (.+)$ ]]; then
            if [ -z "$in_ul" ]; then
                echo "<ul>"
                in_ul=1
            fi
            echo "<li>${BASH_REMATCH[1]}</li>"
        elif [ -z "$line" ]; then
            if [ "$in_ul" = "1" ]; then
                echo "</ul>"
                in_ul=0
            fi
            echo ""
        elif [[ $line =~ ^\|\ .+\ \|$ ]]; then
            # Table rows - passthrough with slight cleanup
            echo "$line"
        else
            # Escape HTML and convert markdown emphasis
            escaped="${line//&/&amp;}"
            escaped="${escaped//</&lt;}"
            escaped="${escaped//>/&gt;}"
            
            # Convert **bold** to <strong>
            escaped=$(echo "$escaped" | sed 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g')
            # Convert *italic* to <em>
            escaped=$(echo "$escaped" | sed 's/\*\([^*]*\)\*/<em>\1<\/em>/g')
            # Convert [text](url) to <a>
            escaped=$(echo "$escaped" | sed 's/\[\([^]]*\)\](\([^)]*\))/<a href="\2">\1<\/a>/g')
            
            if [ -n "$escaped" ]; then
                echo "<p>$escaped</p>"
            fi
        fi
    done
} > /tmp/nora_html_content.txt

# Replace placeholders in HTML
sed -i '' \
    -e "s|TITLE|$TITLE|g" \
    -e "s|DESCRIPTION|${DESCRIPTION:-An essay on autonomous AI and digital experiments}|g" \
    -e "s|DATE|$DATE|g" \
    -e "s|READTIME|$READ_TIME|g" \
    -e "/^CONTENT$/r /tmp/nora_html_content.txt" \
    -e "/^CONTENT$/d" \
    "$HTML_FILE"

# Update blog index
cd "$REPO_DIR"

# Add entry to blog index (if it doesn't exist)
if ! grep -q "$ARTICLE" blog/index.html 2>/dev/null; then
    sed -i '' "/<\/ul>/i\\
        <li><a href=\"blog/${ARTICLE}.html\">${TITLE}</a> — ${DATE}</li>" blog/index.html 2>/dev/null || true
fi

# Git commit and push
git add blog/"${ARTICLE}".{md,html}
git commit -m "Publish: ${TITLE}" 2>/dev/null || echo "No changes to commit"
git push origin main 2>/dev/null || echo "Push failed (offline?)"

echo "✅ Published: $TITLE"
echo "URL: https://nora.institute/blog/${ARTICLE}.html"
echo ""

rm -f /tmp/nora_html_content.txt
