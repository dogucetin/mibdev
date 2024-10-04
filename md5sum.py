import hashlib
import argparse

def calculate_md5(file_name):
    # Initialize MD5 hasher
    md5_hash = hashlib.md5()
    
    try:
        # Open the file in binary mode
        with open(file_name, "rb") as file:
            # Read the file in chunks
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
        
        # Print the MD5 checksum
        print(f"MD5 checksum of {file_name}: {md5_hash.hexdigest()}")
    
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Calculate MD5 checksum of a file.")
    parser.add_argument("file_name", help="Path to the file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the calculate_md5 function with the file_name argument
    calculate_md5(args.file_name)

if __name__ == "__main__":
    main()
