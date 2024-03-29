from tkinter import filedialog,NS,IntVar,StringVar
import datetime
from customtkinter import CTk,CTkButton,CTkLabel,CTkTextbox,CTkSwitch,CTkFrame,set_appearance_mode
import shutil,os
import antiplagarism_tools as at
import document_list_handler as dlh
from TexSoup import TexNode, TexSoup
import extractor
import webbrowser

FILEBASE_FOLDER_DIRECTORY="tex_file_base\\tex"
TEST_FOLDER_DIRECTORY="files_to_test"
HTML_REPORT_DIRECTORY="html_reports"
PLAGIAT_LEVEL_PERCENTAGES={"compare chars":{"para":[60.0,80.0],
                                            "equa":[50.0,70.0]},
                            "compare_paragraph_hashes":{"para":[60.0,80.0],
                                                        "equa":[50.0,70.0]},
                            "content hashes":{"para":[20.0,60.0],
                                                "equa":[20.0,60.0]},
                            "Levenshtein":{"para":[60.0,80.0],
                                                "equa":[60.0,70.0]},  
                            "cosine":{"para":[80.0,95.0],
                                                "equa":[80.0,95.0]},
                            "jaccard":{"para":[70.0,90.0],
                                                "equa":[80.0,95.0]}  
                                                        } # pierwsza wartość to pierwszy próg czyli średnie podejrzenie o plagiat
                                                            # druga wartość to drugi próg czyli mocne podejrzenia o plagiat, chodzi o wartość ratio
def upload_file_to_base():
    path=filedialog.askopenfilename()
    shutil.copy(path,os.getcwd()+"\\"+FILEBASE_FOLDER_DIRECTORY)

def upload_file_to_tests():
    path=filedialog.askopenfilename()
    shutil.copy(path,os.getcwd()+"\\"+TEST_FOLDER_DIRECTORY)

def select_file_to_check():
    filetypes = (
        ('LaTeX files', '*.tex'),
        ('All files', '*.*')
    )
    path=filedialog.askopenfilename(filetypes=filetypes,initialdir=os.getcwd()+"\\"+TEST_FOLDER_DIRECTORY)
    path_variable.set("Selected Article: \n"+path.split("/")[-1])
class Left_Panel(CTkFrame):
    def __init__(self, master, path_variable,report_variable,textbox, **kwargs):
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
        self.upload_test_button=CTkButton(self,text="Upload to Test Base", command=upload_file_to_tests,corner_radius=32).grid(column=0,row=1,pady=20)
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
        self.analyze_button=CTkButton(self,text="Analyze",command=lambda: self.analyze(path_variable,report_variable,textbox),corner_radius=32).grid(column=0,row=13,pady=20)
        self.report_button=CTkButton(self,text="Open Last Report",command=lambda:self.open_report(report_variable),corner_radius=32).grid(column=0,row=14,pady=20)

    def analyze(self, path_variable,report_variable,textbox):
        selected_methods=[]
        if(self.char_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_by_chars]
        if(self.phrase_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_paragraph_hashes]
        if(self.hash_method_var.get()==1):selected_methods+=[at.AntiPlagarism.test_full_content_hashes]
        if(self.formula_levenshtein_var.get()==1):selected_methods+=[at.AntiPlagarism.test_lavenshtein_distance]
        if(self.formula_cosine_var.get()==1):selected_methods+=[at.AntiPlagarism.test_cosine_distance]
        if(self.formula_jaccard_var.get()==1):selected_methods+=[at.AntiPlagarism.test_jaccard_distance]
        print("Selected methods: ", selected_methods)
        if(len(path_variable.get().split("\n"))<2):
            print("No article selected")
            return
        article_name=path_variable.get().split("\n")[1]
        tested_document = dlh.DocumentListHandler.initSoupFromTexFile("files_to_test/"+article_name)
        document_base: list(TexNode) = dlh.DocumentListHandler.init_tex_document_base("tex_file_base")
        antiPlagarism = at.AntiPlagarism(document_base)

        listdir = os.listdir(os.path.join("tex_file_base", "tex"))

        results = [*zip(listdir, *(antiPlagarism.compare_to_document_base(tested_document, method) for method in selected_methods))]

        
        raw_text_results=""
        for test_document, *result in results:
            raw_text_results+=f"{test_document}:\n"
            for r in result:
                #print(r)
                raw_text_results+=f"{r['para'].method} (paragraphs): distance: {r['para'].distance}, match_count: {len(r['para'].matched)}, ratio: {r['para'].ratio}\n" #results in raw form
                if(r['para'].ratio>PLAGIAT_LEVEL_PERCENTAGES[r['para'].method]["para"][1]):
                    raw_text_results+="High suspicions of plagarism\n"
                elif(r['para'].ratio>PLAGIAT_LEVEL_PERCENTAGES[r['para'].method]["para"][0]):
                    raw_text_results+="Medium suspicions of plagarism\n"
                raw_text_results+=f"{r['equa'].method} (equations): distance: {r['equa'].distance}, match_count: {len(r['equa'].matched)}, ratio: {r['equa'].ratio}\n" #results in raw form
                if(r['equa'].ratio>PLAGIAT_LEVEL_PERCENTAGES[r['equa'].method]["equa"][1]):
                    raw_text_results+="High suspicions of plagarism\n"
                elif(r['equa'].ratio>PLAGIAT_LEVEL_PERCENTAGES[r['equa'].method]["equa"][0]):
                    raw_text_results+="Medium suspicions of plagarism\n"
        res = {}

        for document, *result in results:
            for re in result:
                if not res.get(document):
                    res[document] = {}
                    res[document]["para"] = {}
                    res[document]["para"]["matchedBlocks"] = []
                    res[document]["para"]["reportResults"] = []
                    res[document]["equa"] = {}
                    res[document]["equa"]["matchedBlocks"] = []
                    res[document]["equa"]["reportResults"] = []

                r = re["para"]
                if len(r.matched) > 0:
                    res[document]["para"]["matchedBlocks"] += r.matched
                    res[document]["para"]["reportResults"] += [f"{document} (paragraphs) - {r.method}: distance: {r.distance}, ratio: {r.ratio}"],

                r = re["equa"]
                if len(r.matched) > 0:
                    res[document]["equa"]["matchedBlocks"] += r.matched
                    res[document]["equa"]["reportResults"] += [f"{document} - {r.method}: distance: {r.distance}, ratio: {r.ratio}"],

        dt = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
        i = 1

        template = ""
        with open("html_reports/report_template.html", "r") as f:
            template = f.read()

        title = f"report nr {i}, date: {dt}"
        totalParagraphs = ""
        totalEquations = ""
        textResultParagraph = ""
        textResultEquations = ""
        
        for k, v in res.items():
            paragraphs = ""
            results = ""

            with open(f"tex_file_base/tex/{k}", "r") as h:
                paragraphs, equations = extractor.TexExtractor.separateTextAndEquationNodes(TexSoup(h.read()))
                paragraphs = extractor.TexExtractor.nodeListToString(paragraphs)
                equations = extractor.TexExtractor.nodeListToString(equations)
                
            counter = 0
            skip = 0
            for block in v["para"]["matchedBlocks"]:
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

            skip = 0
            for block in v["equa"]["matchedBlocks"]:
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

            if not counter:
                continue

            res = "".join([f"<div>{x[0]}</div>" if x else "" for x in v["para"]["reportResults"]]) + ":" + "\n\n"
            totalParagraphs += res + paragraphs + "\n\n"
            textResultParagraph += "".join([f"{x[0]} " if x else "" for x in v["para"]["reportResults"]]) + "\n\n"

            res = "".join([f"<div>{x[0]}</div>" if x else "" for x in v["equa"]["reportResults"]]) + ":" + "\n\n"
            totalEquations += res + equations + "<hr></hr>"
            textResultEquations += "".join([f"{x[0]} " if x else "" for x in v["equa"]["reportResults"]]) + "\n\n"



        template = template.replace("{{title}}", title)
        template = template.replace("{{equations}}", totalEquations)
        template = template.replace("{{paragraphs}}", totalParagraphs)

        report_variable.set(f"html_reports/report_{dt}_{i}.html")

        with open(f"text_raw_reports/report_{dt}_{i}.txt","w+") as raw_text_report: # raw results saved to file
            raw_text_report.write(raw_text_results)

        text_results="Paragraphs:\n"+textResultParagraph + "\n" +"Equations:\n" +textResultEquations # results by Kris

        textbox.delete("0.0", "end")
        textbox.insert("0.0", raw_text_results) # textbox clear and write

        with open(f"text_reports/report_{dt}_{i}.txt", "w+") as text_report:
            text_report.write(text_results)
        
        with open(f"html_reports/report_{dt}_{i}.html", "w+") as g:
            g.write(template)
            i += 1
        print("Analysis Complete")
    
    def open_report(self,report_variable):
        if(report_variable.get()!=""):
                new = 2 # open in a new tab, if possible
                url = "file://"+os.getcwd()+"\\"+report_variable.get()
                print(url)
                webbrowser.open(url,new=new)
        else:
            print("No analysis made - no reports")
        #print out results

window=CTk()
path_variable=StringVar()
path_variable.set("Selected Article:")
report_variable=StringVar()
report_variable.set("")
print(report_variable.get())
window.title("LaTeX AntiPlagarism App")
set_appearance_mode('dark')
left_mid_padding=CTkFrame(window,width=20,height=0,fg_color="transparent").grid(column=1,row=0)
result_label=CTkLabel(window,text="Results:").grid(column=4,row=0)
result_box=CTkTextbox(window,height=400,width=400)
result_box.grid(column=4,row=1,rowspan=13,padx=20)
left_panel=Left_Panel(window,path_variable,report_variable,result_box,height=400,width=200).grid(column=0,row=0,rowspan=20)
window.mainloop()