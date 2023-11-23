from extractor import TexExtractor
from document_list_handler import DocumentListHandler
from antiplagarism_tools import AntiPlagarism
import os
from TexSoup import TexSoup

TEX_FOLDER_NAME = "tex_file_base"
# Procedura przedstawia schemat dzialania aplikacji dla pojedynczego pliku z files_to_test
if __name__ == "__main__":
    testedDocument = DocumentListHandler.initSoupFromTexFile(os.path.join(os.getcwd(), "files_to_test", "test.tex"))

    testedParagraphs, testedEquations = TexExtractor.separateTextAndEquationNodes(testedDocument)
    testedFullTextContent = TexExtractor.nodeListToString(testedParagraphs)
    testedFullEquationsContent = TexExtractor.nodeListToString(testedParagraphs)

    document_list_handler = DocumentListHandler()
    document_list_handler.load_from_files(os.path.join(os.getcwd(), TEX_FOLDER_NAME), lazy=True)

    #hash tests
    for document in document_list_handler.text_base:
        # porownaj po full content hash
        paragraphs, equations = TexExtractor.separateTextAndEquationNodes(document)
        fullTextContent = TexExtractor.nodeListToString(paragraphs)
        fullEquationContent = TexExtractor.nodeListToString(equations)
        matchedParagraphs = AntiPlagarism.compare_hashes(fullTextContent, testedFullTextContent)
        matchedEquations = AntiPlagarism.compare_hashes(fullEquationContent, testedFullEquationsContent)

        if matchedParagraphs:
            print(f"matched sections from {document.name}: {fullTextContent}")

        if matchedEquations:
            print(f"matched sections from {document.name}: {fullEquationContent}")

        for baseParagraph in paragraphs:
            for testedParagraph in testedParagraphs:
                matchedParagraph = AntiPlagarism.compare_hashes(baseParagraph, testedParagraph)
                if matchedParagraph:
                    print(f"matched section from {document.name}: {testedParagraph}")
        
        for baseEquation in paragraphs:
            for testedEquation in testedEquations:
                matchedEquations = AntiPlagarism.compare_hashes(baseEquation, testedEquation)
                if matchedParagraph:
                    print(f"matched section from {document.name}: {testedEquation}")

    document_list_handler.text_base
