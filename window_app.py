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
    if(left_panel.char_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_by_chars]
    if(left_panel.phrase_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_paragraph_hashes]
    if(left_panel.hash_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_full_content_hashes]
    if(left_panel.formula_levenshtein_var.get()==1):selected_methods+=[at.AntiPlagarism.test_lavenshtein_distance]
    if(left_panel.formula_cosine_var.get()==1):selected_methods+=[at.AntiPlagarism.test_cosine_distance]
    if(left_panel.formula_jaccard_var.get()==1):selected_methods+=[at.AntiPlagarism.test_jaccard_distance]
    print("Selected methods: ", selected_methods)
    if(len(left_panel.path_variable.get().split("\n"))<2):return
    article_name=left_panel.path_variable.get().split("\n")[1]
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
class Left_Panel(CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.char_method_var=IntVar()
        self.word_method_var=IntVar()
        self.phrase_method_var=IntVar()
        self.hash_method_var=IntVar()
        self.word_method_var=IntVar()
        self.formula_levenshtein_var=IntVar()
        self.formula_cosine_var=IntVar()
        self.formula_jaccard_var=IntVar()
        self.upload_button=CTkButton(self,text="Upload to Base", command=upload_file_to_base,corner_radius=32).grid(column=0,row=0,pady=20)
        self.check_file_button=CTkButton(self,text="Pick Article\n to Check",command=select_file_to_check,corner_radius=64).grid(column=0,row=2,pady=20)
        self.filePath_selected_label=CTkLabel(self,textvariable=path_variable).grid(column=0,row=3,pady=20)
        self.select_methods_label=CTkLabel(self,text="Select methods").grid(column=0,row=5)
        self.char_method_checkbox=CTkSwitch(self,text="By chars",variable=self.char_method_var).grid(column=0,row=6)
        self.phrase_method_checkbox=CTkSwitch(self,text="By phrases",variable=self.phrase_method_var).grid(column=0,row=7)
        self.hash_method_checkbox=CTkSwitch(self,text="By hashes",variable=self.hash_method_var).grid(column=0,row=8)
        self.levenshtein_formula_method_checkbox=CTkSwitch(self,text="By Levenshtein",variable=self.formula_levenshtein_var).grid(column=0,row=9)
        self.cosine_formula_method_checkbox=CTkSwitch(self,text="By Cosine",variable=self.formula_cosine_var).grid(column=0,row=10)
        self.jaccard_formula_method_checkbox=CTkSwitch(self,text="By Jaccard",variable=self.formula_jaccard_var).grid(column=0,row=11)
        self.analyze_methods_padding=CTkFrame(self,height=20,fg_color="transparent").grid(column=0,row=12)
        self.analyze_button=CTkButton(self,text="Analyze",command=analyze,corner_radius=32).grid(column=0,row=13,pady=20)

window=CTk()
window.title("LaTeX AntiPlagarism App")
set_appearance_mode('dark')
path_variable=StringVar()
path_variable.set("Selected Article:")
left_panel=Left_Panel(window,height=400,width=200).grid(column=0,rowspan=20)
left_mid_padding=CTkFrame(window,width=20,height=0,fg_color="transparent").grid(column=1,row=0)
result_label=CTkLabel(window,text="Results:").grid(column=4,row=0)
result_box=CTkTextbox(window,height=400,width=400).grid(column=4,row=1,rowspan=13,padx=20)
window.mainloop()

# make frames for left, middle, right panel