import os
from TexSoup import TexSoup
from extractor import TexExtractor
import json

class DocumentListHandler:
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


    def load_from_files(self, dir, lazy = True):
        paragraphsCacheFilename = "cached_paragraphs.json"
        formulasCacheFilename = "cached_formulas.json"
        text = None
        formulas = None
        if (lazy):
            if os.access(f"{dir}/{paragraphsCacheFilename}", 1):
                with open(f"{dir}/{paragraphsCacheFilename}", "r") as f:
                    text = json.loads(f.read())
            if os.access(f"{dir}/{formulasCacheFilename}", 1):
                with open(f"{dir}/{formulasCacheFilename}", "r") as f:
                    formulas = json.loads(f.read())
            if text and formulas:
                self.paragraphs = text
                self.formulas = formulas
                return
        
        for file_name in os.listdir(dir):
            if file_name.split(".")[-1] == "tex":
                file_path = f"{dir}/{file_name}"
                soup = DocumentListHandler.initSoupFromTexFile(file_path)
                text, formulas = TexExtractor.separateTextAndEquationNodes(soup)
                self.paragraphs.append(TexExtractor.nodeListToString(text))
                self.formulas.append(TexExtractor.nodeListToString(formulas))

        with open(f"{dir}/{paragraphsCacheFilename}", "w") as f:
            f.truncate(0)
            f.write(json.dumps(self.paragraphs))
        with open(f"{dir}/{formulasCacheFilename}", "w") as f:
            f.truncate(0)
            f.write(json.dumps(self.formulas))

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