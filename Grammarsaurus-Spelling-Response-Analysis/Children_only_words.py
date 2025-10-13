import pandas as pd
import re # For regular expressions
import os # For file path operations
import reportlab # For PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def main():
    
    file_name = input("Enter the filename of the CSV file: ")
    file_name += ".csv"


    file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

    data = pd.read_csv(file_path)
    Raw_data = []

    for row in data["What are two words your class struggles to spell?"]:
        Raw_data.append(str(row))

    print("\nNow Cleansing the Data...")

    # Second, cleanse the data (remove any unwanted characters, emojis etc...)
    for entry in Raw_data:
        entry = entry.replace('\\', ' ') # Remove backslashes and replace with a space
        entry = entry.replace(',', '') # Remove commas
        entry = entry.replace('and', '') # Remove 'and'
    # Remove any emojis from the data
        entry = re.sub(r'[^\x00-\x7F]+', '', entry) # Remove non-ASCII characters
        entry = re.sub(r'[^\x00-\x7F]+', '', entry) # Remove non-ASCII characters

    print(Raw_data)

    print("\nData Cleansed Successfully...")

    word_count = {}

    for row in Raw_data:
        words = row.split()
        for word in words:
            if word:  # Ensure the word is not an empty string
                word = word.lower()  # Convert to lowercase for uniformity
                word_count[word] = word_count.get(word, 0) + 1 

    print("\nWord Count:")
    for word, count in word_count.items():
        print(f"{word}: {count}")

    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    print("\nSorted Word Count:")
    for word, count in sorted_word_count.items():
        print(f"{word}: {count}")

    print("\nGenerating PDF Report...")
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),     # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),      # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),              # Left align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),           # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), '#f9f9f9'),    # Body background color
        ('GRID', (0, 0), (-1, -1), 1, "#242424"),       # Grid lines
    ])

    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("Child Spelling Analysis Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add space after title
    # Create a table to display the word counts
    child_word_data = [["Word", "Frequency"]]
    for word, count in list(sorted_word_count.items())[:20]:  # Top 20 words
        child_word_data.append([word, count])
    
    child_word_table = Table(child_word_data)
    child_word_table.setStyle(table_style)
    elements.append(child_word_table)

    # Create an output path
    output_path = os.path.join(os.path.expanduser("~"), "Documents", "Child_Spelling_Analysis_Report.pdf")
    report = SimpleDocTemplate(str(output_path), pagesize=A4)
    report.build(elements)
    


if __name__ == "__main__":
    main()