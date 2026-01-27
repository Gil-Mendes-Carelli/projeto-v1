from pathlib import Path

def get_all_sub_folders_paths(folder_path: Path) -> list[Path]:
    return [path for path in folder_path.iterdir() if path.is_dir()]

def get_all_file_paths_in_folder(folder_path: Path) -> list[Path]:
    return [path for path in folder_path.iterdir() if path.is_file()]

def sort_path_list_alphabetically(path_list: list[Path]) -> list[Path]:
    return sorted(path_list, key=lambda path: path.name.lower())



def main() -> None:
    pass

if __name__ == "__main__":
    main()