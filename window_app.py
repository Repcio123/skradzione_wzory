from tkinter import Tk,Canvas,Button, filedialog,Text,Checkbutton,Label,Scrollbar,NS,IntVar
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
    selected_methods=[]
    if(char_method_var.get()==1):selected_methods+=[1]
    if(word_method_var.get()==1):selected_methods+=[2]
    if(phrase_method_var.get()==1):selected_methods+=[3]
    if(hash_method_var.get()==1):selected_methods+=[4]
    if(formula_levenshtein_var.get()==1):selected_methods+=[5]
    if(formula_cosine_var.get()==1):selected_methods+=[6]
    if(formula_jaccard_var.get()==1):selected_methods+=[7]
    print("Selected methods: ", selected_methods)
    #execute the methods on selected file
    #print out results
    #modify html report
window=Tk()
char_method_var=IntVar()
word_method_var=IntVar()
phrase_method_var=IntVar()
hash_method_var=IntVar()
word_method_var=IntVar()
formula_levenshtein_var=IntVar()
formula_cosine_var=IntVar()
formula_jaccard_var=IntVar()
window.title("LaTeX AntiPlagarism App")
upload_button=Button(text="Upload to Base", command=upload_file_to_base)
upload_button.grid(column=0,row=1)
check_file_button=Button(text="Pick Article\n to Check",command=select_file_to_check)
check_file_button.grid(column=0,row=2)
paragraph_method_label=Label(text="Paragraphs")
paragraph_method_label.grid(column=2,row=0)
char_method_checkbox=Checkbutton(text="By chars",variable=char_method_var)
char_method_checkbox.grid(column=2,row=1)
word_method_checkbox=Checkbutton(text="By words",variable=word_method_var)
word_method_checkbox.grid(column=2,row=2)
phrase_method_checkbox=Checkbutton(text="By phrases",variable=phrase_method_var)
phrase_method_checkbox.grid(column=2,row=3)
hash_method_checkbox=Checkbutton(text="By hashes",variable=hash_method_var)
hash_method_checkbox.grid(column=2,row=4)
formula_method_label=Label(text="Formulas")
formula_method_label.grid(column=2,row=5)
levenshtein_formula_method_checkbox=Checkbutton(text="By Levenshtein",variable=formula_levenshtein_var)
levenshtein_formula_method_checkbox.grid(column=2,row=6)
cosine_formula_method_checkbox=Checkbutton(text="By Cosine",variable=formula_cosine_var)
cosine_formula_method_checkbox.grid(column=2,row=7)
jaccard_formula_method_checkbox=Checkbutton(text="By Jaccard",variable=formula_jaccard_var)
jaccard_formula_method_checkbox.grid(column=2,row=8)
filePath_label=Label()
filePath_label.grid(column=3,row=1)
analyze_button=Button(text="Analyze",command=analyze)
analyze_button.grid(column=3,row=3)
window.mainloop()