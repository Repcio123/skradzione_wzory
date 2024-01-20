import os
import json

from antiplagarism_tools import AntiPlagarism
from document_list_handler import DocumentListHandler
TEX_FOLDER = 'files_to_test/unique_articles'

class UniqueArticles():
    def __init__(self):
        self.testedDocumentAI = DocumentListHandler.initSoupFromTexFile('files_to_test/unique_articles/tex/AI.tex')
        self.docBaseLaplace = DocumentListHandler.init_tex_document_base(TEX_FOLDER)

    def compare_articles_by_hashes(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentAI, AntiPlagarism.test_full_content_hashes)
        return {"by_hash": [results[1].ratio, results[2].ratio]}

    def compare_articles_by_chars(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentAI, AntiPlagarism.test_by_chars)
        return {"by_chars": [results[1].ratio, results[2].ratio]}

    def compare_articles_lavenshtein(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentAI, AntiPlagarism.test_lavenshtein_distance)
        return {"lavensthein": [results[1].ratio, results[2].ratio]}

    def compare_articles_cosine(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentAI, AntiPlagarism.test_cosine_distance)
        return {"cosine": [results[1].ratio, results[2].ratio]}

    def compare_articles_jaccard(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentAI, AntiPlagarism.test_jaccard_distance)
        return {"jaccard": [results[1].ratio, results[2].ratio]}
    
    
    def run_tests(self, path):
        with open(path, "w") as f:
            f.write(str(self.compare_articles_by_hashes()) + "\n")
            f.write(str(self.compare_articles_by_chars()) + "\n")
            f.write(str(self.compare_articles_lavenshtein()) + "\n")
            f.write(str(self.compare_articles_cosine()) + "\n")
            f.write(str(self.compare_articles_jaccard()) + "\n")

if __name__ == "__main__":
    test = UniqueArticles()
    test.run_tests("files_to_test/unique_articles/test_results.txt")