import pandas as pd
import re # For regular expressions
import os # For file path operations

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

    print(Raw_data)


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