import os

def get_file_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../" + file_name)

def get_points_by_position(position):
    if position == r"\N":
        return 0

    return 21 - int(position)