# Option 1 — pandoc 
pandoc ebook-abcdesktop-en.md -o ebook-abcdesktop-en.pdf --pdf-engine=weasyprint --metadata title="abcdesktop.io"

# Option 2 — pandoc to HTML
pandoc ebook-abcdesktop-en.md -o ebook-abcdesktop-en.html -s --metadata title="abcdesktop.io"
