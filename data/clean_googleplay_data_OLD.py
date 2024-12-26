import pandas as pd
import os

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current directory: data/
RAW_FILE_PATH = os.path.join(BASE_DIR, 'raw', 'googleplaystore.csv')
CLEAN_FILE_PATH = os.path.join(BASE_DIR, 'cleaned', 'googleplaystore_cleaned_OLD.csv')


def clean_googleplay_data(input_path, output_path):
    """
    Clean the Google Play Store dataset and save the cleaned version.
    Removes entries with category '1.9'.
    """
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(input_path)
    print("Dataset loaded successfully.")

    # Data Cleaning
    print("Cleaning data...")
    # Remove rows with missing 'Rating'
    df = df.dropna(subset=['Rating'])

    # Remove entries where category is '1.9'
    print("Removing category '1.9' entries...")
    df = df[df['Category'] != '1.9']

    # Fill missing 'Type' values with 'Free' (explicitly updating column)
    df['Type'] = df['Type'].fillna('Free')

    # Convert 'Reviews' to numeric, setting invalid ones to NaN
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    # Clean 'Installs' column: remove '+' and ',' then convert to float
    df['Installs'] = df['Installs'].str.replace('+', '', regex=False) \
        .str.replace(',', '', regex=False) \
        .astype(float, errors='ignore')

    # Save cleaned dataset
    print("Saving cleaned data...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    # Run the cleaning process
    print("Starting the cleaning process...")
    clean_googleplay_data(RAW_FILE_PATH, CLEAN_FILE_PATH)
    print("Process completed successfully.")