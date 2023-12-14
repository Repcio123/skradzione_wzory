
from Levenshtein import distance as levenshtein_distance,matching_blocks as levenshtein_matching_blocks,editops as levenshtein_editops, ratio as levenshtein_similarity_ratio
from TexSoup import TexSoup
from hashlib import md5
from document_list_handler import DocumentListHandler
from extractor import TexExtractor
import os
import numpy as np
from numpy.linalg import norm
from collections import Counter
import math
from dataclasses import dataclass
from typing import Callable

test_document_folder_path = os.path.join(os.getcwd(), "tex_file_base")

@dataclass
class AntiPlagiatResult:
    method: str
    distance: float
    matched: list[str]
    ratio: float

class AntiPlagarism:
    word_threshold: int = 15
    char_sensitivity: int = 8  # one per this chars can be mismatched to give match
    text_base: list[TexSoup] = []

    def __init__(self, text_base) -> None:
        self.text_base = text_base

    def load_file_base(self):
        for file_name in os.listdir(os.getcwd()+"\\tex_file_base"):
            with open(os.getcwd()+"\\tex_file_base\\"+file_name, "r") as file:
                self.text_base += [file.read()]

    def by_chars(self, checked: str):
        ...

    def by_words(self, checked: str):
        ...
    def with_nlp(self, checked: str):
        ...

    @staticmethod
    def compare_paragraph_hashes(paragraphs1: list[str], paragraphs2: list[str]):
        matchedSections = []
        totalLength = len(TexExtractor.nodeListToString(paragraphs1))
        ratio = 0
        distance = totalLength
        for testedParagraph in paragraphs1:
            for referenceParagraph in paragraphs2:
                if AntiPlagarism.compare_hashes(TexExtractor.nodeListToString(testedParagraph), TexExtractor.nodeListToString(referenceParagraph)):
                    matched = testedParagraph
                    matchedLength = len(matched)
                    matchedSections.append(matched)
                    ratio += matchedLength / totalLength
                    distance -= matchedLength
        return AntiPlagiatResult("compare_paragraph_hashes", distance, matchedSections, 100*ratio)

    @staticmethod
    def test_paragraph_hashes(tested_document: TexSoup, other_document: TexSoup):
        tested_paragraphs, tested_equations = TexExtractor.separateTextAndEquationNodes(tested_document)
        tested_document_contents = [*tested_paragraphs, *tested_equations]

        paragraphs, equations = TexExtractor.separateTextAndEquationNodes(other_document)
        document_contents = [*paragraphs, *equations]
        return AntiPlagarism.compare_paragraph_hashes(tested_document_contents, document_contents)

    def compare_to_document_base(self, tested_document: TexSoup, comparison_function: Callable[[str, str], AntiPlagiatResult]):
        return [comparison_function(tested_document, document) for document in self.text_base]
        
    @staticmethod
    def test_full_content_hashes(tested_document: TexSoup, other_document: TexSoup):

        tested_paragraphs, tested_equations = TexExtractor.separateTextAndEquationNodes(tested_document)
        tested_document_paragraphs = TexExtractor.nodeListToString(tested_paragraphs)
        tested_document_equations = TexExtractor.nodeListToString(tested_equations)

        paragraphs, equations = TexExtractor.separateTextAndEquationNodes(other_document)
        document_paragraphs = TexExtractor.nodeListToString(paragraphs)
        document_equations = TexExtractor.nodeListToString(equations)

        matchedParagraphs = AntiPlagarism.compare_hashes(tested_document_paragraphs, document_paragraphs)
        matchedEquations = AntiPlagarism.compare_hashes(tested_document_equations, document_equations)

        symbolCount = len(tested_document_paragraphs) + len(tested_document_equations)

        if matchedParagraphs and matchedEquations:
            return AntiPlagiatResult("content hashes", 0, [tested_document_paragraphs, tested_document_equations], 1)

        if matchedParagraphs:
            distance = symbolCount - len(tested_document_paragraphs)
            matched = [tested_document_paragraphs]
            ratio = 100 * (len(tested_document_paragraphs) / symbolCount)
            return AntiPlagiatResult("content hashes", distance, matched, ratio)

        if matchedEquations:
            distance = symbolCount - len(tested_document_equations)
            matched = [tested_document_equations]
            ratio = 100 * (len(tested_document_equations) / symbolCount)
            return AntiPlagiatResult("content hashes", distance, matched, ratio)

        return AntiPlagiatResult("content hashes", symbolCount, [], 0)

    @staticmethod
    def compare_hashes(testedDocument: str, otherDocument: str):
        return md5(testedDocument.encode()).hexdigest() == md5(otherDocument.encode()).hexdigest()

    @staticmethod
    def formula_check_levenshtein_simple(str1: str,str2: str):
        distance = levenshtein_distance(str1, str2)
        matches = levenshtein_matching_blocks(levenshtein_editops(str1, str2), str1, str2)
        list_of_matches = [str1[x[0]:x[0]+x[2]] for x in matches]
        ratio = levenshtein_similarity_ratio(str1, str2) * 100
        return AntiPlagiatResult("lavenshtein", distance, list_of_matches, ratio)
        # simple levenshtein check, to be tweaked later
        # needs difference extrapolation about differences
        # distance is distance which we use to get a percentage
    
    @staticmethod
    def test_lavenshtein_distance(tested_document: TexSoup, other_document: TexSoup):
        tested_paragraphs, tested_equations = TexExtractor.separateTextAndEquationNodes(tested_document)
        tested_document_contents = TexExtractor.nodeListToString([*tested_paragraphs, *tested_equations])
        paragraphs, equations = TexExtractor.separateTextAndEquationNodes(other_document)
        document_paragraphs = TexExtractor.nodeListToString([*paragraphs, *equations])
        return AntiPlagarism.formula_check_levenshtein_simple(tested_document_contents, document_paragraphs)

    @staticmethod
    def formula_split_symbols(formula:str):
        long_name_symbols=["\Alpha","\\alpha","\Beta","\\beta","\\Gamma","\\gamma","\Delta","\\delta","\\neg","\#","\\frac"]
        symbols_to_ignore=["{","}", " "]
        split_symbols=[]
        i=0
        while(i<len(formula)):
            if formula[i] not in symbols_to_ignore:
                if formula[i]=="\\":
                    long_symbol="\\"
                    while((long_symbol not in long_name_symbols ) and (i<len(formula)-1) and (formula[i] not in symbols_to_ignore)):
                        i+=1
                        long_symbol+=formula[i]
                    split_symbols+=[long_symbol.strip()]
                else:
                    split_symbols+=[formula[i]]
            i+=1
        return split_symbols

    @staticmethod
    def formula_check_cosine(l1: list[str], l2: list[str]): #list of symbols
        vec1 = Counter(l1)
        vec2 = Counter(l2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

        #can have a parameter to check by n symbol parts

    @staticmethod
    def formula_check_jaccard(l1: list[str],l2: list[str]):
        intersection = len(list(set(l1).intersection(l2)))
        union = (len(set(l1)) + len(set(l2))) - intersection
        return float(intersection) / union
        # need to separate stuff into a list with operators and symbols
        ...
    #def formula_check_tree_model(self,checked:str): #optional
        # make a tree with separated operators as parent nodes and operands as children
        ...
    #def with_nlp(self,checked:str):
        ...

#if __name__=='__main__':
    #distance,matches,ratio=AntiPlagarism.formula_check_levenshtein_simple('sitting','kitten')
    #print(f"Levenshtein distance for formulas:\nDistance: {distance}\nPercent: {ratio}%\nMatches: {matches}")
#    test = "jd"

if __name__ == '__main__':
    tested_document = DocumentListHandler.initSoupFromTexFile("files_to_test/lagrange.tex")
    document_base = DocumentListHandler.init_tex_document_base("tex_file_base")
    antiPlagarism = AntiPlagarism(document_base)

    results1 = antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_paragraph_hashes)
    results2 = antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_full_content_hashes)
    results3 = antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_lavenshtein_distance)
    listdir = os.listdir(os.path.join("tex_file_base", "tex"))

    results = list(zip(listdir, results1, results2, results3))
    print("results for file files_to_test/lagrange.tex:S")
    for test_document, r1, r2, r3 in results:
        print(
            f"{test_document}:", 
            f"{r1.method}: distance: {r1.distance}, match_count: {len(r1.matched)}, ratio: {r1.ratio}",
            f"{r2.method}: distance: {r2.distance}, match_count: {len(r2.matched)}, ratio: {r2.ratio}",
            f"{r3.method}: distance: {r3.distance}, match_count: {len(r3.matched)}, ratio: {r3.ratio}",
            "-----------------------------------------------------------------",
            sep="\n")


# TODO:
# 0. preparation
#   - load the paragraphs into class (DONE)
#   - load the formulas into class
# 1. function with string comparison
#   - by words
#       * word threshold (eg. 20 in a row)
#       * if eg. 1 in 8 chars are mismatched, it is still considered a match
#   - by sentences (eg. 2 sentences matched means plagarism)
#   -
# 2. formula comparison
#   - using trees to represent formulas
#   - checking the formula structure - plagarised when formulas are the same with different variable names
# 3. different plagarism degrees
#   - overt plagarism (very visible)
#   - possible plagarism (not 100%, but has proof of possibility for plagarism)
#   - vague plagarism (eg. sophisticated words, which happened in other works, every other word matched)
