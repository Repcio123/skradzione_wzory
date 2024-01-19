from tkinter import filedialog,NS,IntVar,StringVar
import datetime
from customtkinter import CTk,CTkButton,CTkLabel,CTkTextbox,CTkSwitch,CTkFrame,set_appearance_mode
import shutil,os
import antiplagarism_tools as at
import document_list_handler as dlh
from TexSoup import TexNode, TexSoup
import extractor

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
    document_base: list(TexNode) = dlh.DocumentListHandler.init_tex_document_base("tex_file_base")
    antiPlagarism = at.AntiPlagarism(document_base)

    listdir = os.listdir(os.path.join("tex_file_base", "tex"))

    results = [*zip(listdir, *(antiPlagarism.compare_to_document_base(tested_document, method) for method in selected_methods))]

    res = {}

    for document, *result in results:
        for r in result:
            if len(r.matched) > 0:
                if not res.get(document):
                    res[document] = {}
                    res[document]["matchedBlocks"] = []
                    res[document]["reportResults"] = []
                res[document]["matchedBlocks"] += r.matched
                res[document]["reportResults"] += [f"{document} - {r.method}: distance: {r.distance}, ratio: {r.ratio}"],


    dt = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    i = 1

    template = ""
    with open("html_reports/report_template.html", "r") as f:
        template = f.read()

    title = f"report nr {i}, date: {dt}"
    totalContent = ""
    
    for k, v in res.items():
        paragraphs = ""
        results = ""

        with open(f"tex_file_base/tex/{k}", "r") as h:
            paragraphs, equations = extractor.TexExtractor.separateTextAndEquationNodes(TexSoup(h.read()))
            paragraphs = extractor.TexExtractor.nodeListToString(paragraphs)
            equations = extractor.TexExtractor.nodeListToString(equations)
            
        counter = 0
        skip = 0
        for block in v["matchedBlocks"]:
            if block and len(block):
                considered = paragraphs[skip:]
                found = considered.find(block)
                newSkip = skip + found
                if found != -1 and len(block) > 2:
                    newBlock = f"<span class=\"match\">{block}</span>"
                    considered = considered.replace(block, newBlock, 1)
                    newSkip = skip + found + len(newBlock)
                    counter += 1
                paragraphs = paragraphs[:skip] + considered
                skip = newSkip
                # elif equations.find(block) != -1:
                #     equations = equations.replace(block, f"<span class=\"match\">{block}</span>", 1)
                #     counter += 1
        skip = 0
        for block in v["matchedBlocks"]:
            if block and len(block):
                considered = equations[skip:]
                found = considered.find(block)
                newSkip = skip
                if found != -1 and len(block) > 2:
                    newBlock = f"<span class=\"match\">{block}</span>"
                    considered = considered.replace(block, newBlock, 1)
                    newSkip = skip + found + len(newBlock)
                    counter += 1
                equations = equations[:skip] + considered
                skip = newSkip
                # elif equations.find(block) != -1:
                #     equations = equations.replace(block, f"<span class=\"match\">{block}</span>", 1)
                #     counter += 1
        if not counter:
            continue
        res = "".join([f"<div>{x[0]}</div>" if x else "" for x in v["reportResults"]]) + ":" + "\n\n"
        totalContent += res + paragraphs + equations + "<hr></hr>"


    template = template.replace("{{title}}", title)
    template = template.replace("{{paragraphs}}", totalContent)

    with open(f"html_reports/report_{dt}_{i}.html", "w+") as g:
        g.write(template)
        i += 1

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
phrase_method_checkbox=CTkSwitch(window,text="By paragraphs",variable=phrase_method_var)
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