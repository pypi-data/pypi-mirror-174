class DatabricksLibrary:
    def __init__(self, libraries: dict, install_all: bool = False):
        self.install_all: bool = install_all
        self.libraries = libraries
