from os import PathLike, getcwd, path as osPath, makedirs


class CheckExists:

    def __init__(self, root_path: str | PathLike[str] = getcwd()):
        """
        Init
        :param root_path: set a custom root path or use working dictionary
        """
        self.root_path = root_path

    def checkFolderAndCreate(self, path: str | PathLike[str]):
        """
        Check if a folder exists, created it when it not exists
        :param path: The path of the folder
        :return: Returns ture if create it
        """
        path = self.getValidPath(path)  # convert the path to a valid path
        if osPath.isdir(path): return False  # if path exists return
        makedirs(path)  # create the dictionary's
        return True

    def checkFileAndCreate(self, file: str | PathLike[str], content: str = ""):
        """
        Check if a file exists, created it when not exists with specific content
        :param file: the path of the file
        :param content: a string of content witch should contain the file, not required
        :return: Returns ture if create it
        """
        path = self.getValidPath(file)
        print(path)
        if not osPath.isdir(path.rsplit("/", 1)[0]): makedirs(path)  # if path not exists create it
        if osPath.exists(path): return False  # if file exists, return
        with open(path, mode='x') as w:  # open the file like a text file
            if content:  # if content write it in
                w.write(content)  # write
            w.close()  # close ist
        return True

    def getValidPath(self, path: str | PathLike[str]):
        """
        Transform a folder path to a valid usable path
        :param path: folder path, example /output or /config/options
        :return:
        """
        if path.startswith("./"):
            path = path[1:]
        path = path.replace("\\", "/")
        if path.startswith("/"): return self.root_path + path
        return self.root_path + "/" + path
