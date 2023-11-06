import os
from TexSoup import TexSoup
<<<<<<< Updated upstream
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
=======
from extractor import TexExtractor

class DocumentListHandler:
    test_cases: list[TexSoup] = []
    paragraphs: list[str] = []
    formulas: list[str] = []
    
    @staticmethod
    def initSoupFromTexFile(filename: str):
        with open(filename, "r") as f:
            try:
                file_contents = f.read()
                return TexSoup(file_contents)
            except:
                raise Exception(f"failed to parse latex")

    def load_from_files(self, dir):
        for file_name in os.listdir(dir):
            soup = DocumentListHandler.initSoupFromTexFile(f"{dir}/{file_name}")
            text, equations = TexExtractor.separateTextAndEquationNodes(soup)
            self.paragraphs.append(TexExtractor.nodeListToString(text))
            self.formulas.append(TexExtractor.nodeListToString(equations))
    
    def load_from_files_and_save_extracted(self,dir,saveText,saveEquations):
        for file_name in os.listdir(dir):
            soup = DocumentListHandler.initSoupFromTexFile(f"{dir}/{file_name}")
            text, equations = TexExtractor.separateTextAndEquationNodes(soup)
            file_for_text=open(saveText+"/"+file_name[:-3]+"txt","w")
            text_string=str(text[0])
            for par in text[1:]:
                text_string+="\n"+str(par)
            file_for_text.write(text_string)
            file_for_text.close()
            file_for_equations=open(saveEquations+"/"+file_name[:-3]+"txt","w")
            equations_string=str(equations[0])
            for eq in equations[1:]:
                equations_string+="\n"+str(eq)
            file_for_equations.write(equations_string)
            file_for_equations.close()

    def load_paragraphs_from_prepared_paragraphs(self,prepParagsFolder):
        self.paragraphs=[]
        for file_name in os.listdir(prepParagsFolder):
            paragraphs_in_file=[]
            file=open(f"{prepParagsFolder}/{file_name}","r")
            for line in file.read().split("\n"):
                paragraphs_in_file+=[line] #by line, needs checking
            self.paragraphs+=[paragraphs_in_file]
            file.close()

    def load_formluas_from_prepared_formualas(self,prepFormulasFolder):
        self.formulas=[]
        for file_name in os.listdir(prepFormulasFolder):
            formulas_in_file=[]
            file=open(f"{prepFormulasFolder}/{file_name}","r")
            for line in file.read().split("\n"):
                formulas_in_file+=[line] #by line, needs checking, seems ok
            self.formulas+=[formulas_in_file]
            file.close()
    
            


TEX_FOLDER_NAME = "tex_file_base"
TEX_SAVE_TEXT_FOLDER="prepared_paragraphs"
TEX_SAVE_FORMULAS_FOLDER="prepared_formulas"   
if __name__ == "__main__":
    file_handler = DocumentListHandler()
    file_handler.load_from_files(f"{os.getcwd()}/{TEX_FOLDER_NAME}")
    #file_handler.load_from_files_and_save_extracted(f"{os.getcwd()}/{TEX_FOLDER_NAME}",f"{os.getcwd()}/{TEX_SAVE_TEXT_FOLDER}",f"{os.getcwd()}/{TEX_SAVE_FORMULAS_FOLDER}")
    #print(file_handler.paragraphs, "\n\n\n")
    #file_handler.load_paragraphs_from_prepared_paragraphs(f"{os.getcwd()}/{TEX_SAVE_TEXT_FOLDER}")
    #print(file_handler.paragraphs) # not as it should be - needs consulting
    print(file_handler.formulas,"\n\n\n")
    file_handler.load_formluas_from_prepared_formualas(f"{os.getcwd()}/{TEX_SAVE_FORMULAS_FOLDER}")
    print(file_handler.formulas)

>>>>>>> Stashed changes
#TODO:
#1. basic file handler - to text (DONE)
#2. getting paragraphs/chunks of text and formulas into lists
#3. using imported method for checking plagarism
#4. (BONUS) generate html report