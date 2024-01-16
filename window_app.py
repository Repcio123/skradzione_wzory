from tkinter import filedialog,NS,IntVar,StringVar
from customtkinter import CTk,CTkButton,CTkLabel,CTkTextbox,CTkSwitch,CTkFrame,set_appearance_mode
import shutil,os
import antiplagarism_tools as at
import document_list_handler as dlh

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
    path_variable.set("Selected Article: \n"+path.split("/")[-1])

def analyze():
    selected_methods=[]
    if(char_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_by_chars]
    if(phrase_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_paragraph_hashes]
    if(hash_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_full_content_hashes]
    if(formula_levenshtein_var.get()==1):selected_methods+=[at.AntiPlagarism.test_lavenshtein_distance]
    if(formula_cosine_var.get()==1):selected_methods+=[at.AntiPlagarism.test_cosine_distance]
    if(formula_jaccard_var.get()==1):selected_methods+=[at.AntiPlagarism.test_jaccard_distance]
    print("Selected methods: ", selected_methods)
    
    article_name=path_variable.get().split("\n")[1]
    tested_document = dlh.DocumentListHandler.initSoupFromTexFile("files_to_test/"+article_name)
    document_base = dlh.DocumentListHandler.init_tex_document_base("tex_file_base")
    antiPlagarism = at.AntiPlagarism(document_base)

    listdir = os.listdir(os.path.join("tex_file_base", "tex"))

    results = [*zip(listdir, *(antiPlagarism.compare_to_document_base(tested_document, method) for method in selected_methods))]

    for document, *result in results:
        print(f"document: {document}")
        for r in result:
            print(f"{r.method}: distance: {r.distance}, match_count: {len(r.matched)}, ratio: {r.ratio}"),
    


    #execute the methods on selected file
    #print out results
    #modify html report

window=CTk()
set_appearance_mode('dark')
path_variable=StringVar()
path_variable.set("Selected Article:")
char_method_var=IntVar()
word_method_var=IntVar()
phrase_method_var=IntVar()
hash_method_var=IntVar()
word_method_var=IntVar()
formula_levenshtein_var=IntVar()
formula_cosine_var=IntVar()
formula_jaccard_var=IntVar()
window.title("LaTeX AntiPlagarism App")
left_mid_padding=CTkFrame(window,width=20,fg_color="transparent").grid(column=1,row=1,rowspan=6)
upload_button=CTkButton(window,text="Upload to Base", command=upload_file_to_base,corner_radius=32)
upload_button.grid(column=0,row=1)
check_file_button=CTkButton(window,text="Pick Article\n to Check",command=select_file_to_check,corner_radius=64)
check_file_button.grid(column=0,row=3)
filePath_selected_label=CTkLabel(window,textvariable=path_variable)
filePath_selected_label.grid(column=0,row=4)
analyze_button=CTkButton(window,text="Analyze",command=analyze,corner_radius=32)
analyze_button.grid(column=0,row=6)
select_methods_label=CTkLabel(window,text="Select methods")
select_methods_label.grid(column=2,row=0)
char_method_checkbox=CTkSwitch(window,text="By chars",variable=char_method_var)
char_method_checkbox.grid(column=2,row=1)
phrase_method_checkbox=CTkSwitch(window,text="By phrases",variable=phrase_method_var)
phrase_method_checkbox.grid(column=2,row=2)
hash_method_checkbox=CTkSwitch(window,text="By hashes",variable=hash_method_var)
hash_method_checkbox.grid(column=2,row=3)
levenshtein_formula_method_checkbox=CTkSwitch(window,text="By Levenshtein",variable=formula_levenshtein_var)
levenshtein_formula_method_checkbox.grid(column=2,row=4)
cosine_formula_method_checkbox=CTkSwitch(window,text="By Cosine",variable=formula_cosine_var)
cosine_formula_method_checkbox.grid(column=2,row=5)
jaccard_formula_method_checkbox=CTkSwitch(window,text="By Jaccard",variable=formula_jaccard_var)
jaccard_formula_method_checkbox.grid(column=2,row=6)
right_mid_padding=CTkFrame(window,width=20,fg_color="transparent").grid(column=3,row=1,rowspan=6)
result_label=CTkLabel(window,text="Results:")
result_label.grid(column=4,row=0)
result_box=CTkTextbox(window)
result_box.grid(column=4,row=2,rowspan=6)
window.mainloop()

# make frames for left, middle, right panel