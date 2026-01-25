##########################################################
########## Script for general utility functions ##########
##########################################################

def remove_blank_lines_from_txt_file(file_path: str) -> None:
    """
    Clean blank lines from a text file and save the result.
    
    Args:
        file_path: path to the text file to be cleaned.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()    
    
    non_blank_lines = [line for line in lines if line.strip()]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(non_blank_lines)

def main() -> None:
    pass

if __name__ == "__main__":
    main()