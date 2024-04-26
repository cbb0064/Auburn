import sys
import hashlib
from pathlib import Path

# Constants for magic numbers and common values
HEADER_OFFSETS = {
    "AVI": 4,
    "BMP": 2,
}

# Define dictionary structures for file types and footers
FSigs = {
    "MPG": b"\x00\x00\x01\xB3\x14",
    "PDF": b"\x25\x50\x44\x46",
    "DOCX": b"\x50\x4B\x03\x04\x14\x00\x06\x00",
    "AVI": b"\x52\x49\x46\x46",
    "PNG": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
    "JPG": b"\xFF\xD8\xFF\xE0",
    "GIF": b"\x47\x49\x46\x38\x39\x61",
    "BMP": b"\x42\x4D\x76\x30\x01",
}

FOOTERS = {
    "MPG": b"\x00\x00\x01\xB7",
    "PDF": b"\x25\x25\x45\x4F\x46",
    "DOCX": b"\x50\x4B\x05\x06",
    "PNG": b"\x49\x45\x4E\x44\xAE\x42\x60\x82",
    "JPG": b"\xFF\xD9",
    "GIF": b"\x00\x00\x3B",
}

def calculate_file_hash(file_data):
    """Calculate SHA256 hash of given file data."""
    return hashlib.sha256(file_data).hexdigest()

def find_footer(data, footer, start_offset):
    """Find the footer of the file from start_offset."""
    footer_index = data.find(footer, start_offset)
    return footer_index + len(footer) if footer_index != -1 else -1

def recover_file(disk_data, file_info, recovery_dir):
    """Recover the file and write it to the recovery directory."""
    file_name, file_start, file_end = file_info
    file_data = disk_data[file_start:file_end]
    recovered_file_path = recovery_dir / file_name
    with open(recovered_file_path, 'wb') as recovered_file:
        recovered_file.write(file_data)

def main(disk_file_path):
    try:
        # Read disk file
        with open(disk_file_path, 'rb') as file:
            disk_data = file.read()

        found_files = {}
        recovered_files_dir = Path("RecoveredFiles")
        recovered_files_dir.mkdir(parents=True, exist_ok=True)

        # Main file processing logic
        for f, header in FSigs.items():
            offset = 0
            while (offset := disk_data.find(header, offset)) != -1:
                # Find end of file based on type
                file_end = find_footer(disk_data, FOOTERS.get(f, b""), offset + len(header))
                
                # Specific handling for file types with complex endings
                if f == "AVI":
                    # AVI size is bytes 4-7
                    file_size = int.from_bytes(disk_data[offset + HEADER_OFFSETS[f]: offset + HEADER_OFFSETS[f] + 4], byteorder='little', signed=False)
                    file_end = offset + file_size
                elif f == "BMP":
                    # BMP size is bytes 2-5
                    file_size = int.from_bytes(disk_data[offset + HEADER_OFFSETS[f]: offset + HEADER_OFFSETS[f] + 4], byteorder='little', signed=False)
                    file_end = offset + file_size
                elif f == "DOCX":
                    # DOCX has an additional 18 bytes after the footer
                    file_end += 18

                if file_end == -1:
                    # No valid end found; likely a false positive, skip to next
                    offset += len(header)
                    continue

                # Construct file information tuple
                file_name = f"file{len(found_files) + 1}.{f.lower()}"
                file_sha256 = calculate_file_hash(disk_data[offset:file_end])
                found_files[file_name] = (file_name, offset, file_end)

                # Recover the file
                recover_file(disk_data, found_files[file_name], recovered_files_dir)
                
                # Move to the next offset
                offset = file_end

        # Print recovered file information
        print(f"The disk image contains {len(found_files)} files\n")
        for file_name, (file_name, file_start, file_end) in found_files.items():
            file_sha256 = calculate_file_hash(disk_data[file_start:file_end])
            print(f"{file_name}, Start Offset: 0x{file_start:X}, End Offset: 0x{file_end:X}\nSHA-256: {file_sha256}\n")
    # Print the recovery directory
        print(f"Recovered files are located in {recovered_files_dir.resolve()}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <disk_image>")
        sys.exit(1)
    main(sys.argv[1])
