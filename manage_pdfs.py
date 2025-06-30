#!/usr/bin/env python3
"""
PDF Management Script for Soros Chatbot
Helps organize and process PDF files
"""

import os
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import configuration
sys.path.append(str(Path(__file__).parent))
from config import Config

def list_pdfs():
    """List all PDFs in the system"""
    print("📚 PDF Files in Soros Chatbot")
    print("=" * 50)
    
    # Main PDF directory
    main_pdfs = list(Config.PDF_DIR.glob("*.pdf"))
    if main_pdfs:
        print(f"\n📁 Main Directory ({Config.PDF_DIR}):")
        for pdf in main_pdfs:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"   📄 {pdf.name} ({size_mb:.1f}MB)")
    
    # Processed directory
    processed_pdfs = list(Config.PDF_PROCESSED_DIR.glob("*.pdf"))
    if processed_pdfs:
        print(f"\n✅ Processed Directory ({Config.PDF_PROCESSED_DIR}):")
        for pdf in processed_pdfs:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"   📄 {pdf.name} ({size_mb:.1f}MB)")
    
    # Uploads directory
    upload_pdfs = list(Config.PDF_UPLOADS_DIR.glob("*.pdf"))
    if upload_pdfs:
        print(f"\n📤 Uploads Directory ({Config.PDF_UPLOADS_DIR}):")
        for pdf in upload_pdfs:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"   📄 {pdf.name} ({size_mb:.1f}MB)")
    
    # Archive directory
    archive_pdfs = list(Config.PDF_ARCHIVE_DIR.glob("*.pdf"))
    if archive_pdfs:
        print(f"\n🗄️  Archive Directory ({Config.PDF_ARCHIVE_DIR}):")
        for pdf in archive_pdfs:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"   📄 {pdf.name} ({size_mb:.1f}MB)")
    
    total_pdfs = len(main_pdfs) + len(processed_pdfs) + len(upload_pdfs) + len(archive_pdfs)
    print(f"\n📊 Total PDFs: {total_pdfs}")

def add_pdf(pdf_path):
    """Add a PDF to the main directory"""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"❌ Error: File {pdf_path} does not exist")
        return False
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"❌ Error: {pdf_path} is not a PDF file")
        return False
    
    # Check file size
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    if size_mb > Config.MAX_PDF_SIZE_MB:
        print(f"❌ Error: File too large ({size_mb:.1f}MB > {Config.MAX_PDF_SIZE_MB}MB)")
        return False
    
    # Copy to main PDF directory
    dest_path = Config.PDF_DIR / pdf_path.name
    
    # Handle naming conflicts
    counter = 1
    while dest_path.exists():
        name = pdf_path.stem + f"_{counter}" + pdf_path.suffix
        dest_path = Config.PDF_DIR / name
        counter += 1
    
    try:
        shutil.copy2(pdf_path, dest_path)
        print(f"✅ Added {pdf_path.name} to {Config.PDF_DIR}")
        print(f"   Size: {size_mb:.1f}MB")
        return True
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return False

def move_pdf(pdf_name, destination):
    """Move a PDF to a different directory"""
    # Find the PDF
    pdf_path = None
    for directory in [Config.PDF_DIR, Config.PDF_PROCESSED_DIR, Config.PDF_UPLOADS_DIR, Config.PDF_ARCHIVE_DIR]:
        potential_path = directory / pdf_name
        if potential_path.exists():
            pdf_path = potential_path
            break
    
    if not pdf_path:
        print(f"❌ Error: PDF '{pdf_name}' not found")
        return False
    
    # Determine destination
    if destination.lower() in ['processed', 'process']:
        dest_dir = Config.PDF_PROCESSED_DIR
    elif destination.lower() in ['uploads', 'upload']:
        dest_dir = Config.PDF_UPLOADS_DIR
    elif destination.lower() in ['archive', 'arch']:
        dest_dir = Config.PDF_ARCHIVE_DIR
    elif destination.lower() in ['main', 'root']:
        dest_dir = Config.PDF_DIR
    else:
        print(f"❌ Error: Unknown destination '{destination}'")
        print("   Valid destinations: processed, uploads, archive, main")
        return False
    
    # Move the file
    dest_path = dest_dir / pdf_name
    try:
        shutil.move(str(pdf_path), str(dest_path))
        print(f"✅ Moved {pdf_name} to {dest_dir}")
        return True
    except Exception as e:
        print(f"❌ Error moving file: {e}")
        return False

def clean_uploads():
    """Clean up temporary upload files"""
    upload_files = list(Config.PDF_UPLOADS_DIR.glob("*.pdf"))
    
    if not upload_files:
        print("📤 No files in uploads directory to clean")
        return
    
    print(f"🧹 Cleaning {len(upload_files)} files from uploads directory...")
    
    for pdf_file in upload_files:
        try:
            pdf_file.unlink()
            print(f"   🗑️  Deleted {pdf_file.name}")
        except Exception as e:
            print(f"   ❌ Error deleting {pdf_file.name}: {e}")
    
    print("✅ Upload directory cleaned")

def show_help():
    """Show help information"""
    print("📚 PDF Management Script")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python manage_pdfs.py list                    # List all PDFs")
    print("  python manage_pdfs.py add <path>              # Add a PDF")
    print("  python manage_pdfs.py move <name> <dest>      # Move a PDF")
    print("  python manage_pdfs.py clean                   # Clean uploads")
    print("  python manage_pdfs.py help                    # Show this help")
    print()
    print("Destinations for move:")
    print("  main      - Main PDF directory")
    print("  processed - Processed PDFs")
    print("  uploads   - Temporary uploads")
    print("  archive   - Archived PDFs")
    print()
    print("Examples:")
    print("  python manage_pdfs.py add ~/Downloads/soros_essay.pdf")
    print("  python manage_pdfs.py move my_pdf.pdf archive")
    print("  python manage_pdfs.py clean")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_pdfs()
    elif command == 'add':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide a PDF path")
            print("Usage: python manage_pdfs.py add <path>")
            return
        add_pdf(sys.argv[2])
    elif command == 'move':
        if len(sys.argv) < 4:
            print("❌ Error: Please provide PDF name and destination")
            print("Usage: python manage_pdfs.py move <name> <dest>")
            return
        move_pdf(sys.argv[2], sys.argv[3])
    elif command == 'clean':
        clean_uploads()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    # Ensure directories exist
    Config.ensure_directories()
    main() 