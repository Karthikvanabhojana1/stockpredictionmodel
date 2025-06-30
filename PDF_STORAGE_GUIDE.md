# 📚 PDF Storage Guide for Soros Chatbot

## 📁 Directory Structure

Your PDFs should be stored in the following organized structure:

```
data/pdfs/
├── README.md                    # Documentation
├── The Alchemy of Finance...pdf # Your main PDF (already here!)
├── processed/                   # PDFs that have been analyzed
├── uploads/                     # Temporary upload storage
└── archive/                     # Backup and archived PDFs
```

## 🎯 Where to Store PDFs

### 1. **Main Directory** (`data/pdfs/`)
- **Purpose**: Primary storage for PDFs you want to process
- **Best for**: PDFs you're actively working with
- **Current**: Your "Alchemy of Finance" PDF is here ✅

### 2. **Processed Directory** (`data/pdfs/processed/`)
- **Purpose**: PDFs that have been analyzed and added to knowledge base
- **Best for**: Moving PDFs after successful processing

### 3. **Uploads Directory** (`data/pdfs/uploads/`)
- **Purpose**: Temporary storage for web uploads
- **Best for**: Automatically managed by the web interface

### 4. **Archive Directory** (`data/pdfs/archive/`)
- **Purpose**: Long-term storage and backups
- **Best for**: PDFs you want to keep but aren't actively using

## 🛠️ Managing PDFs

### Using the Management Script

```bash
# List all PDFs in the system
python manage_pdfs.py list

# Add a new PDF
python manage_pdfs.py add ~/Downloads/new_soros_paper.pdf

# Move a PDF to archive
python manage_pdfs.py move "The Alchemy of Finance - Reading the Mind of the Market 2nd edition 1994.pdf" archive

# Clean temporary uploads
python manage_pdfs.py clean

# Show help
python manage_pdfs.py help
```

### Manual File Management

```bash
# Copy a PDF to the main directory
cp ~/Downloads/soros_essay.pdf data/pdfs/

# Move a PDF to processed after analysis
mv data/pdfs/my_pdf.pdf data/pdfs/processed/

# Archive old PDFs
mv data/pdfs/old_paper.pdf data/pdfs/archive/
```

## 📋 Best Practices

### File Naming
- ✅ Use descriptive names: `soros_reflexivity_1994.pdf`
- ✅ Avoid spaces: use underscores or hyphens
- ✅ Include dates when relevant: `soros_essay_2023.pdf`
- ❌ Avoid: `document1.pdf`, `paper.pdf`

### File Organization
- **Active PDFs**: Keep in main directory
- **Processed PDFs**: Move to `processed/` after analysis
- **Temporary Files**: Let the system handle `uploads/`
- **Backups**: Store in `archive/` for long-term

### File Size Limits
- **Maximum size**: 50MB per PDF
- **Recommended**: Under 20MB for best performance
- **Large files**: Consider splitting into smaller documents

## 🔄 PDF Processing Workflow

1. **Add PDF** → Place in `data/pdfs/`
2. **Process** → System analyzes and extracts knowledge
3. **Move to Processed** → `python manage_pdfs.py move filename.pdf processed`
4. **Archive if needed** → Move to `archive/` for backup

## 🌐 Web Interface Upload

When using the web interface:
1. Drag & drop PDFs in the browser
2. Files are temporarily stored in `uploads/`
3. System processes and extracts knowledge
4. Files can be moved to appropriate directories

## 📊 Current Status

Your system currently has:
- ✅ **1 PDF** in main directory: "The Alchemy of Finance"
- ✅ **Organized structure** with all directories created
- ✅ **Management tools** ready to use

## 🚀 Next Steps

1. **Set your API key** in `.env` file
2. **Start the system**: `./start.sh`
3. **Upload more PDFs** through the web interface
4. **Use the management script** to organize files

## 🔍 Troubleshooting

### PDF Not Found
```bash
# Check if PDF exists
python manage_pdfs.py list

# Add missing PDF
python manage_pdfs.py add /path/to/your/pdf.pdf
```

### File Too Large
```bash
# Check file size
ls -lh your_file.pdf

# Split large PDFs or compress them
# Maximum size: 50MB
```

### Permission Issues
```bash
# Ensure directories are writable
chmod 755 data/pdfs/
chmod 755 data/pdfs/*/
```

## 📞 Quick Commands Reference

```bash
# View all PDFs
python manage_pdfs.py list

# Add new PDF
python manage_pdfs.py add /path/to/pdf

# Move PDF to archive
python manage_pdfs.py move filename.pdf archive

# Clean temporary files
python manage_pdfs.py clean

# Get help
python manage_pdfs.py help
```

---

**Your PDF "The Alchemy of Finance" is already properly stored and ready for processing!** 🎉 