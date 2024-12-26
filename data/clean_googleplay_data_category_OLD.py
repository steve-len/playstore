import pandas as pd
import os

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE_PATH = os.path.join(BASE_DIR, 'raw', 'googleplaystore.csv')
CLEAN_FILE_PATH = os.path.join(BASE_DIR, 'cleaned', 'googleplaystore_cleaned_category.csv')


def clean_googleplay_data(input_path, output_path):
    """
    Clean the Google Play Store dataset by removing entries with category '1.9'
    """
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(input_path)
    print("Dataset loaded successfully.")

    # Remove rows with category '1.9'
    print("Removing category '1.9' entries...")
    df = df[df['Category'] != '1.9']

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save cleaned dataset
    print("Saving cleaned data...")
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    # Run the cleaning process
    print("Starting the cleaning process...")
    clean_googleplay_data(RAW_FILE_PATH, CLEAN_FILE_PATH)
    print("Process completed successfully.")