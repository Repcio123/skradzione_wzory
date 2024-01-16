import os
import json

from antiplagarism_tools import AntiPlagarism
from document_list_handler import DocumentListHandler
TEX_FOLDER = 'tex_file_base/tex'


def get_documents_list() -> list[str]:
    return os.listdir(TEX_FOLDER)


def is_min_tex_amount(files):
    assert len(files) >= 50
    print("Jest 50 dokumentów")

def identical_functions():
    tested_document = DocumentListHandler.initSoupFromTexFile("tests/identicalCheck/tex/graphs.tex")
    document_base = DocumentListHandler.init_tex_document_base("tests/identicalCheck")
    antiPlagarism = AntiPlagarism(document_base)

    results1 = antiPlagarism.compare_to_document_base(tested_document, AntiPlagarism.test_full_content_hashes)
    assert results1[0].ratio == 1 #jesli 1 to sa identyczne 
    print("Są identyczne po hashach")



if __name__ == "__main__":
    is_min_tex_amount(get_documents_list())
    identical_functions()
