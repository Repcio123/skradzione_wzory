
from TexSoup import TexSoup
from difflib import SequenceMatcher
import os
import json

class TexExtractor:
    MATH_SYMBOLS = ["$", "equation", "align"]

    @staticmethod
    def getContentsListFromNodeTree(node):
        nodeListOrString = "NodeList" if hasattr(node, 'contents') else "String"
        
        if nodeListOrString == "String":
            return [node]
        
        return sum([TexExtractor.getContentsListFromNodeTree(x) for x in node.contents], [])

    @staticmethod   
    def separateTextAndEquationNodes(soup: TexSoup):
        document_body = soup.document
        symbols = document_body.find_all(TexExtractor.MATH_SYMBOLS)
        for index, symbol in enumerate(symbols):
            temp = symbol.copy()
            symbol.replace_with("") #shit breaks here bc there is nothing to replace
            symbols[index] = temp.contents 
        paragraphs = TexExtractor.getContentsListFromNodeTree(document_body)
        equations = ["".join([str(y) for y in x]) for x in TexExtractor.getContentsListFromNodeTree(symbols)[0]] # 0???
        clearedParagraphs = [y.strip() for y in "".join(paragraphs).split("\n\n") if y != ""]
        clearedEquations = [y.strip() for y in equations if y != ""]
        return clearedParagraphs, clearedEquations

    @staticmethod
    def nodeListToString(nodeList):
        return " ".join(str(x) for x in nodeList)

    @staticmethod
    def is_cache_stale():
        cache_mtime = os.path.getmtime("cached_formulas.json")

        # Sprawdza pliki .tex
        for file_name in os.listdir("tex_file_base"):
            if file_name.endswith(".tex"):
                tex_file_path = os.path.join("tex_file_base", file_name)
                # Sprawdzenie modyfikacji
                if os.path.getmtime(tex_file_path) > cache_mtime:
                    return True
        return False

    @staticmethod
    def parseDocumentList(directory, soups: list[TexSoup]):
        paragraphsCacheFilename = "cached_paragraphs.json"
        formulasCacheFilename = "cached_formulas.json"
        readAccessCode = 1
        paragraphs = None
        formulas = None
        is_cache_stale = TexExtractor.is_cache_stale()
        if is_cache_stale:
            if os.access(os.path.join(directory, paragraphsCacheFilename), readAccessCode):
                with open(os.path.join(directory, paragraphsCacheFilename), "r") as f:
                    paragraphs = json.loads(f.read())
            if os.access(os.path.join(directory, formulasCacheFilename), readAccessCode):
                with open(os.path.join(directory, formulasCacheFilename), "r") as f:
                    formulas = json.loads(f.read())
            if paragraphs and formulas:
                return paragraphs, formulas

        for soup in soups:
            paragraphs, formulas = TexExtractor.separateTextAndEquationNodes(soup)

        
        if is_cache_stale:
            with open(os.path.join(directory, paragraphsCacheFilename), "w") as f:
                f.truncate(0)
                f.write(json.dumps(paragraphs))
            with open(os.path.join(directory, formulasCacheFilename), "w") as f:
                f.truncate(0)
                f.write(json.dumps(formulas))
        
        return paragraphs, formulas
    

if __name__ == "__main__":
    # Example use case
    from document_list_handler import DocumentListHandler

    sampleText = DocumentListHandler.initSoupFromTexFile(os.getcwd() + "/tex_file_base/main1.tex")


    paragraphNodes, equationNodes = TexExtractor.separateTextAndEquationNodes(sampleText)
    documentText = TexExtractor.nodeListToString(paragraphNodes)
    documentEquations = TexExtractor.nodeListToString(equationNodes)
    JUNK = [",", " ", "."]

    text_similarity_ratio = SequenceMatcher(lambda x: x in JUNK, documentText, documentText).ratio()
    equations_similarity_ratio = SequenceMatcher(lambda x: x in JUNK, documentEquations, documentEquations).ratio()

    assert text_similarity_ratio == 1, "DJDJ"
    assert equations_similarity_ratio == 1, "JDJD"
