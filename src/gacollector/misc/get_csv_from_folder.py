import os


def gen_csv_files_from_folder(folder):
    '''
    generator of valid .csv files from folder
    :param folder: folder contain .csv files
    :return: file_name, file_path
    '''
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            yield file_name, file_path
