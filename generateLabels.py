import requests
import os
import shutil
import time

# Base URL for calls to the BOMIST API. Update to match your environment.
base_url = "http://localhost:3333"

# BOMIST API URLs
barcode_url = base_url + "/barcodes/export"
parts_url = base_url + "/parts"
labels_url = base_url + "/labels"

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

temporary_directory = os.path.join(script_directory, "raw")
final_directory = os.path.join(script_directory, "renamed")

# Ensure directories exist
os.makedirs(temporary_directory, exist_ok=True)
os.makedirs(final_directory, exist_ok=True)

# Helper function to process each part
def process_part(part_details):
    ipn = part_details.get('title', None)
    if not ipn:  # Check if IPN is missing or invalid
        print("Invalid IPN, skipping part:", part_details)
        return

    print("Processing IPN:", ipn)  # Debug statement

    payload = {
        "action": "save_to_png",
        "format": "qrcode",
        "labelType": "detailed",
        "data": [part_details],
        "outputPath": temporary_directory
    }
    #print("payload: ", payload)

    # Send the request
    response = requests.post(barcode_url, json=payload)
    response.raise_for_status()

    # Check for the new file and rename it
    time.sleep(2)  # Wait a bit for the file to be created
    
    # Find the generated file and rename it
    found = False
    for filename in os.listdir(temporary_directory):
        if "barcode" in filename:
            new_filename = f"{ipn}.png"
            src_path = os.path.join(temporary_directory, filename)
            
            # Determine the type folder based on the first 3 digits of the title
            type_folder = ipn[:3]
            type_path = os.path.join(final_directory, type_folder)
            os.makedirs(type_path, exist_ok=True)  # Create the type folder if it does not exist
            
            dst_path = os.path.join(type_path, new_filename)
            shutil.move(src_path, dst_path)
            print(f"File renamed and moved to: {dst_path}")
            found = True
            break
    
    if not found:
        print("No barcode file found for IPN:", ipn)

# Fetch the latest parts data from BOMIST
def fetch_latest_parts():
    response = requests.get(parts_url)
    response.raise_for_status()
    return response.json()

# Fetch the latest labels data from BOMIST
def fetch_latest_labels():
    response = requests.get(labels_url)
    response.raise_for_status()
    return response.json()

# Get a set of existing labels from the renamed directory
def get_existing_labels(directory):
    existing_labels = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                existing_labels.add(file.replace('.png', ''))
    return existing_labels

# Helper function to find a label by ID
def find_label_by_id(label_id, latest_labels):
    for label in latest_labels:
        if label['id'] == label_id:
            return label['label']
    return "Unknown Label"

# Main function to process parts
def main():
    latest_parts = fetch_latest_parts()
    latest_labels = fetch_latest_labels()
    existing_labels = get_existing_labels(final_directory)

    for part in latest_parts:
        part_info = part['part']
        title = part_info.get('ipn', '')
        if title and title not in existing_labels:
            # This is a new part or a part without a printed label
            print(f"Processing new or updated part: {title}")
            part_details = {
                "barcode": part_info['id'],
                "title": title,
                "subtitle": find_label_by_id(part_info['label'], latest_labels),
                "meta": part_info.get('mpn', ''),
                "description": part_info.get('description', '')
            }
            process_part(part_details)
            # Here would be the logic to generate the label (like previously discussed)
            # For now, we just simulate this by printing
            #print(f"Label would be generated for: {title}")




if __name__ == "__main__":
    main()
