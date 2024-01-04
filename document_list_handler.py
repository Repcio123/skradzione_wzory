import os
from TexSoup import TexSoup
from extractor import TexExtractor
import json



class DocumentListHandler:
    text_base: list[TexSoup] = []

    @staticmethod
    def initSoupFromTexFile(filepath: str):
        with open(filepath, "r") as f:
            try:
                file_contents = f.read()
                return TexSoup(file_contents)
            except:
                raise Exception(f"failed to parse latex")

    @staticmethod
    def init_tex_document_base(dir, lazy = True):
        result = []
        for file_name in os.listdir(os.path.join(dir, "tex")):
            if file_name.split(".")[-1] == "tex":
                file_path = os.path.join(dir, "tex", file_name)
                result.append(DocumentListHandler.initSoupFromTexFile(file_path))
        return result

TEX_FOLDER_NAME = "tex_file_base"

if __name__ == "__main__":
    file_handler = DocumentListHandler()
    file_handler.load_from_files(f"{os.getcwd()}/{TEX_FOLDER_NAME}", lazy=True)

    print(len(file_handler.formulas))

#TODO:
#1. basic file handler - to text (DONE)
#2. getting paragraphs/chunks of text and formulas into lists (DONE)
#3. using imported method for checking plagarism (DONE)
#4. (BONUS) generate html report