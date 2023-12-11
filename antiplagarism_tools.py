
from Levenshtein import distance as levenshtein_distance,matching_blocks as levenshtein_matching_blocks,editops as levenshtein_editops, ratio as levenshtein_similarity_ratio
from TexSoup import TexSoup
from hashlib import md5
from document_list_handler import DocumentListHandler
from extractor import TexExtractor
import os


class AntiPlagarism:
    word_threshold: int = 15
    char_sensitivity: int = 8 #one per this chars can be mismatched to give match

    def by_chars(self, checked: str):
        ...

    def by_words(self,checked: str):
        ...

    def with_nlp(self, checked: str):
        ...

    @staticmethod
    def compare_paragraph_hashes(testedDocument: TexSoup):
        testedParagraphs, testedEquations = TexExtractor.separateTextAndEquationNodes(testedDocument)

        document_list_handler = DocumentListHandler()
        document_list_handler.load_from_files(os.path.join(os.getcwd(), "tex_file_base"), lazy=True)
        
        textSymbolCount = len(TexExtractor.nodeListToString(testedParagraphs))
        equationSymbolCount = len(TexExtractor.nodeListToString(testedEquations))
        assert textSymbolCount != 0 and equationSymbolCount != 0, "???"
        matchedSections = []
        
        for document in document_list_handler.text_base:
            paragraphs, equations = TexExtractor.separateTextAndEquationNodes(document)

            for testedParagraph in testedParagraphs:
                for paragraph in paragraphs:
                    if AntiPlagarism.compare_hashes(testedParagraph, paragraph):
                        matched = paragraph
                        ratio = 100 * (len(paragraph) / textSymbolCount)
                        matchedSections.append((matched, ratio))
            
            for testedEquation in testedEquations:
                for equation in equations:
                    if AntiPlagarism.compare_hashes(TexExtractor.nodeListToString(testedEquation), TexExtractor.nodeListToString(equation)):
                        matched = equation
                        ratio = 100 * (len(equation) / equationSymbolCount)
                        matchedSections.append((matched, ratio))

        list_of_matches = list(map(lambda x: x[0], matchedSections))
        totalRatio = sum(map(lambda x: x[1], matchedSections))
        # Nie wiem czym ma byc distance w tym przypadku
        return list_of_matches, totalRatio

    @staticmethod
    def compare_content_hashes(testedDocument: TexSoup):

        testedParagraphs, testedEquations = TexExtractor.separateTextAndEquationNodes(testedDocument)
        testedFullTextContent = TexExtractor.nodeListToString(testedParagraphs)
        testedFullEquationsContent = TexExtractor.nodeListToString(testedEquations)

        document_list_handler = DocumentListHandler()
        document_list_handler.load_from_files(os.path.join(os.getcwd(), "tex_file_base"), lazy=True)

        #hash tests
        for document in document_list_handler.text_base:
            # porownaj po full content hash
            paragraphs, equations = TexExtractor.separateTextAndEquationNodes(document)
            fullTextContent = TexExtractor.nodeListToString(paragraphs)
            fullEquationContent = TexExtractor.nodeListToString(equations)
            matchedParagraphs = AntiPlagarism.compare_hashes(fullTextContent, testedFullTextContent)
            matchedEquations = AntiPlagarism.compare_hashes(fullEquationContent, testedFullEquationsContent)

            assert len(fullTextContent) * len(fullEquationContent) != 0, "Co ty odjaniepawlasz??"
            symbolCount = len(fullTextContent) + len(fullEquationContent)

            if matchedParagraphs and matchedEquations:
                return 0, document, 1 

            if matchedParagraphs:
                distance = len(fullTextContent)
                matched = fullTextContent
                ratio = 100 * (len(fullTextContent) / symbolCount)
                return distance, matched, ratio

            if matchedEquations:
                distance = len(fullEquationContent)
                matched = fullEquationContent
                ratio = 100 * (len(fullEquationContent) / symbolCount)
                return distance, matched, ratio

    @staticmethod
    def compare_hashes(testedDocument: str, otherDocument: str):
        return md5(testedDocument.encode()).hexdigest() == md5(otherDocument.encode()).hexdigest()

    @staticmethod
    def formula_check_levenshtein_simple(str1: str,str2: str):
        distance = levenshtein_distance(str1, str2)
        matches = levenshtein_matching_blocks(levenshtein_editops(str1, str2), str1, str2)
        list_of_matches = [str1[x[0]:x[0]+x[2]] for x in matches]
        ratio = levenshtein_similarity_ratio(str1, str2) * 100
        return distance, list_of_matches, ratio
        # simple levenshtein check, to be tweaked later
        # needs difference extrapolation about differences
        # distance is distance which we use to get a percentage
    @staticmethod
    def formula_split_symbols(formula:str):
        long_name_symbols=["\Alpha","\\alpha","\Beta","\\beta","\\Gamma","\\gamma","  ","+","-","\\neg","!","\#"]
    def formula_check_cosine_simple(self,l1:list,l2:list): #list of symbols
        # simple cosine check, to be tweaked later
        ...

    def formula_check_jaccard(self,checked:str):
        # need to separate stuff into a list with operators and symbols
        ...
    #def formula_check_tree_model(self,checked:str): #optional
        # make a tree with separated operators as parent nodes and operands as children
        ...
    #def with_nlp(self,checked:str):
        ...
if __name__=='__main__':
    #distance,matches,ratio=AntiPlagarism.formula_check_levenshtein_simple('sitting','kitten')
    #print(f"Levenshtein distance for formulas:\nDistance: {distance}\nPercent: {ratio}%\nMatches: {matches}")
    test = "jd"

#TODO:
#0. preparation
#   - load the paragraphs into class (DONE)
#   - load the formulas into class 
#1. function with string comparison
#   - by words
#       * word threshold (eg. 20 in a row)
#       * if eg. 1 in 8 chars are mismatched, it is still considered a match
#   - by sentences (eg. 2 sentences matched means plagarism)
#   -
#2. formula comparison
#   - using trees to represent formulas
#   - checking the formula structure - plagarised when formulas are the same with different variable names
#3. different plagarism degrees
#   - overt plagarism (very visible)
#   - possible plagarism (not 100%, but has proof of possibility for plagarism)
#   - vague plagarism (eg. sophisticated words, which happened in other works, every other word matched)

