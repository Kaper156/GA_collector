import os


def up_to_project_folder():
    path = os.path.abspath(os.getcwd())
    while 'src' in path:
        os.chdir('../..')
        path = os.path.abspath(os.getcwd())
        print(f'Change working dir to: {path}')
    if 'src' not in os.listdir(path):
        raise Exception(f"Incorrect folder! ({path})")
    return path


def get_folder_path_from_name(folder_name):
    if not folder_name:
        return None
    # return if this folder exist
    if os.path.exists(folder_name):
        return os.path.abspath(folder_name)
    # create new folder in GA_Selenium (project-folder)/out
    cur_dir = os.path.abspath(os.path.curdir)
    while not os.path.exists(os.path.join(cur_dir, 'out')):
        cur_dir = os.path.join(cur_dir, '..')
        # print(f"Change dir to: \n{cur_dir}\n{os.path.abspath(cur_dir)}\n\n")  # Debug
    out_dir = os.path.abspath(cur_dir)  # Replace dots with real folder path
    folder_name = os.path.split(folder_name)[-1]  # Get folder name (folder-name may contain some path)
    return os.path.join(out_dir, 'out', folder_name)
