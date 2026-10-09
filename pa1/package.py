"""Package the assignment into pa1.zip for submission.

The archive contains the src/ directory and CMakeLists.txt,
with build artifacts and editor files excluded.
"""

import os
import zipfile

OUTPUT_ZIP = "pa1.zip"

# Files and directories that should never be packaged.
EXCLUDED_DIRS = {"__pycache__", ".antlr", ".vscode", ".idea", "build"}
EXCLUDED_EXT = {".o", ".pyc"}


def should_include(filename):
    return os.path.splitext(filename)[1] not in EXCLUDED_EXT


def zip_directory(zipf, directory):
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if should_include(file):
                file_path = os.path.join(root, file)
                zipf.write(file_path)  # keeps the relative path inside the archive


def main():
    # Sanity check: the script must run from the project root.
    if not (os.path.isdir("src") and os.path.isfile("CMakeLists.txt")):
        print("Error: missing src/ directory or CMakeLists.txt")
        print("Please run this script from the project root.")
        return

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        zip_directory(zipf, "src")
        zip_directory(zipf, "grammar")
        zipf.write("CMakeLists.txt")

    print(f"Archive created: {OUTPUT_ZIP}. Please submit this file to Gradescope.")


if __name__ == "__main__":
    main()
