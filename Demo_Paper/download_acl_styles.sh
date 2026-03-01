#!/bin/bash

# ACL Style Files Download Script
# Downloads required ACL LaTeX style files for paper compilation

echo "=================================="
echo "ACL Style Files Download Script"
echo "=================================="
echo ""

# Create temporary directory if needed
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 Downloading ACL style files..."
echo ""

# Download acl.sty
if [ -f "acl.sty" ]; then
    echo "⚠️  acl.sty already exists. Skipping download."
else
    echo "⬇️  Downloading acl.sty..."
    curl -L -o acl.sty https://raw.githubusercontent.com/acl-org/acl-style-files/master/latex/acl.sty
    if [ $? -eq 0 ]; then
        echo "✅ acl.sty downloaded successfully"
    else
        echo "❌ Failed to download acl.sty"
        echo "   Please download manually from: https://github.com/acl-org/acl-style-files"
        exit 1
    fi
fi

# Download acl_natbib.bst (bibliography style)
if [ -f "acl_natbib.bst" ]; then
    echo "⚠️  acl_natbib.bst already exists. Skipping download."
else
    echo "⬇️  Downloading acl_natbib.bst..."
    curl -L -o acl_natbib.bst https://raw.githubusercontent.com/acl-org/acl-style-files/master/latex/acl_natbib.bst
    if [ $? -eq 0 ]; then
        echo "✅ acl_natbib.bst downloaded successfully"
    else
        echo "❌ Failed to download acl_natbib.bst"
        echo "   Continuing anyway (paper may still compile with default style)"
    fi
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "You can now compile the paper with:"
echo "  pdflatex master_translator_demo.tex"
echo "  bibtex master_translator_demo"
echo "  pdflatex master_translator_demo.tex"
echo "  pdflatex master_translator_demo.tex"
echo ""
echo "Or use latexmk for automatic compilation:"
echo "  latexmk -pdf master_translator_demo.tex"
echo ""
