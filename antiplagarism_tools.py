import os

class AntiPlagarism:
    word_threshold:int=15
    char_sensitivity:int=8 #one per this chars can be mismatched to give match
    text_base:list=[]
    def load_file_base(self):
        for file_name in os.listdir(os.getcwd()+"\\tex_file_base"):
            with open(os.getcwd()+"\\tex_file_base\\"+file_name,"r") as file:
                self.text_base+=[file.read()]
    def by_chars(self, checked:str):
        ...
    def by_words(self,checked:str):
        ...
    def by_hash(self,checked:str):
        ...
    def with_nlp(self,checked:str):
        ...
    def formula_check(self,checked:str):
        ...

#TODO:
#0. preparation
#   - load the paragraphs into class
#1. function with string comparison
#   - by paragraph
#       * word threshold (eg. 20 in a row)
#       * if eg. 1 in 8 chars are mismatched, it is still considered a match
#   - by sentences (eg. 2 sentences matched means plagarism)
#   -
#2. formula comparison
#   - using trees to represent formulas
#   - checking the formula structure - plagarised when formulas are the same with different variable names
#3. different plagarism degrees
#   - overt plagarism (very visible)
#   - possible plagarism (not 100%, but has proof of possibility for plagarism)
#   - vague plagarism (eg. sophisticated words, which happened in other works, every other word matched)

