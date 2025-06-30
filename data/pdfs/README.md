# PDF Storage Directory

This directory is for storing PDF files that will be processed by the Soros Chatbot.

## Structure

```
data/pdfs/
├── README.md           # This file
├── processed/          # PDFs that have been processed and analyzed
├── uploads/            # Temporary storage for uploaded PDFs
└── archive/            # Archived or backup PDFs
```

## Usage

### For Development/Testing
- Place PDF files directly in the root of this directory
- The system will automatically detect and process them
- Example: `data/pdfs/soros_essay.pdf`

### For Production
- Upload PDFs through the web interface
- They will be stored in `uploads/` temporarily
- Processed content is stored in the knowledge base
- Original files can be moved to `archive/` for backup

### Supported Formats
- PDF files (.pdf)
- Maximum file size: 50MB (configurable)
- Text-based PDFs work best (scanned PDFs may have limited text extraction)

## File Naming
- Use descriptive names: `soros_reflexivity_theory.pdf`
- Avoid spaces: use underscores or hyphens
- Include date if relevant: `soros_1994_alchemy_finance.pdf`

## Processing
When a PDF is loaded:
1. Text is extracted and cleaned
2. Content is chunked for AI processing
3. Key quotes and concepts are identified
4. Metadata is stored (title, author, date, etc.)
5. Content is added to the knowledge base

## Security
- Only PDF files are accepted
- Files are scanned for malicious content
- Uploaded files are processed in a sandboxed environment 