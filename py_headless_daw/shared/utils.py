import os


def get_path_relative_to_project_root(relative_path: str) -> str:
    this_dir_path = os.path.dirname(os.path.realpath(__file__))
    return this_dir_path + '/../../' + relative_path


def get_path_relative_to_file(file_name: str, relative_path: str) -> str:
    this_dir_path = os.path.dirname(os.path.realpath(file_name))
    return this_dir_path + '/' + relative_path
