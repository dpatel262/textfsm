import os
import pandas as pd
import textfsm

# Directory containing the files
directory = "/home/devapate/repos/textfsm/"   # Replace with your directory path

# List of interfaces to extract
interfaces_to_extract = [
    "ens11np0", "ens12np0", "ens21np0", "ens22np0", 
    "ens31np0", "ens32np0", "ens41np0", "ens42np0"
]

# Path to the TextFSM template
template_path = "/home/devapate/repos/textfsm/textfsm_template_ip_addr_show.txt"

# Function to process a single file with TextFSM
def process_file(file_path, template_path):
    with open(template_path, 'r') as template_file:
        fsm = textfsm.TextFSM(template_file)
    with open(file_path, 'r') as file:
        content = file.read()
        parsed_data = fsm.ParseText(content)
        return [dict(zip(fsm.header, row)) for row in parsed_data]

# Process all files in the directory
all_extracted_info = []
for file_name in os.listdir(directory):
    if file_name.endswith("_ip_info.txt"):  # Filter specific files
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                parsed_info = process_file(file_path, template_path)
                for record in parsed_info:
                    if record['INTERFACE'] in interfaces_to_extract:
                        record['FILENAME'] = file_name
                        all_extracted_info.append(record)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Create a DataFrame for the extracted data
df = pd.DataFrame(all_extracted_info)

# Display the table and save to CSV
if not df.empty:
    pd.set_option('display.max_columns', None)
    print("Extracted Data:")
    print(df.to_string(index=False))
    output_csv = "interface_info_with_state.csv"
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")
else:
    print("No data extracted from the files.")

