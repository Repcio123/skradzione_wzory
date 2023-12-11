from extractor import TexExtractor
from document_list_handler import DocumentListHandler
from antiplagarism_tools import AntiPlagarism
import os
from TexSoup import TexSoup

TEX_FOLDER_NAME = "tex_file_base"
# Procedura przedstawia schemat dzialania aplikacji dla pojedynczego pliku z files_to_test
if __name__ == "__main__":
    # uncomment when testing
    testedDocument = DocumentListHandler.initSoupFromTexFile(os.path.join(os.getcwd(), "files_to_test", "lagrange.tex"))
    results = AntiPlagarism.compare_paragraph_hashes(testedDocument) 
    print(results)
    exit(0)
