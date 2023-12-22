from tkinter import Tk,Canvas,Button, filedialog,Text,Checkbutton,Label,Scrollbar,NS
import shutil,os
import antiplagarism_tools as at
FILEBASE_FOLDER_DIRECTORY="tex_file_base\\tex"
TEST_FOLDER_DIRECTORY="files_to_test"
def upload_file_to_base():
    path=filedialog.askopenfilename()
    shutil.copy(path,os.getcwd()+"\\"+FILEBASE_FOLDER_DIRECTORY)

def select_file_to_check():
    filetypes = (
        ('LaTeX files', '*.tex'),
        ('All files', '*.*')
    )
    path=filedialog.askopenfilename(filetypes=filetypes,initialdir=os.getcwd()+"\\"+TEST_FOLDER_DIRECTORY)
    filePath_label.config(text=path.split("/")[-1])

def analyze():
#    methods_dict={
#        1:at.by_chars,
#        2:at.by_words,
#        3:at.by_phrases,
#        4:at.compare_hashes,
#        5:at.formula_check_levenshtein_simple,
#        6:at.formula_check_cosine, 
#        7:at.formula_check_jaccard
#    } # to implement in code
  #  selected_methods=[]
   # if(char_method_checkbox.state()==["selected"]):selected_methods+=[1]
    #if(word_method_checkbox.state()=="selected"):selected_methods+=[2]
    #if(phrase_method_checkbox.state()=="selected"):selected_methods+=[3]
    #if(hash_method_checkbox.state()=="selected"):selected_methods+=[4]
    #if(levenshtein_formula_method_checkbox.state()=="selected"):selected_methods+=[5]
    #if(cosine_formula_method_checkbox.state()=="selected"):selected_methods+=[6]
    #if(jaccard_formula_method_checkbox.state()=="selected"):selected_methods+=[7]
    #print("Selected methods: ", selected_methods) # to fix
    ...
window=Tk()
window.title("LaTeX AntiPlagarism App")
upload_button=Button(text="Upload to Base", command=upload_file_to_base)
upload_button.grid(column=0,row=1)
check_file_button=Button(text="Pick Article\n to Check",command=select_file_to_check)
check_file_button.grid(column=0,row=2)
paragraph_method_label=Label(text="Paragraphs")
paragraph_method_label.grid(column=2,row=0)
char_method_checkbox=Checkbutton(text="By chars")
char_method_checkbox.grid(column=2,row=1)
word_method_checkbox=Checkbutton(text="By words")
word_method_checkbox.grid(column=2,row=2)
phrase_method_checkbox=Checkbutton(text="By phrases")
phrase_method_checkbox.grid(column=2,row=3)
hash_method_checkbox=Checkbutton(text="By hashes")
hash_method_checkbox.grid(column=2,row=4)
formula_method_label=Label(text="Formulas")
formula_method_label.grid(column=2,row=5)
levenshtein_formula_method_checkbox=Checkbutton(text="By Levenshtein")
levenshtein_formula_method_checkbox.grid(column=2,row=6)
cosine_formula_method_checkbox=Checkbutton(text="By Cosine")
cosine_formula_method_checkbox.grid(column=2,row=7)
jaccard_formula_method_checkbox=Checkbutton(text="By Jaccard")
jaccard_formula_method_checkbox.grid(column=2,row=8)
filePath_label=Label()
filePath_label.grid(column=3,row=1)
analyze_button=Button(text="Analyze",command=analyze)
analyze_button.grid(column=3,row=3)
window.mainloop()