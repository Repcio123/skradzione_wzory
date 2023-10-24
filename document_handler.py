import os
from TexSoup import TexSoup
class FileHandler:
    text:list=[]
    paragraphs:list=[]
    formulas:list=[]
    def load_text(self): #from file
        for file_name in os.listdir(os.getcwd()+"\\files_to_test"):
            with open(os.getcwd()+"\\files_to_test\\"+file_name,"r") as file:
                self.text+=[file.read()]
    def get_paragraphs_and_formulas(self,index:int):
        soup=TexSoup(self.text[index])
        print(soup.find_all('section'))
        #extract paragraphs (or chunks of text) and formulas
        #using TexSoup
        
fH=FileHandler()
fH.load_text()
fH.get_paragraphs_and_formulas(1)
#TODO:
#1. basic file handler - to text
#2. separation by backslash instructions
#3. using imported method for checking plagarism
#4. (BONUS) generate html report