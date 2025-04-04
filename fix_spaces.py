import os

def remove_spaces_in_filenames(root_folder):

    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith(".json") or file.endswith(".txt"):
                # Remove spaces from file name
                new_file = file.replace(" ", "")
                if new_file != file:
                    old_path = os.path.join(dirpath, file)
                    new_path = os.path.join(dirpath, new_file)
                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} -> {new_path}")
                    except Exception as e:
                        print(f"Error renaming {old_path}: {e}")

if __name__ == "__main__":
    # Change this to your root folder path
    root_folder = "benchmark_dataset_v2/misaligned_terminalogy_legal_spaces"
    remove_spaces_in_filenames(root_folder)
