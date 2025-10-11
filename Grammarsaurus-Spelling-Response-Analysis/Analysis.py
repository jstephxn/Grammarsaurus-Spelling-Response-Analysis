import pandas as pd
import re # For regular expressions
import os # For file path operations
import reportlab # For PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet



def build_report(location_count, sorted_word_count, location_word_count, word_count):

    elements = []

    styles = getSampleStyleSheet()

    # Set the style for the normal text
    wrap_style = styles['Normal']

    # Set the style for the tables
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),     # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),      # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),              # Left align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),           # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), '#f9f9f9'),    # Body background color
        ('GRID', (0, 0), (-1, -1), 1, "#242424"),       # Grid lines
    ])



    # Create a table to display the total responses per location
    location_table_data = [["Location", "Number of Responses"]]
    for location, count in location_count.items():
        location_table_data.append([location, count])
    
    location_table = Table(location_table_data)
    location_table.setStyle(table_style)
    elements.append(location_table)

    # Create a table to display the most common words overall
    word_table_data = [["Word", "Frequency"]]
    for word, count in list(sorted_word_count.items())[:20]:  # Top 20 words
        word_table_data.append([word, count])

    common_word_table = Table(word_table_data)
    common_word_table.setStyle(table_style)
    elements.append(common_word_table)

    # Create tables to display the most common words per location
    location_word_tables = {}
    for location, words in location_word_count.items():
        word_table_data = [["Word", "Frequency"]]
        sorted_words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
        for word, count in list(sorted_words.items())[:10]:  # Top 10 words per location
            word_table_data.append([word, count])
        location_word_tables[location] = word_table_data
    
    words_per_location_table = Table(location_word_tables)
    words_per_location_table.setStyle(table_style)
    elements.append(words_per_location_table)

    # Create an output path
    output_path = os.path.join(os.path.expanduser("~"), "Documents", "Spelling_Analysis_Report.pdf")

    # Now, let's add the elements to the PDF
    report = SimpleDocTemplate("Spelling_Analysis_Report.pdf", pagesize=A4)
    report.build(elements)





def analyze_data(data):
    # Create an empty list to store data
    Raw_data = []
    # first extract the relevant columns from the dataframe
    for index, row in data.iterrows():
        Raw_data.append([str(row['Timestamp']), str(row['What are two words your class struggles to spell?']), str(row['What are two words you struggle to spell? (Don\'t worry about the spelling.)'])])

    print("\nNow Cleansing the Data...")

    # Second, cleanse the data (remove any unwanted characters, emojis etc...)
    for entry in Raw_data:
        entry[0] = entry[0].replace('\\', ' ') # Remove backslashes and replace with a space
        entry[0] = entry[0].replace(',', '') # Remove commas
    # Remove any emojis from the data
        entry[1] = re.sub(r'[^\x00-\x7F]+', '', entry[1]) # Remove non-ASCII characters
        entry[2] = re.sub(r'[^\x00-\x7F]+', '', entry[2]) # Remove non-ASCII characters

    print(Raw_data)

    print("\nData Cleansed Successfully...")

    # Create a Dictionary Containing the Dates and Locations of the Events
    event_days = {
        "Cornwall" : "17/09/2025",
        "Portsmouth" : "19/09/2025",
        "Wellingborough" : "23/09/2025",
        "Walsall" : "25/09/2025",
        "Nottingham" : "26/09/2025",
        "Stoke On Trent" : "29/09/2025",
        "Manchester" : "30/09/2025",
        "Hull" : "02/10/2025",
        "Leeds" : "03/10/2025",
        "Newcastle" : "07/10/2025",
        "Blackpool" : "09/10/2025",
        "Gloucester" : "10/10/2025",
    }

    # Using the Timestamp collumn, replace the the timestamp with the location of the event for each entry
    for entry in Raw_data:
        for location, date in event_days.items():
            if date in entry[0]:
                entry[0] = location
                break
        else:
            entry.append("Unknown Location")
    
    # ----- ----- ----- ----- ----- -----
    # ------ End of Data Cleansing ------


    # Now begin the analysis of the data 
    # To start lets count the reponces form each location
    location_count = {}
    for entry in Raw_data:
        location = entry[0]
        if location in location_count:
            location_count[location] += 1
        else:
            location_count[location] = 1
    
    print("\nLocation Count:")
    print(location_count)

    # Now run through the data and count the most common words that people struggle to spell
    word_count = {}

    for entry in Raw_data:
        words = entry[1].split() + entry[2].split() # Split the words by spaces
        for word in words:
            word = word.lower() # Convert to lowercase for uniformity
            word = re.sub(r'[^\w\s]', '', word) # Remove punctuation
            if word: # Ensure the word is not empty
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    # Sort the word count dictionary by frequency
    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

    # Now run through the data and count the most common words per location
    location_word_count = {}
    for entry in Raw_data:
        location = entry[0]
        words = entry[1].split() + entry[2].split() # Split the words by spaces
        if location not in location_word_count:
            location_word_count[location] = {}
        for word in words:
            word = word.lower() # Convert to lowercase for uniformity
            word = re.sub(r'[^\w\s]', '', word) # Remove punctuation
            if word: # Ensure the word is not empty
                if word in location_word_count[location]:
                    location_word_count[location][word] += 1
                else:
                    location_word_count[location][word] = 1

    build_report(location_count, sorted_word_count, location_word_count, word_count)


def main():
    file_name = input("Enter the filename of the CSV file: ")

    file_name += ".csv" if not file_name.endswith(".csv") else ""

    print(f"Loading data from {file_name}...")

    file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

    # Load the data
    try:
        data = pd.read_csv(file_path)
    
    # Handle potential errors
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return
    
    print("Data loaded successfully...")

    print("\n", data.head())  # Display the first few rows of the dataframe for verification

    # Pass the data to the analysis function
    analyze_data(data)

if __name__ == "__main__":
    main()