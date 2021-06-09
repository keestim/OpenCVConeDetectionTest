import os

class FileUtils:
    def __init__(self, folder_path, valid_extensions = [".png", ".jpg", ".jpeg"]):
        self.ffolder_path = folder_path
        self.fvalid_extensions = valid_extensions

        self.favaliable_files = self.__buildFileQueue(self.ffolder_path)

        self.findex = 0

    def __buildFileQueue(self, folder_path):
        temp_valid_files = []

        for filename in os.listdir(folder_path):
            if self.__isFileValid(filename): 
                temp_valid_files.append(filename)

        temp_valid_files.sort()
        return temp_valid_files

    def __isFileValid(self, file_str):
        for extension in self.fvalid_extensions:
            if (file_str.endswith(extension)):
                return True
        
        return False

    def getFolderPath(self):
        return self.ffolder_path

    def getCurrentFile(self):
        return (self.ffolder_path + "/" + self.favaliable_files[self.findex])

    def getNextFile(self):
        if (self.findex <= len(self.favaliable_files) - 2):
            self.findex += 1
        else:
            self.findex = 0

        return self.getCurrentFile()

    def getPrevFile(self):
        if (self.findex > 0):
            self.findex -= 1
        else:
            self.findex = len(self.favaliable_files) - 1

        return self.getCurrentFile()

    #intergrate this, so it shows if xml has been produced
    def getXMLFileExists(self):
        return False

    #also print file name