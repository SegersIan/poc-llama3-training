import os

def process_folder(source_folder_path, target_folder_path):
    # Print the full path of the folder
    full_path = os.path.abspath(source_folder_path)
    print(f"Full path of the folder: {full_path}")

    # List all files in the folder
    files = os.listdir(source_folder_path)
    print("Files in the folder:")
    for file in files:
        print(file)

    # Create/overwrite the output text file
    full_target_path = os.path.abspath(target_folder_path)
    output_file_path = os.path.join(full_target_path, 'combined_markdown_content.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate through files and write content of markdown files to output file
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(source_folder_path, file)
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                    output_file.write(content + '\n')

    print(f"Combined markdown content written to: {output_file_path}")

# Example usage
source_folder_path = '../learning-data'
target_folder_path = '../temp'
process_folder(source_folder_path, target_folder_path)
