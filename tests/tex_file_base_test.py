import os
import json
TEX_FOLDER = 'tex_file_base/tex'


def get_documents_list() -> list[str]:
    return os.listdir(TEX_FOLDER)


def is_min_tex_amount(files):
    assert len(files) >= 50, "minimal amount of documents is done"


if __name__ == "__main__":
    is_min_tex_amount(get_documents_list())
