import os
from datetime import datetime

def convert_size(size_bytes):
    """
    Convert size in bytes to human-readable format (KB, MB, GB, etc.).
    """
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name)-1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

def get_directory_size(directory):
    """
    Get the total size of all files in a directory and its subdirectories.
    """
    total_size = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(root, f)
            total_size += os.path.getsize(file_path)
    return total_size

def generate_hierarchy(directory, root_name, indent=""):
    """
    Generate directory hierarchy starting from the given directory with file sizes.
    """
    hierarchy = ""
    for root, dirs, files in os.walk(directory):
        current_level = root.replace(directory, "").count(os.sep)
        if root_name == os.path.basename(root):
            hierarchy += f"{root_name} (Total: {convert_size(get_directory_size(root))})\n"
        else:
            root_display = os.path.basename(root)
            folder_size = get_directory_size(root)
            hierarchy += f"{indent}{'│   ' * (current_level - 1)}{'├── ' if current_level > 0 else ''}{root_display} ({convert_size(folder_size)})\n"
        for f in files:
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            hierarchy += f"{indent}{'│   ' * current_level}{'├── '}{f} ({convert_size(file_size)})\n"
    return hierarchy

def main():
    # Get directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Directories in the directory '{script_directory}':")

    # List directories in the script's directory
    directories = next(os.walk(script_directory))[1]

    if not directories:
        print("No directories found in the script's directory.")
        return

    for i, directory in enumerate(directories, start=1):
        print(f"{i}. {directory}")

    # Prompt user to choose a directory
    while True:
        try:
            choice = input("Enter the number corresponding to the directory you want to choose: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(directories):
                    chosen_directory = directories[choice - 1]
                    print(f"You chose '{chosen_directory}'.")
                    chosen_directory_path = os.path.join(script_directory, chosen_directory)
                    hierarchy = generate_hierarchy(chosen_directory_path, chosen_directory)
                    if hierarchy.strip():  # Check if hierarchy is not empty
                        now = datetime.now()
                        timestamp = now.strftime("%d-%m-%Y-%I.%M%p")
                        file_name = f"{chosen_directory}_Hierarchy_{timestamp}.txt"
                        with open(file_name, "w", encoding="utf-8") as file:
                            file.write(f"{hierarchy}")
                        print(f"Directory hierarchy saved in '{file_name}'.")
                    else:
                        print("No directory hierarchy to save.")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
