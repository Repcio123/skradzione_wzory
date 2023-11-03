
from TexSoup import TexSoup
from difflib import SequenceMatcher
import os

class TexExtractor:
    MATH_SYMBOLS = ["$", "equation"]
    OTHER_SYMBOLS = ["maketitle", "section"]

    @staticmethod   
    def separateTextAndEquationNodes(soup: TexSoup):
        document_body = soup.document
        symbols = [x for x in document_body.children if x.name in TexExtractor.MATH_SYMBOLS]
        for index, symbol in enumerate(symbols):
            temp = symbol.copy()
            symbol.replace_with("") 
            symbols[index] = temp.contents
        return document_body.contents, symbols

    @staticmethod
    def nodeListToString(nodeList):
        return " ".join(str(x) for x in nodeList)
    

if __name__ == "__main__":
    # Example use case
    from document_handler import DocumentListHandler

    sampleText = DocumentListHandler.initSoupFromTexFile(os.getcwd() + "/tex_file_base/main1.tex")


    paragraphNodes, equationNodes = TexExtractor.separateTextAndEquationNodes(sampleText)
    documentText = TexExtractor.nodeListToString(paragraphNodes)
    documentEquations = TexExtractor.nodeListToString(equationNodes)

    print(paragraphNodes[2])
    JUNK = [",", " ", "."]

    text_similarity_ratio = SequenceMatcher(lambda x: x in JUNK, documentText, documentText).ratio()
    equations_similarity_ratio = SequenceMatcher(lambda x: x in JUNK, documentEquations, documentEquations).ratio()

    assert text_similarity_ratio == 1, "DJDJ"
    assert equations_similarity_ratio == 1, "JDJD"
