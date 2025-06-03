import os


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, "r", encoding="UTF-8") as file:
            return file.read()

    def load_qss_files(qss_directory):
        qss_files = []
        for root, dirs, files in os.walk(qss_directory):
            for file in files:
                if file.endswith(".qss"):
                    qss_files.append(os.path.join(root, file))
        qss = ""
        for file in qss_files:
            with open(file, "r", encoding="UTF-8") as f:
                qss += f.read()
        return qss
