import pandas as pd
import os # For file path operations

def analyze_data(data):
    # Create an empty list to store data
    Raw_data = []
    # first take data apaet into a list 
    for row in data['Where are you attending the course?', 'What are two words you struggle to spell? (Don\'t worry about the spelling.)', 'What are two words your class struggles to spell?']:
        Raw_data.append([row])
    
    # Second, cleanse the data (remove any unwanted characters etc...)
    for entry in Raw_data:
        entry[0] = entry[0].replace('\\', ' ') # Remove backslashes and replace with a space
        entry[0] = entry[0].replace(',', '') # Remove commas

    print(Raw_data.head()) # Display the first few rows of the cleansed data for verification


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
    
    print("Data loaded successfully.")
    print(data.head())  # Display the first few rows of the dataframe for verification

    # Pass the data to the analysis function
    analyze_data(data)

if __name__ == "__main__":
    main()