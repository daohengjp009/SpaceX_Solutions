"""
Convert PowerPoint to PDF

This script shows different methods to convert PPTX to PDF.
Note: These methods require different external dependencies.
Choose the one that works best for your environment.
"""

import os
import sys
import subprocess

def main():
    print("PowerPoint to PDF Conversion Options")
    print("====================================")
    
    pptx_file = "SpaceX_ML_Project_Presentation.pptx"
    pdf_file = "SpaceX_ML_Project_Presentation.pdf"
    
    if not os.path.exists(pptx_file):
        print(f"Error: Presentation file '{pptx_file}' not found.")
        return
    
    print(f"Source file: {pptx_file}")
    print(f"Target PDF: {pdf_file}")
    print("\nChoose a conversion method:")
    
    # Method 1: Using LibreOffice (if installed)
    print("\nMethod 1: Using LibreOffice")
    print("This requires LibreOffice to be installed on your system.")
    print("Command to run:")
    print(f"soffice --headless --convert-to pdf {pptx_file}")
    
    # Method 2: Using unoconv (requires LibreOffice and unoconv)
    print("\nMethod 2: Using unoconv")
    print("Requires LibreOffice and unoconv to be installed.")
    print("Install unoconv using: pip install unoconv")
    print("Command to run:")
    print(f"unoconv -f pdf {pptx_file}")
    
    # Method 3: Using comtypes (Windows only)
    print("\nMethod 3: Using comtypes (Windows only)")
    print("This requires PowerPoint to be installed on your Windows system.")
    print("Install comtypes using: pip install comtypes")
    print("Python code to run:")
    print("""
    import comtypes.client
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = True
    presentation = powerpoint.Presentations.Open(pptx_path)
    presentation.SaveAs(pdf_path, 32)  # 32 is the PDF format code
    presentation.Close()
    powerpoint.Quit()
    """)
    
    # Method 4: Using python-pptx and pdf libraries (complex)
    print("\nMethod 4: Using python-pptx and reportlab/fpdf")
    print("This is a complex method that converts each slide to an image and then to PDF.")
    print("Requires: pip install python-pptx Pillow reportlab")
    
    # Method 5: Online conversion
    print("\nMethod 5: Online conversion")
    print("Upload your PowerPoint to an online converter like:")
    print("- https://www.adobe.com/acrobat/online/ppt-to-pdf.html")
    print("- https://smallpdf.com/ppt-to-pdf")
    print("- https://www.ilovepdf.com/powerpoint_to_pdf")
    
    # Method 6: On macOS - use Automator/AppleScript
    if sys.platform == 'darwin':
        print("\nMethod 6: Using macOS Automator/AppleScript")
        print("You can create an Automator workflow or use the following AppleScript:")
        print("""
        tell application "Microsoft PowerPoint"
            open POSIX file "/path/to/presentation.pptx"
            set pres to active presentation
            save as pres filename POSIX file "/path/to/output.pdf" file format PDF file format
            close pres
            quit
        end tell
        """)
    
    # Method 7: Using subprocess to call PowerPoint (macOS)
    if sys.platform == 'darwin':
        print("\nMethod 7: Using osascript on macOS")
        print("This uses AppleScript via osascript to control PowerPoint.")
        print("Attempting to convert using osascript...")
        
        try:
            # Get absolute paths
            absolute_pptx_path = os.path.abspath(pptx_file)
            absolute_pdf_path = os.path.abspath(pdf_file)
            
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
            
            # Ask the user if they want to run this script
            print("\nWould you like to attempt conversion using AppleScript? (y/n)")
            choice = input().lower()
            
            if choice == 'y':
                print("Running AppleScript to convert PowerPoint to PDF...")
                subprocess.run(['osascript', '-e', applescript])
                
                # Check if the PDF was created
                if os.path.exists(pdf_file):
                    print(f"Success! PDF created at: {pdf_file}")
                else:
                    print("Conversion failed. The PDF was not created.")
            else:
                print("AppleScript conversion cancelled.")
                
        except Exception as e:
            print(f"Error during conversion: {e}")
    
    print("\nChoose the method that works best for your system configuration.")
    print("For most reliable results, open the PowerPoint file manually and use 'Save As' to save as PDF.")

if __name__ == "__main__":
    main() 