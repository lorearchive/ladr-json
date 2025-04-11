import json
import os
from collections import defaultdict
import argparse
import ijson  # For memory-efficient JSON parsing

def create_output_directory(directory):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def process_large_json(input_file, output_dir):
    """
    Process a large JSON file and group objects by GroupId.
    Uses streaming parser to handle large files efficiently.
    """
    create_output_directory(output_dir)
    
    # Dictionary to store objects grouped by GroupId
    grouped_data = defaultdict(list)
    
    # Parse the large JSON file using ijson for streaming
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        # Get DataList items one by one to avoid loading the entire file into memory
        data_items = ijson.items(f, 'DataList.item')
        
        # Process each item
        count = 0
        for item in data_items:
            if 'GroupId' in item:
                group_id = item['GroupId']
                grouped_data[group_id].append(item)
                count += 1
                if count % 100000 == 0:
                    print(f"Processed {count} items...")
    
    print(f"Finished processing {count} items.")
    print(f"Found {len(grouped_data)} unique GroupIds.")
    
    # Write each group to a separate file
    for group_id, items in grouped_data.items():
        output_file = os.path.join(output_dir, f"{group_id}.json")
        
        # Create output in the required format
        output_data = {
            "DataList": items
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Use indent to preserve formatting
            json.dump(output_data, f, indent=4)
        
        print(f"Created file: {output_file} with {len(items)} items")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Group JSON objects by GroupId')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('--output-dir', default='output', help='Directory to store output files (default: "output")')
    
    args = parser.parse_args()
    
    process_large_json(args.input_file, args.output_dir)
