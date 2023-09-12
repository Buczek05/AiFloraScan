import os
from Downloaders.saving_photos import (
    SavingPhotoFromURLToFolderWithName,
    FolderFilesManagement,
)


def remove_folder_if_exists(folder_path):
    if os.path.isdir(folder_path):
        os.rmdir(folder_path)


def remove_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


class TestsSavingPhotoFromURLToFolderWithName:
    URL = "https://laflora.pl/854-large_default/czerwone-roze.jpg"
    FOLDER_PATH = "Tests/Downloaders/Tests_Downloaders"
    NAME = "00001"
    FINAL_PATH = FOLDER_PATH + "/" + NAME + ".jpg"

    def test_get_final_file_path(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        assert photo.get_final_file_path() == self.FINAL_PATH

    def test_check_if_file_exists_false(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        assert photo.check_if_file_exists() == False

    def test_create_folder_if_not_exists(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        photo.create_folder_if_not_exists()
        assert os.path.isdir(self.FOLDER_PATH) == True

    def test_saving_photo(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        photo.save_photo()
        assert os.path.isfile(self.FINAL_PATH) == True
        remove_file_if_exists(self.FINAL_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_check_if_file_exists_true(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        photo.save_photo()
        assert photo.check_if_file_exists() == True
        remove_file_if_exists(self.FINAL_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_except_error_if_file_exists(self):
        photo = SavingPhotoFromURLToFolderWithName(
            self.URL, self.FOLDER_PATH, self.NAME
        )
        photo.save_photo()
        try:
            photo.except_error_if_file_exists()
            assert False
        except FileExistsError:
            assert True
        remove_file_if_exists(self.FINAL_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)


class TestsFolderFilesManagement:
    FOLDER_PATH = "Tests/Downloaders/Tests_Downloaders"
    FILE_NAME = "0000000001"
    FILE_PATH = FOLDER_PATH + "/" + FILE_NAME + ".jpg"

    def test_get_files_list_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_files_list() == []
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_get_files_list_not_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        if not os.path.isfile(self.FILE_PATH):
            open(self.FILE_PATH, "w").close()
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_files_list() == [self.FILE_NAME + ".jpg"]
        remove_file_if_exists(self.FILE_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_get_next_file_number_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_next_file_number() == 1
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_get_next_file_number_not_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        if not os.path.isfile(self.FILE_PATH):
            open(self.FILE_PATH, "w").close()
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_next_file_number() == 2
        remove_file_if_exists(self.FILE_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_get_next_file_name_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_next_file_name() == self.FILE_NAME
        remove_folder_if_exists(self.FOLDER_PATH)

    def test_get_next_file_name_not_empty(self):
        if not os.path.isdir(self.FOLDER_PATH):
            os.mkdir(self.FOLDER_PATH)
        if not os.path.isfile(self.FILE_PATH):
            open(self.FILE_PATH, "w").close()
        folder = FolderFilesManagement(self.FOLDER_PATH)
        assert folder.get_next_file_name() == "0000000002"
        remove_file_if_exists(self.FILE_PATH)
        remove_folder_if_exists(self.FOLDER_PATH)
