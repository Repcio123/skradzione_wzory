import os
from TexSoup import TexSoup
from extractor import TexExtractor

class DocumentListHandler:
    test_cases: list[TexSoup] = []
    paragraphs: list[str] = []
    formulas: list[str] = []
    
    @staticmethod
    def initSoupFromTexFile(filename: str):
        with open(filename, "r") as f:
            try:
                file_contents = f.read()
                return TexSoup(file_contents)
            except:
                raise Exception(f"failed to parse latex")

    def load_from_files(self, dir):
        for file_name in os.listdir(dir):
            soup = DocumentListHandler.initSoupFromTexFile(f"{dir}/{file_name}")
            text, equations = TexExtractor.separateTextAndEquationNodes(soup)
            self.paragraphs.append(TexExtractor.nodeListToString(text))
            self.formulas.append(TexExtractor.nodeListToString(equations))

TEX_FOLDER_NAME = "tex_file_base"

if __name__ == "__main__":
    file_handler = DocumentListHandler()
    file_handler.load_from_files(f"{os.getcwd()}/{TEX_FOLDER_NAME}")

    print(file_handler.paragraphs)

#TODO:
#1. basic file handler - to text (DONE)
#2. getting paragraphs/chunks of text and formulas into lists (DONE)
#3. using imported method for checking plagarism (DONE)
#4. (BONUS) generate html report