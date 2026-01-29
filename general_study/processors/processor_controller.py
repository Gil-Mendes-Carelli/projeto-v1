from pathlib import Path
from dataclasses import dataclass

import helper_functions.helper_functions as hf
import processors.folder_processor as fop
import processors.file_processor as fp

@dataclass(slots=True)
class ProcessorControlConfig:
    sorted_folder_path_list: Path
    file_processor_config: fp.ProcessFilesConfig


def processor_controller(config: ProcessorControlConfig) -> None:
    file_path_list: list[Path] = []
    sorted_file_path_list: list[Path] = []    
    for folder_path in config.sorted_folder_path_list:
        ignored_file_text: str = config.file_processor_config.system_role 
        system_role: str = config.file_processor_config.system_role
        config.file_processor_config.system_role = ""
        file_path_list = fop.get_all_file_paths_in_folder(folder_path=folder_path)        
        sorted_file_path_list = fop.sort_path_list_alphabetically(file_path_list)
        ignored_file_text = hf.get_ignored_file_text(file_path_list=sorted_file_path_list)
        config.file_processor_config.system_role += f"{system_role}"
        config.file_processor_config.system_role += f"\n{ignored_file_text}"
        sorted_file_path_list: list[Path] = hf.remove_ignored_file_from_path_list(
            file_path_list=sorted_file_path_list
        )
        for path in sorted_file_path_list:
            # print(path.name)
            config.file_processor_config.file_path=path
            hf.save_response_to_file(
                response=fp.process_file(config=config.file_processor_config), source_file_name=path.name
            )   


def main() -> None:
    pass


if __name__ == "__main__":
    main()
