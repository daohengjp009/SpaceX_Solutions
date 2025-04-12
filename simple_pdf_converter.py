"""
Simple PowerPoint to PDF Converter Guide

This script provides simple guidance for converting your PowerPoint to PDF.
"""

import os
import platform
import webbrowser

def main():
    pptx_file = "SpaceX_ML_Project_Presentation.pptx"
    
    if not os.path.exists(pptx_file):
        print(f"Error: PowerPoint file '{pptx_file}' not found.")
        return
        
    print("PowerPoint to PDF Conversion Guide")
    print("==================================")
    print(f"Found presentation: {pptx_file}")
    
    system = platform.system()
    print(f"Detected OS: {system}")
    
    print("\nHere's how to convert your presentation to PDF:")
    
    if system == "Windows":
        print("\nOn Windows:")
        print("1. Right-click on the PowerPoint file")
        print("2. Select 'Open with' > 'PowerPoint'")
        print("3. In PowerPoint, go to File > Export > Create PDF/XPS Document")
        print("4. Click 'Create PDF/XPS'")
        print("5. Choose a location and filename, then click 'Publish'")
        
    elif system == "Darwin":  # macOS
        print("\nOn macOS:")
        print("1. Double-click the PowerPoint file to open it in PowerPoint")
        print("2. Go to File > Save As...")
        print("3. From the 'Format' dropdown, select 'PDF'")
        print("4. Choose a location and click 'Save'")
        
    elif system == "Linux":
        print("\nOn Linux:")
        print("1. If you have LibreOffice installed, open the file with LibreOffice Impress")
        print("2. Go to File > Export As > Export as PDF")
        print("3. Configure the options and click 'Export'")
        print("\nOR using command line with LibreOffice:")
        print(f"libreoffice --headless --convert-to pdf {pptx_file}")
        
    print("\nOnline Conversion Options:")
    print("You can also use online converters:")
    
    online_options = [
        {"name": "Adobe PDF converter", "url": "https://www.adobe.com/acrobat/online/ppt-to-pdf.html"},
        {"name": "SmallPDF", "url": "https://smallpdf.com/ppt-to-pdf"},
        {"name": "iLovePDF", "url": "https://www.ilovepdf.com/powerpoint_to_pdf"}
    ]
    
    for i, option in enumerate(online_options, 1):
        print(f"{i}. {option['name']}: {option['url']}")
    
    # Ask if the user wants to open an online converter
    print("\nWould you like to open an online converter? (y/n)")
    choice = input().lower()
    
    if choice == 'y':
        print("Which converter would you like to use? (1-3)")
        try:
            converter_choice = int(input())
            if 1 <= converter_choice <= len(online_options):
                print(f"Opening {online_options[converter_choice-1]['name']}...")
                webbrowser.open(online_options[converter_choice-1]['url'])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print("\nAfter conversion, make sure to:")
    print("1. Name your PDF 'SpaceX_ML_Project_Presentation.pdf'")
    print("2. Check that all slides and formatting appear correctly")
    print("3. Ensure all charts and images are clearly visible")

if __name__ == "__main__":
    main() 