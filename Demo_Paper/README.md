# Master Translator Demo Paper

Academic demo paper for ACL/EMNLP Demo Track submission.

## 📄 Paper Information

- **Title**: Master Translator: An Intelligent Chunking-Based System for Long Document Translation with Real-Time Visualization
- **Format**: ACL 2-column format, 4-6 pages including references
- **Target Venues**: ACL 2026 Demo Track, EMNLP 2025 Demo Track
- **Status**: Draft (ready for review)

## 📋 Prerequisites

### LaTeX Distribution
You need a complete LaTeX distribution installed:

- **macOS**: MacTeX
  ```bash
  brew install --cask mactex
  ```

- **Linux**: TeX Live
  ```bash
  sudo apt-get install texlive-full
  ```

- **Windows**: MiKTeX
  - Download from: https://miktex.org/download

### Required Files
Ensure you have:
- `master_translator_demo.tex` - Main paper source
- `references.bib` - Bibliography file
- `acl.sty` - ACL style file (download from ACL website if not included)

## 🔨 Compilation

### Method 1: Full Compilation with Bibliography

```bash
# Navigate to the Demo_Paper directory
cd /path/to/Master-Translator-Web/Demo_Paper

# First pass: compile LaTeX
pdflatex master_translator_demo.tex

# Process bibliography
bibtex master_translator_demo

# Second pass: resolve references
pdflatex master_translator_demo.tex

# Third pass: ensure all references are correct
pdflatex master_translator_demo.tex
```

### Method 2: Quick Compilation (without updating bibliography)

```bash
pdflatex master_translator_demo.tex
```

Use this when you're only making text changes and haven't modified references.

### Method 3: Using latexmk (Recommended)

```bash
# Automatically handles all compilation passes
latexmk -pdf master_translator_demo.tex

# Clean auxiliary files after compilation
latexmk -c
```

## 📦 Output

After successful compilation, you'll find:
- **master_translator_demo.pdf** - The compiled paper (this is what you submit!)

Auxiliary files (can be deleted):
- `*.aux`, `*.log`, `*.bbl`, `*.blg`, `*.out` - Compilation artifacts

## ✅ Verification Checklist

Before submission, verify:

### Content
- [ ] Title and author information are correct
- [ ] Abstract is 150-200 words
- [ ] All sections are complete (Introduction → Conclusion)
- [ ] Figures/tables have captions and are referenced in text
- [ ] All citations appear in bibliography
- [ ] Appendix includes technical details

### Formatting
- [ ] Paper compiles without errors
- [ ] Paper is 4-6 pages (including references)
- [ ] Font size is 11pt
- [ ] Margins meet ACL requirements
- [ ] Line numbers appear (for review submission)

### References
- [ ] All cited works appear in references.bib
- [ ] Bibliography appears at end of paper
- [ ] Citations format is correct (e.g., \cite{}, \citet{})
- [ ] URLs are properly formatted

### Technical Details
- [ ] System architecture diagram is clear
- [ ] Code examples are properly formatted
- [ ] Tables have professional formatting
- [ ] Equations (if any) render correctly

## 🐛 Troubleshooting

### Error: "acl.sty not found"
**Solution**: Download the ACL style file:
```bash
# Download from ACL GitHub
wget https://raw.githubusercontent.com/acl-org/acl-style-files/master/acl.sty
```

### Error: "Bibliography not found"
**Solution**: Make sure you've run `bibtex` after the first `pdflatex` compilation:
```bash
pdflatex master_translator_demo.tex
bibtex master_translator_demo
pdflatex master_translator_demo.tex
```

### Error: "Undefined citations"
**Solution**: Run `pdflatex` multiple times (typically 3 passes):
```bash
pdflatex master_translator_demo.tex  # Pass 1
bibtex master_translator_demo        # Process bibliography
pdflatex master_translator_demo.tex  # Pass 2 - resolve citations
pdflatex master_translator_demo.tex  # Pass 3 - ensure all references
```

### Warning: "Overfull \hbox"
**Solution**: This means text extends into the margin. Common fixes:
- Break long URLs with `\url{}`
- Add hyphenation hints: `al\-go\-rithm`
- Rephrase sentences to fit better

### Paper too long (>6 pages)
**Solutions**:
- Move detailed algorithms to appendix
- Reduce figure sizes
- Condense related work section
- Use tables instead of prose for comparisons

## 📊 Word Count

To check word count (approximate):
```bash
# macOS/Linux
pdftotext master_translator_demo.pdf - | wc -w

# Or use texcount
texcount master_translator_demo.tex
```

Typical ACL Demo Paper: 3,000-4,500 words

## 📝 Submission Instructions

### For ACL/EMNLP Demo Track:

1. **Anonymize** (for initial review):
   - Remove author names and affiliations
   - Anonymize GitHub URLs and system names if requested
   - Add `\usepackage[review]{acl}` in preamble

2. **Prepare Supplementary Materials**:
   - Demo video (5 minutes max, MP4 format)
   - System access link (or installation instructions)
   - Optional: code repository snapshot

3. **Submit via START**:
   - Create account at https://www.softconf.com/
   - Upload PDF to appropriate track
   - Fill in metadata (title, abstract, keywords)
   - Upload supplementary materials

4. **After Acceptance**:
   - De-anonymize the paper
   - Incorporate reviewer feedback
   - Prepare camera-ready version
   - Update with final DOI/conference info

## 📚 Resources

### ACL Style Guidelines
- Official ACL template: https://github.com/acl-org/acl-style-files
- Formatting instructions: https://acl-org.github.io/ACLPUB/formatting.html
- Demo Track CFP: Check ACL/EMNLP websites for current year

### LaTeX Resources
- Overleaf ACL template: https://www.overleaf.com/latex/templates/acl-conference-proceedings/vdkpsbzrvphg
- LaTeX Wikibook: https://en.wikibooks.org/wiki/LaTeX
- TeX Stack Exchange: https://tex.stackexchange.com/

### Demo Paper Examples
- Past ACL Demo Papers: https://aclanthology.org/ (filter by "Demo")
- Exemplary demos with code: Look for papers with GitHub stars

## 🔄 Version Control

Recommended workflow:

```bash
# Track changes with git
git add master_translator_demo.tex references.bib
git commit -m "Draft v1.0: Complete first draft"

# Create version snapshots before major revisions
cp master_translator_demo.tex master_translator_demo_v1.0.tex
```

## 📧 Contact

For questions about this paper:
- **Author**: Polly
- **Email**: polly@example.com
- **GitHub**: https://github.com/Polly2014/Master-Translator-Web

---

**Good luck with your submission! 🎉**

