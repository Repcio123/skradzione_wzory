
from TexSoup import TexSoup
import os
class TexParagraphExtractor:
    def extract_paragraphs(self, tex_text):
        paragraphs=[]
        soup=TexSoup(tex_text)
        for p in soup.find_all('paragraph'):
            paragraphs+=[p.string]
        print(paragraphs)
tPE=TexParagraphExtractor()
with open(os.getcwd()+"//tex_file_base//dummy_PCA.tex","r") as file:
    sampleText=file.read()
tPE.extract_paragraphs(sampleText)

#TODO:
#1. make a function to extract paragraphs/text chunks from article
#2. make a function to extract formulas from article