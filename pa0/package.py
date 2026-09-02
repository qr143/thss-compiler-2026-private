"""Package the assignment into pa0.zip for submission.

The archive contains only word_counter.cpp at the root level,
as required by GradeScope:

    pa0.zip
    └── word_counter.cpp
"""

import os
import zipfile

OUTPUT_ZIP = "pa0.zip"
SOURCE_FILE = "word_counter.cpp"


def main():
    # Sanity check: the script must run from the project root.
    if not os.path.isfile(SOURCE_FILE):
        print(f"Error: missing {SOURCE_FILE}")
        print("Please run this script from the project root.")
        return

    # Write the file at the archive root, without any directory prefix.
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(SOURCE_FILE, arcname=SOURCE_FILE)

    print(f"Archive created: {OUTPUT_ZIP}. Please submit this file to GradeScope.")


if __name__ == "__main__":
    main()
