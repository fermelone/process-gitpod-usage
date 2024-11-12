import pandas as pd
from datetime import datetime
import argparse
import sys
import os

def process_usage_data(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Convert time columns to datetime
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['endTime'] = pd.to_datetime(df['endTime'])
    
    # Calculate duration
    def calculate_duration(row):
        if pd.isna(row['endTime']):
            return 'RUNNING'
        
        duration = row['endTime'] - row['startTime']
        minutes = duration.total_seconds() / 60
        return f"{minutes:.1f}"
    
    # Create output dataframe with required columns
    output_df = pd.DataFrame({
        'Date': df['startTime'].dt.strftime('%Y-%m-%d'),
        'Name': df['userName'],
        'Repo': df['contextURL'],
        'Duration (minutes)': df.apply(calculate_duration, axis=1)
    })
    
    return output_df

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process Gitpod usage data from CSV file')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('-o', '--output', help='Path to the output CSV file (optional)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Process the data
        output_df = process_usage_data(args.input_file)
        
        # Determine output file name
        if args.output:
            output_file = args.output
        else:
            # Generate output filename based on input filename
            input_base = os.path.splitext(args.input_file)[0]
            output_file = f"{input_base}_summary.csv"
        
        # Save to CSV
        output_df.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
        
        # Display first few rows as preview
        print("\nPreview of processed data: (only first 5 rows)")
        print(output_df.head().to_string())
        
    except Exception as e:
        print(f"Error processing file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()