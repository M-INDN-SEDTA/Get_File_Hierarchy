import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        # If already running as admin, execute the main function
        main()
    else:
        # If not running as admin, relaunch the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def generate_hierarchy(directory, root_name, indent=""):
    """
    Generate directory hierarchy starting from the given directory.
    """
    hierarchy = ""
    for root, dirs, files in os.walk(directory):
        current_level = root.replace(directory, "").count(os.sep)
        if root_name == os.path.basename(root):
            hierarchy += f"{root_name}\n"
        else:
            root_display = os.path.basename(root)
            hierarchy += f"{indent}{'│   ' * (current_level - 1)}{'├── ' if current_level > 0 else ''}{root_display}\n"
        for f in files:
            hierarchy += f"{indent}{'│   ' * current_level}{'├── '}{f}\n"
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
    if is_admin():
        main()
    else:
        run_as_admin()
