import os
import json

from antiplagarism_tools import AntiPlagarism
from document_list_handler import DocumentListHandler
TEX_FOLDER_LAPLACE = 'files_to_test/fewer_sections/laplace'
TEX_FOLDER_MAIN4 = 'files_to_test/fewer_sections/main4'

class FewerSections():
    def __init__(self):
        self.testedDocumentLaplace = DocumentListHandler.initSoupFromTexFile('files_to_test/fewer_sections/laplace/tex/laplace.tex')
        self.docBaseLaplace = DocumentListHandler.init_tex_document_base(TEX_FOLDER_LAPLACE)
        self.testedDocumentMain4 = DocumentListHandler.initSoupFromTexFile('files_to_test/fewer_sections/main4/tex/main4.tex')
        self.docBaseMain4 = DocumentListHandler.init_tex_document_base(TEX_FOLDER_MAIN4)

    def compare_articles_by_hashes_test_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentLaplace, AntiPlagarism.test_full_content_hashes)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_by_hashes_test_main4(self):
        antiPlagarism = AntiPlagarism(self.docBaseMain4)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentMain4, AntiPlagarism.test_full_content_hashes)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_by_chars_test_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentLaplace, AntiPlagarism.test_by_chars)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_by_chars_test_main4(self):
        antiPlagarism = AntiPlagarism(self.docBaseMain4)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentMain4, AntiPlagarism.test_by_chars)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_lavensthein_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentLaplace, AntiPlagarism.test_lavenshtein_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_lavensthein_main4(self):
        antiPlagarism = AntiPlagarism(self.docBaseMain4)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentMain4, AntiPlagarism.test_lavenshtein_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_cosine_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentLaplace, AntiPlagarism.test_cosine_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_cosine_main4(self):
        antiPlagarism = AntiPlagarism(self.docBaseMain4)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentMain4, AntiPlagarism.test_cosine_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio

    def compare_articles_jaccard_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseLaplace)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentLaplace, AntiPlagarism.test_jaccard_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio
    
    def compare_articles_jaccard_laplace(self):
        antiPlagarism = AntiPlagarism(self.docBaseMain4)
        results = antiPlagarism.compare_to_document_base(self.testedDocumentMain4, AntiPlagarism.test_jaccard_distance)
        return results[0]['para'].ratio, results[0]['equa'].ratio
    
    def run_tests(self, path):
        with open(path, "w") as f:
            f.write(str(self.compare_articles_by_hashes_test_laplace()) + "\n")
            f.write(str(self.compare_articles_by_hashes_test_main4()) + "\n")
            f.write(str(self.compare_articles_by_chars_test_laplace()) + "\n")
            f.write(str(self.compare_articles_by_chars_test_main4()) + "\n")
            f.write(str(self.compare_articles_lavensthein_laplace()) + "\n")
            f.write(str(self.compare_articles_lavensthein_main4()) + "\n")
            f.write(str(self.compare_articles_cosine_laplace()) + "\n")
            f.write(str(self.compare_articles_cosine_main4()) + "\n")
            f.write(str(self.compare_articles_jaccard_laplace()) + "\n")

if __name__ == "__main__":
    test = FewerSections()
    test.run_tests("files_to_test/fewer_sections/test_results.txt")