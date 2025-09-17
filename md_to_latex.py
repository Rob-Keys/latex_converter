#!/usr/bin/env python3
"""
Write me a python file that converts markdown files to latex. I only care about certain features so it only needs to convert these: Headings/text of different sizes, bullet points, numbered lists, tabs, blank lines, whitespace spaces, bold, italics, underline, superscript, subscript, and special unicode characters that latex doesnt recognize. So like ℕ, U+2115, which is \natnums, and other set theory notation
"""

import re
import sys
import argparse
from pathlib import Path

class MarkdownToLatexConverter:
    def __init__(self):
        # Unicode to LaTeX mapping for mathematical symbols
        self.unicode_map = {
            # Set theory and number theory
            'ℕ': r'\mathbb{N}',  # Natural numbers
            'ℤ': r'\mathbb{Z}',  # Integers
            'ℚ': r'\mathbb{Q}',  # Rationals
            'ℝ': r'\mathbb{R}',  # Reals
            'ℂ': r'\mathbb{C}',  # Complex numbers
            '∅': r'\emptyset',   # Empty set
            '∈': r'\in',         # Element of
            '∉': r'\notin',      # Not element of
            '⊆': r'\subseteq',   # Subset or equal
            '⊂': r'\subset',     # Proper subset
            '⊇': r'\supseteq',   # Superset or equal
            '⊃': r'\supset',     # Proper superset
            '∪': r'\cup',        # Union
            '∩': r'\cap',        # Intersection
            '∖': r'\setminus',   # Set difference
            '△': r'\triangle',   # Symmetric difference
            '×': r'\times',      # Cartesian product
            
            # Logic symbols
            '∧': r'\land',       # Logical and
            '∨': r'\lor',        # Logical or
            '¬': r'\neg',        # Logical not
            '→': r'\rightarrow', # Implies
            '↔': r'\leftrightarrow', # If and only if
            '∀': r'\forall',     # For all
            '∃': r'\exists',     # There exists
            '∄': r'\nexists',    # There does not exist
            
            # Relations and operators
            '≤': r'\leq',        # Less than or equal
            '≥': r'\geq',        # Greater than or equal
            '≠': r'\neq',        # Not equal
            '≡': r'\equiv',      # Equivalent
            '≈': r'\approx',     # Approximately equal
            '∞': r'\infty',      # Infinity
            '∑': r'\sum',        # Summation
            '∏': r'\prod',       # Product
            '∫': r'\int',        # Integral
            '∂': r'\partial',    # Partial derivative
            '∇': r'\nabla',      # Nabla
            
            # Greek letters (common ones)
            'α': r'\alpha',      'β': r'\beta',       'γ': r'\gamma',
            'δ': r'\delta',      'ε': r'\epsilon',    'ζ': r'\zeta',
            'η': r'\eta',        'θ': r'\theta',      'ι': r'\iota',
            'κ': r'\kappa',      'λ': r'\lambda',     'μ': r'\mu',
            'ν': r'\nu',         'ξ': r'\xi',         'π': r'\pi',
            'ρ': r'\rho',        'σ': r'\sigma',      'τ': r'\tau',
            'υ': r'\upsilon',    'φ': r'\phi',        'χ': r'\chi',
            'ψ': r'\psi',        'ω': r'\omega',
            'Α': r'\Alpha',      'Β': r'\Beta',       'Γ': r'\Gamma',
            'Δ': r'\Delta',      'Ε': r'\Epsilon',    'Ζ': r'\Zeta',
            'Η': r'\Eta',        'Θ': r'\Theta',      'Ι': r'\Iota',
            'Κ': r'\Kappa',      'Λ': r'\Lambda',     'Μ': r'\Mu',
            'Ν': r'\Nu',         'Ξ': r'\Xi',         'Π': r'\Pi',
            'Ρ': r'\Rho',        'Σ': r'\Sigma',      'Τ': r'\Tau',
            'Υ': r'\Upsilon',    'Φ': r'\Phi',        'Χ': r'\Chi',
            'Ψ': r'\Psi',        'Ω': r'\Omega',
        }

    def convert_unicode_chars(self, text):
        """Convert unicode mathematical symbols to LaTeX commands"""
        for unicode_char, latex_cmd in self.unicode_map.items():
            text = text.replace(unicode_char, f'${latex_cmd}$')
        return text

    def convert_headings(self, text):
        """Convert markdown headings to LaTeX sections"""
        # Convert headings (# ## ### etc.)
        text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^##### (.+)$', r'\\subparagraph{\1}', text, flags=re.MULTILINE)
        return text

    def convert_formatting(self, text):
        """Convert bold, italic, underline, superscript, subscript"""
        # Bold: **text** or __text__
        text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'__(.+?)__', r'\\textbf{\1}', text)
        
        # Italic: *text* or _text_ (but not if it's part of bold)
        text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\\textit{\1}', text)
        text = re.sub(r'(?<!_)_([^_]+?)_(?!_)', r'\\textit{\1}', text)
        
        # Underline: <u>text</u>
        text = re.sub(r'<u>(.+?)</u>', r'\\underline{\1}', text)
        
        # Superscript: ^text^ or text^superscript^
        text = re.sub(r'\^(.+?)\^', r'\\textsuperscript{\1}', text)
        
        # Subscript: ~text~ or text~subscript~
        text = re.sub(r'~(.+?)~', r'\\textsubscript{\1}', text)
        
        return text

    def convert_lists(self, text):
        """Convert bullet points and numbered lists"""
        lines = text.split('\n')
        result = []
        in_itemize = False
        in_enumerate = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Bullet points
            if re.match(r'^(\s*)[*+-] (.+)', line):
                if not in_itemize:
                    result.append('\\begin{itemize}')
                    in_itemize = True
                if in_enumerate:
                    result.append('\\end{enumerate}')
                    in_enumerate = False
                    
                match = re.match(r'^(\s*)[*+-] (.+)', line)
                indent_level = len(match.group(1)) // 2
                item_text = match.group(2)
                result.append('  ' * indent_level + f'\\item {item_text}')
                
            # Numbered lists
            elif re.match(r'^(\s*)\d+\. (.+)', line):
                if not in_enumerate:
                    result.append('\\begin{enumerate}')
                    in_enumerate = True
                if in_itemize:
                    result.append('\\end{itemize}')
                    in_itemize = False
                    
                match = re.match(r'^(\s*)\d+\. (.+)', line)
                indent_level = len(match.group(1)) // 2
                item_text = match.group(2)
                result.append('  ' * indent_level + f'\\item {item_text}')
                
            else:
                # End lists if we're not in a list item anymore
                if in_itemize:
                    result.append('\\end{itemize}')
                    in_itemize = False
                if in_enumerate:
                    result.append('\\end{enumerate}')
                    in_enumerate = False
                result.append(line)
            
            i += 1
        
        # Close any remaining open lists
        if in_itemize:
            result.append('\\end{itemize}')
        if in_enumerate:
            result.append('\\end{enumerate}')
            
        return '\n'.join(result)

    def preserve_whitespace(self, text):
        """Handle tabs and preserve important whitespace"""
        # Convert tabs to spaces (LaTeX doesn't handle tabs well)
        text = text.expandtabs(4)
        
        # Preserve multiple spaces within lines
        text = re.sub(r' {2,}', lambda m: '\\hspace{' + str(len(m.group(0)) * 0.3) + 'em}', text)
        
        return text

    def handle_blank_lines(self, text):
        """Convert blank lines to proper LaTeX paragraph breaks"""
        # Multiple consecutive blank lines become paragraph breaks
        text = re.sub(r'\n\s*\n\s*\n+', r'\n\n\\vspace{\\baselineskip}\n\n', text)
        return text

    def escape_latex_chars(self, text):
        """Escape special LaTeX characters"""
        # Characters that need escaping in LaTeX
        escape_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '\\': r'\textbackslash{}',
        }
        
        # Apply escaping, but be careful not to escape our LaTeX commands
        for char, escaped in escape_chars.items():
            # Use negative lookbehind/lookahead to avoid escaping LaTeX commands
            if char in ['$', '^', '_', '~']:  # These we handle specially due to our formatting
                continue
            text = text.replace(char, escaped)
        
        return text

    def add_latex_preamble(self, content):
        """Add LaTeX document structure"""
        preamble = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage[normalem]{ulem}

\begin{document}

"""
        
        postamble = r"""
\end{document}"""
        
        return preamble + content + postamble

    def convert(self, markdown_text, add_document_structure=True):
        """Main conversion function"""
        text = markdown_text
        
        # Step 1: Escape LaTeX special characters (but not our markdown syntax)
        # We'll do this carefully to avoid interfering with our conversions
        
        # Step 2: Convert unicode characters first
        text = self.convert_unicode_chars(text)
        
        # Step 3: Convert headings
        text = self.convert_headings(text)
        
        # Step 4: Convert formatting (bold, italic, etc.)
        text = self.convert_formatting(text)
        
        # Step 5: Convert lists
        text = self.convert_lists(text)
        
        # Step 6: Handle whitespace and blank lines
        text = self.preserve_whitespace(text)
        text = self.handle_blank_lines(text)
        
        # Step 7: Escape remaining LaTeX characters
        text = self.escape_latex_chars(text)
        
        # Step 8: Add LaTeX document structure if requested
        if add_document_structure:
            text = self.add_latex_preamble(text)
        
        return text

    def convert_file(self, input_path, output_path=None):
        """Convert a markdown file to LaTeX"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file {input_path} not found")
        
        if output_path is None:
            output_path = input_path.with_suffix('.tex')
        else:
            output_path = Path(output_path)
        
        # Read the markdown file
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to LaTeX
        latex_content = self.convert(markdown_content)
        
        # Write the LaTeX file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"Converted {input_path} to {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to LaTeX')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output LaTeX file (default: input file with .tex extension)')
    parser.add_argument('-o', '--output-file', help='Output LaTeX file (alternative to positional argument)')
    parser.add_argument('--template', help='LaTeX template file to use')
    parser.add_argument('--no-document', action='store_true', help='Don\'t add LaTeX document structure')
    
    args = parser.parse_args()
    
    # Handle output file specification (positional or -o flag)
    output_file = args.output or args.output_file
    
    converter = MarkdownToLatexConverter()
    
    try:
        if args.no_document:
            # Just convert the content without document structure
            with open(args.input, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            latex_content = converter.convert(markdown_content, add_document_structure=False)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                print(f"Converted {args.input} to {output_file}")
            else:
                print(latex_content)
        else:
            converter.convert_file(args.input, output_file, args.template)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()