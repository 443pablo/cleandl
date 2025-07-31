def move_file(source, destination):
    import os
    import shutil

    if not os.path.exists(destination):
        os.makedirs(destination)
    shutil.move(source, os.path.join(destination, os.path.basename(source)))

def get_file_extension(file_name):
    return file_name.split('.')[-1] if '.' in file_name else None

def is_supported_file_type(file_name, supported_extensions):
    return get_file_extension(file_name) in supported_extensions

def list_files_in_directory(directory):
    import os
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]