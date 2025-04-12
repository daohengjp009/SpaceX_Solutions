"""
Convert PowerPoint to PDF using AppleScript on macOS

This script directly converts a PowerPoint file to PDF using AppleScript
without requiring user interaction.
"""

import os
import subprocess

def convert_to_pdf(pptx_file, pdf_file=None):
    """
    Convert PowerPoint to PDF using AppleScript on macOS
    
    Args:
        pptx_file (str): Path to the PowerPoint file
        pdf_file (str, optional): Path for the output PDF file. If None, uses the same name as PPTX.
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    if not os.path.exists(pptx_file):
        print(f"Error: File '{pptx_file}' not found.")
        return False
    
    # If no PDF file path provided, use the same name as the PPTX but with .pdf extension
    if pdf_file is None:
        pdf_file = os.path.splitext(pptx_file)[0] + ".pdf"
    
    # Get absolute paths
    absolute_pptx_path = os.path.abspath(pptx_file)
    absolute_pdf_path = os.path.abspath(pdf_file)
    
    print(f"Converting: {absolute_pptx_path}")
    print(f"Output PDF: {absolute_pdf_path}")
    
    # AppleScript to convert PPTX to PDF
    applescript = f'''
    tell application "Microsoft PowerPoint"
        open POSIX file "{absolute_pptx_path}"
        set pres to active presentation
        save as pres filename POSIX file "{absolute_pdf_path}" file format PDF file format
        close pres saving no
        quit
    end tell
    '''
    
    try:
        print("Running AppleScript to convert PowerPoint to PDF...")
        result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        # Check if the PDF was created
        if os.path.exists(pdf_file):
            print(f"Success! PDF created at: {pdf_file}")
            return True
        else:
            print("Conversion failed. The PDF was not created.")
            return False
            
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

if __name__ == "__main__":
    pptx_file = "SpaceX_ML_Project_Presentation.pptx"
    convert_to_pdf(pptx_file) 