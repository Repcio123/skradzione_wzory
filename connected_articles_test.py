import os
import json
from TexSoup import TexSoup
from antiplagarism_tools import AntiPlagarism
from document_list_handler import DocumentListHandler

TEX_FOLDER = 'tex_file_base/tex'

def get_documents_list() -> list[str]:
    return os.listdir(TEX_FOLDER)

class ConnectedArticlesTester:
    def __init__(self, tested_document_path, document_base_path):
        self.tested_document_path = tested_document_path
        self.document_base_path = document_base_path
        self.antiPlagarism = None  # Initialize antiPlagarism as an instance variable
    def run_tests(self):
        tested_document = DocumentListHandler.initSoupFromTexFile(self.tested_document_path)
        document_base = DocumentListHandler.init_tex_document_base(self.document_base_path)
        self.antiPlagarism = AntiPlagarism(document_base)  # Assign the antiPlagarism instance

        with open("files_to_test/connected_test/ConnectedArticleTestResults.txt","w") as file:
            file.write(str(self._test_hashes(tested_document))+"\n")
            file.write(str(self._test_chars(tested_document))+"\n")
            file.write(str(self._test_levenstein(tested_document))+"\n")
            file.write(str(self._test_jaccard(tested_document))+"\n")
            file.write(str(self._test_cosine(tested_document)))

    def _test_hashes(self, tested_document):
        results_hashes = self.antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_full_content_hashes)
        return {"Wynik testu po hashach": [results_hashes[0].ratio, results_hashes[2].ratio]}

    def _test_chars(self, tested_document):
        tested_document_content = TexSoup(open(self.tested_document_path, 'r').read())
        results_chars = self.antiPlagarism.compare_to_document_base(tested_document_content, AntiPlagarism.test_by_chars)
        return {"Wynik testu po charach": [results_chars[0].ratio, results_chars[2].ratio]}

    def _test_levenstein(self, tested_document):
        results_levenstein = self.antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_lavenshtein_distance)
        return {"Wynik testu levensteina": [results_levenstein[0].ratio, results_levenstein[2].ratio]}

    def _test_jaccard(self, tested_document):
        results_jaccard = self.antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_jaccard_distance)
        return {"Wynik testu Jaccarda": [results_jaccard[0].ratio, results_jaccard[2].ratio]}

    def _test_cosine(self, tested_document):
        results_cosine = self.antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_cosine_distance)
        return {"Wynik testu Cosine": [results_cosine[0].ratio, results_cosine[2].ratio]}

if __name__ == "__main__":
    tester = ConnectedArticlesTester("files_to_test/connected_test/tex/numeric_queue.tex", "files_to_test/connected_test")
    tester.run_tests()