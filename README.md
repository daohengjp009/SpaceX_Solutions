# SpaceX ML Project Presentation Generator

This repository contains Python scripts to generate a PowerPoint presentation for the SpaceX Machine Learning project.

## Files

- `SpaceX_ML_Solutions.py`: The main ML code with all model implementations
- `create_spacex_presentation.py`: Python script to generate the PowerPoint presentation
- `convert_to_pdf.py`: Helper script with methods to convert PowerPoint to PDF

## Requirements

To use these scripts, you'll need the following Python packages:

```
pip install python-pptx matplotlib numpy pandas
```

## Usage Instructions

### 1. Generate the PowerPoint Presentation

Run the following command to generate the presentation:

```
python create_spacex_presentation.py
```

This will:
- Create a `charts` directory with visualizations
- Generate charts for your presentation
- Create a PowerPoint file named `SpaceX_ML_Project_Presentation.pptx`

### 2. Convert to PDF

There are several ways to convert the PowerPoint to PDF:

1. **Using the conversion script** (requires additional dependencies):
   ```
   python convert_to_pdf.py
   ```
   This script will provide several options for converting your PowerPoint to PDF.

2. **Manual conversion** (recommended):
   - Open the PowerPoint file in Microsoft PowerPoint or another presentation software
   - Use "Save As" and select PDF as the file format

### 3. Customize the Presentation

To customize the presentation:

1. Edit `create_spacex_presentation.py` to modify:
   - Slide content
   - Chart data
   - Visual styling
   - Number of slides

2. Run the script again to regenerate the presentation

## Presentation Content

The presentation includes the following sections:

1. Title slide
2. Executive Summary
3. Introduction
4. Data Collection & Wrangling methodology
5. Exploratory Data Analysis 
6. Visual Analytics with multiple visualizations
7. SQL Analysis Results
8. Interactive Map Visualization
9. Plotly Dash Dashboard
10. Predictive Analysis Methodology
11. ML Model Comparisons
12. Detailed Model Results
13. Conclusion
14. GitHub Repository

## Note

You may need to adjust the paths and content to match your specific project details and GitHub repository URL.

## License

This project is for educational purposes. 