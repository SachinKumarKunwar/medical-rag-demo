import os

# Folders / files to scan
ROOT_DIR = "."  # current directory

# Replacements to make
REPLACEMENTS = {
    "": "",
    "": ""
}

# File extensions to update
EXTENSIONS = [".py"]

def fix_imports():
    for foldername, subfolders, filenames in os.walk(ROOT_DIR):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in EXTENSIONS):
                filepath = os.path.join(foldername, filename)

                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                new_content = content
                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)

                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(new_content)
                    print(f"Updated imports in: {filepath}")

if __name__ == "__main__":
    fix_imports()
    print("✅ Import paths updated successfully!")
