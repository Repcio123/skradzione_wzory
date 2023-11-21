import os
from typing import Optional
from weakref import WeakValueDictionary
import hashlib

from Levenshtein import distance as levenshtein_distance,matching_blocks as levenshtein_matching_blocks,editops as levenshtein_editops, ratio as levenshtein_similarity_ratio

class CachedRecord:
    hash_cache = WeakValueDictionary()
    hash_function = hashlib.md5

    def __init__(self, text: str):
        self.text = text
        CachedRecord.hash_cache[CachedRecord.encode(text)] = self
    
    @staticmethod
    def encode(text: str) -> str:
        return CachedRecord.hash_function(text.encode("utf-8")).hexdigest()

    @staticmethod
    def get(text) -> Optional[object]:
        return CachedRecord.hash_cache.get(CachedRecord.encode(text))


class AntiPlagarism:
    word_threshold:int=15
    char_sensitivity:int=8 #one per this chars can be mismatched to give match
    text_base: list[CachedRecord]=[]

    def load_file_base(self):
        #  os.join for system interop (/ and \)
        for file_name in os.listdir(os.path.join(os.getcwd(), "tex_file_base")):
            with open(os.path.join(os.getcwd(), "tex_file_base", file_name), "r") as file:
                self.text_base+=[CachedRecord(file.read())]

    def by_chars(self, checked: str):
        ...
    def by_words(self,checked: str):
        ...

    def by_hash(self, checked: str) -> Optional[CachedRecord]:
        return CachedRecord.get(checked)

    def with_nlp(self,checked:str):
        ...
    @staticmethod
    def formula_check_levenshtein_simple(str1:str,str2:str):
        distance=levenshtein_distance(str1,str2)
        matches=levenshtein_matching_blocks(levenshtein_editops(str1,str2),str1,str2)
        list_of_matches=[str1[x[0]:x[0]+x[2]] for x in matches]
        ratio=levenshtein_similarity_ratio(str1,str2)*100
        return distance,list_of_matches,ratio
        # simple levenshtein check, to be tweaked later
        # needs difference extrapolation about differences
        # distance is distance which we use to get a percentage
        ...
    def formula_check_cosine_simple(self,checked:str):
        # simple cosine check, to be tweaked later
        ...
    def formula_check_jaccard(self,checked:str):
        # need to separate stuff into a list with operators and symbols
        ...
    def formula_check_tree_model(self,checked:str):
        # make a tree with separated operators as parent nodes and operands as children
        ...
if __name__=='__main__':
    #distance,matches,ratio=AntiPlagarism.formula_check_levenshtein_simple('sitting','kitten')
    #print(f"Levenshtein distance for formulas:\nDistance: {distance}\nPercent: {ratio}%\nMatches: {matches}")
    test = "jd"

#TODO:
#0. preparation
#   - load the paragraphs into class (DONE)
#   - load the formulas into class 
#1. function with string comparison
#   - by words
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

