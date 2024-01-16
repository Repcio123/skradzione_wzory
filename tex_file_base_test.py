import os
import json
from TexSoup import TexSoup
from antiplagarism_tools import AntiPlagarism
from document_list_handler import DocumentListHandler

TEX_FOLDER = 'tex_file_base/tex'


def get_documents_list() -> list[str]:
    return os.listdir(TEX_FOLDER)


def is_min_tex_amount(files):
    assert len(files) >= 50, "Test zakończony niepowodzeniem: Za mało dokumentów w bazie."
    print("Test zakończony sukcesem: Odpowiednia ilość dokumentów bazie")

class IdenticalFunctionsTester:
    def __init__(self, tested_document_path, document_base_path):
        self.tested_document_path = tested_document_path
        self.document_base_path = document_base_path
        self.antiPlagarism = None  # Initialize antiPlagarism as an instance variable

    def run_tests(self):
        tested_document = DocumentListHandler.initSoupFromTexFile(self.tested_document_path)
        document_base = DocumentListHandler.init_tex_document_base(self.document_base_path)
        self.antiPlagarism = AntiPlagarism(document_base)  # Assign the antiPlagarism instance

        self._test_hashes(tested_document)
        self._test_chars(tested_document)
        self._test_levenstein(tested_document)
        self._test_jaccard(tested_document)
        self._test_cosine(tested_document)

    def _test_hashes(self, tested_document):
        results_hashes = self.antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_full_content_hashes)
        assert results_hashes[0].ratio == 1, "Test po hashach zakończony niepowodzeniem: Dokumenty nie są identyczne."
        print("Test po hashach zakończony sukcesem: Dokumenty są identyczne")

    def _test_chars(self, tested_document):
        tested_document_content = TexSoup(open(self.tested_document_path, 'r').read())
        results_chars = self.antiPlagarism.compare_to_document_base(tested_document_content, AntiPlagarism.test_by_chars)
        assert results_chars[0].ratio > 99, "Test po znakach zakończony niepowodzeniem: Dokumenty nie są identyczne po znakach."
        print("Test po znakach zakończony sukcesem: Dokumenty są identyczne.")

    def _test_levenstein(self, tested_document):
        results_levenstein = self.antiPlagarism.test_lavenshtein_distance(tested_document, tested_document)
        assert results_levenstein.distance == 0, "Test Levensteina zakończony niepowodzeniem: Dokumenty nie są identyczne."
        print("Test Levensteina zakończony powodzeniem: Dokumenty są identyczne.")

    def _test_jaccard(self, tested_document):
        results_jaccard = self.antiPlagarism.test_jaccard_distance(tested_document, tested_document)
        assert results_jaccard.ratio == 100, "Test Jaccarda zakończony niepowodzeniem: Dokumenty nie są identyczne."
        print("Test Jaccarda zakończony powodzeniem: Dokumenty są identyczne.")

    def _test_cosine(self, tested_document):
        results_cosine = self.antiPlagarism.test_cosine_distance(tested_document, tested_document)
        assert results_cosine.ratio == 100, "Test Cosine zakończony niepowodzeniem: Dokumenty nie są identyczne."
        print("Test Jaccarda zakończony powodzeniem: Dokumenty są identyczne.")

if __name__ == "__main__":
    is_min_tex_amount(get_documents_list())
    tester = IdenticalFunctionsTester("tests/identicalCheck/tex/graphs.tex", "tests/identicalCheck")
    tester.run_tests()
