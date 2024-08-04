import os
import hashlib
import json

def get_file_hash(file_path, hash_algo='md5'):
    """Calculate hash of a file."""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def check_file_duplicates(directory, hash_algo='md5'):
    """Check for duplicate files based on hash and return a structured list."""
    file_hashes = {}
    duplicates = {}
    non_duplicates = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path, hash_algo)
            if file_hash in file_hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [file_hashes[file_hash]]
                duplicates[file_hash].append(file_path)
            else:
                file_hashes[file_hash] = file_path
    
    # Prepare the structured list
    result = []
    if duplicates:
        duplicate_groups = [{'Duplicate': files} for files in duplicates.values()]
        result.extend(duplicate_groups)
    
    # Add non-duplicate files
    non_duplicate_files = [file_path for file_hash, file_path in file_hashes.items() if file_hash not in duplicates]
    if non_duplicate_files:
        result.append({'non': non_duplicate_files})

    return result

def export_to_file(data, export_directory='export', export_file='export.txt'):
    """Export the result data to a text file."""
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    export_path = os.path.join(export_directory, export_file)
    
    with open(export_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data exported to {export_path}")

# Path to your directory
directory_path = r'Import'

# Get the result
result = check_file_duplicates(directory_path)

# Export the result to a file
export_to_file(result)
