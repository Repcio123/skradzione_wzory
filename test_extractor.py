from extractor import TexExtractor
from document_list_handler import DocumentListHandler
import os


DIRECTORY = "files_to_test"
FILES = os.listdir(DIRECTORY)
full_paths = [os.path.join(DIRECTORY, file) for file in FILES]
if __name__ == "__main__":
    sampleText = DocumentListHandler.initSoupFromTexFile(
        os.getcwd() + '/files_to_test/test.tex'
    )
    paragraphNodes, equationNodes = TexExtractor.separateTextAndEquationNodes(
        sampleText)
    documentText = TexExtractor.nodeListToString(paragraphNodes)
    documentEquations = TexExtractor.nodeListToString(equationNodes)
    JUNK = [",", " ", "."]
    
    

