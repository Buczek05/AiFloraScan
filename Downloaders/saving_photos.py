import requests, os

PHOTO_EXTENSION = "jpg"
FILE_NAME_LENGTH = 10


class SavingPhotoFromURLToFolderWithName:
    def __init__(self, url, folder_path, name):
        self.url = url
        self.folder_path = folder_path
        self.name = name

    def save_photo(self):
        self.except_error_if_file_exists()
        self.create_folder_if_not_exists()
        final_file_path = self.get_final_file_path()
        photo = self.download_photo()
        with open(final_file_path, "wb") as file:
            file.write(photo)

    def except_error_if_file_exists(self):
        if self.check_if_file_exists():
            raise FileExistsError("File already exists")

    def check_if_file_exists(self) -> bool:
        return os.path.isfile(self.get_final_file_path())

    def create_folder_if_not_exists(self):
        if not os.path.isdir(self.folder_path):
            os.mkdir(self.folder_path)

    def get_final_file_path(self) -> str:
        return self.folder_path + "/" + self.name + "." + PHOTO_EXTENSION

    def download_photo(self) -> bytes:
        r = requests.get(self.url)
        return r.content


class FolderFilesManagement:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_next_file_name(self) -> str:
        file_number = self.get_next_file_number()
        self.file_name = str(file_number).zfill(FILE_NAME_LENGTH)
        return self.file_name

    def get_next_file_number(self) -> int:
        return len(self.get_files_list()) + 1

    def get_files_list(self) -> list:
        return os.listdir(self.folder_path)
