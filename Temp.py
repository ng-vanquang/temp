import os
import sys
from tqdm import tqdm


def load_original_files(file_a_path):
    """
    Trả về dict:
    {
        filename: size
    }
    """
    original_files = {}

    with open(file_a_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Reading File A"):
            path = line.strip()
            if not path:
                continue

            if not os.path.exists(path):
                print(f"WARNING: File not found: {path}")
                continue

            filename = os.path.basename(path)
            size = os.path.getsize(path)

            original_files[filename] = size

    return original_files


def verify_files(file_a_path, folder_b_path):
    print("Loading original file list...")
    original_files = load_original_files(file_a_path)

    missing_files = []
    size_mismatch = []
    verified = 0

    print("Scanning Folder B...")

    # Build dict for moved files
    moved_files = {}

    with os.scandir(folder_b_path) as it:
        for entry in tqdm(it, desc="Scanning Folder B"):
            if entry.is_file():
                stat = entry.stat()
                moved_files[entry.name] = stat.st_size

    print("Comparing...")

    for filename, original_size in tqdm(original_files.items(), desc="Verifying"):
        if filename not in moved_files:
            missing_files.append(filename)
        else:
            moved_size = moved_files[filename]
            if moved_size != original_size:
                size_mismatch.append(
                    (filename, original_size, moved_size)
                )
            else:
                verified += 1

    print("\n===== RESULT =====")
    print(f"Total in File A     : {len(original_files)}")
    print(f"Total in Folder B   : {len(moved_files)}")
    print(f"Verified OK         : {verified}")
    print(f"Missing files       : {len(missing_files)}")
    print(f"Size mismatch       : {len(size_mismatch)}")

    if missing_files:
        print("\nExample missing files:")
        for f in missing_files[:10]:
            print(f)

    if size_mismatch:
        print("\nExample size mismatch:")
        for f in size_mismatch[:5]:
            print(f"{f[0]} | original={f[1]} | moved={f[2]}")

    return missing_files, size_mismatch


if __name__ == "__main__":
    file_a = sys.argv[1]
    folder_b = sys.argv[2]

    verify_files(file_a, folder_b)
