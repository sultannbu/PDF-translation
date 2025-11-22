import customtkinter as ctk
from tkinter import filedialog
import threading
import time
from pathlib import Path
import ctypes
import json,math
#import mtrgm
import tkinter as tk
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image,ImageDraw
import translte

class main(): 
    global data
    file = Path(__file__).parent
    json_data = file / "config.json"
    with open(rf"{json_data}","r", encoding="utf-8") as datah:
        data = json.load(datah)

    hover_color="#25883E"
    fg_color="#0D852B"
    font = ("Arial", 12, "bold")


    # The Main
    def __init__(self):
        self.file1 = Path(__file__).parent
        self.status =0 
        self.value= 0
        self.clear_files()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.frame = ctk.CTk()
        self.frame.geometry("680x350")
        self.frame.title("مترجمي")
        self.frame.resizable(False,False)
        icon =tk.PhotoImage(file =self.file1/ "lib\photo\pdf.png")
        self.frame.iconphoto(True,icon)
        self.frame.iconbitmap( rf"{self.file1}\lib\photo\pdf.ico")
        buttun_file = ctk.CTkButton(self.frame,text="اختر الملف" ,command=self.select_file, font=self.font, fg_color=data["fg_color"], hover_color=data["hover_color"])
        buttun_file.place(x=180,y=10)
        
        buttun_filea = ctk.CTkButton(self.frame,text=" أضغط هنا للتكبير " ,width=20,command=self.zoom, font=self.font, fg_color=data["fg_color"], hover_color=data["hover_color"])
        buttun_filea.place(x=200,y=250)
        
        self.label_file = ctk.CTkLabel(self.frame,text="",font=self.font)
        self.label_file.place(x=180,y=40)

        
        self.label_Page = ctk.CTkLabel(self.frame,text="",font=self.font)
        self.label_Page.place(x=50,y=300)
        
        
        self.bar_f= ctk.CTkFrame(self.frame,corner_radius=10  )
        self.bar_f.place(x=150,y= 300 )
        self.bar= ctk.CTkProgressBar(self.bar_f,width=250)
        self.lab= ctk.CTkLabel(self.bar_f,width=20,text=f" %   {int(data['bar']*100)}    :التقدم  ",font=self.font)
        self.lab.pack()
        self.bar.pack()
        self.bar.set(0.00)


        ### frame before and after

        before= ctk.CTkFrame(self.frame,corner_radius=10  )
        before.place(x=300,y= 80 )
        ctk.CTkLabel(before,text="قبل",font=self.font).pack()
        photo = ctk.CTkImage(Image.open(r"C:\Users\MST\Desktop\projects\translte\pdf.png"),size=(150,150))
        self.before = ctk.CTkLabel(before,image=photo,text="")
        self.before.pack(pady=20)




        after= ctk.CTkFrame(self.frame,corner_radius=10  )
        after.place(x=40,y= 80)
        ctk.CTkLabel(after,text="بعد",font=self.font).pack()
        photo = ctk.CTkImage(Image.open(r"C:\Users\MST\Desktop\projects\translte\pdf.png"),size=(150,150))
        self.after =ctk.CTkLabel(after,image=photo,font=self.font,text="")
        self.after.pack(pady=20)


        ######








        # تعيين الأيقونة في شريط المهام (Windows)
        myappid = 'MyCompany.MyTranslator.1.0'  # اسم تعريفي للتطبيق
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)





        frame_but= ctk.CTkFrame(self.frame,corner_radius=10)
        frame_but.place(x=500,y= 20)
        label_run = ctk.CTkLabel(frame_but,text="التشغيل", font=self.font)
        label_run.pack()
        self.buttun_run = ctk.CTkButton(frame_but,text="تشغيل",command=self.run , font=self.font, fg_color=data["fg_color"], hover_color=data["hover_color"])
        self.buttun_run.pack()
        #
        ###
        
        buttun_infromition = ctk.CTkButton(self.frame,text="التعليمات",command=self.infromation , font=self.font, fg_color=data["fg_color"], hover_color=data["hover_color"])
        buttun_infromition.place(x=500,y= 270)
        
        buttun_setting = ctk.CTkButton(self.frame,text="الأعدادات",command=self.Setting , font=self.font, fg_color=data["fg_color"], hover_color=data["hover_color"])
        buttun_setting.place(x=500,y= 305)
        ######
        ########################### الاختيارات
        frame_menu= ctk.CTkFrame(self.frame,corner_radius=10)
        frame_menu.place(x=500,y= 90)




        label_but = ctk.CTkLabel(frame_menu,text=" لغة الملف", font=self.font)
        label_but.grid(row=0,column=0)
        global lang
        self.lang = ctk.CTkOptionMenu(frame_menu,values=list(data["lang"].keys()), font=self.font, fg_color=data["fg_color"])
        self.lang.grid(row=1,column=0)
        self.lang.configure(command=self.update_defulte)


        label_but = ctk.CTkLabel(frame_menu,text=" نوع الكتاب", font=self.font)
        label_but.grid(row=2,column=0)
        global type1
        self.type1 = ctk.CTkOptionMenu(frame_menu,values=list(data["type"].keys()) , font=self.font, fg_color=self.fg_color)
        self.type1.grid(row=3,column=0)
        self.type1.configure(command=self.update_defulte)



        label_but = ctk.CTkLabel(frame_menu,text="المترجم", font=self.font)
        label_but.grid(row=4,column=0)
        self.translter = ctk.CTkOptionMenu(frame_menu,values=list(data["translter"].keys()), font=self.font, fg_color=data["fg_color"])
        self.translter.grid(row=5,column=0)
        self.translter.configure(command=self.update_defulte)
        value=0

        ######
        
        self.frame.mainloop()
 
        







    def update_defulte(self,p):
        data["defult"]["translter"] = self.translter.get()
        data["defult"]["type"] = self.type1.get()
        data["defult"]["lang"] = self.lang.get()
        with open(rf"{self.json_data}", "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)




 



    def clear_files(self):
        data["target_file"]= "" 
        data["target_path"]= ""
        data["bar"]= 0.0
        if data["path"] == "":
            data["path"]= rf"{self.file}\tesseract\tesseract.exe"


        self.clear_json(data)
    
    def infromition(self):
        pass
    def select_file(self):
        if self.status == 1:
            self.wrong("اطفى عملية الترجمة اولاً")
            return
        f = filedialog.askopenfilename(title="اختر ملف الPdf",filetypes=[("Only PDF","*.pdf")])
     #   print(f)           
        name=f.split("/",99)[-1]
        path = f
      #  print(f"""
       #     name file is {name}  and path is {path}""")
        data["target_file"]= name 
        data["target_path"]= path
        if path != "":
            self.label_file.configure(text=f"{name} اسم الملف المترجم ")
        else:
            self.label_file.configure(text=f"")
        
        
        
        self.update_file()
        
    def update_file(self):
        with open(rf"{self.json_data}", "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)
    def run(self):
        if data["target_path"] == "":
            self.wrong("لم تختر اي ملف للترجمة ")
            return 
        a = self.check_lang(data["lang"][data["defult"]["lang"]])
        if a == 0:
            self.wrong("  لغة الترجمة غير متوفره يرجى تحميلها او مراجعة التعليمات   ")
            return
        if self.status == 0:
            self.status= 1
            data["status"] = 1
            self.clear_json(data)
            self.buttun_run.configure(text="إيقاف عملية الترجمة")
            
            self.run2 =threading.Thread(target=translte.main)
            self.run2.start()

        #   self.run2.join()
            
            self.bar_f.after(3000,self.update_bar)

        elif self.status == 1:
            
            data["status"] = 0
            self.buttun_run.configure(text="تشغيل")
            self.status= 0
            self.clear_json(data)




    def zoom(self):
        self.status_zoom = 1
        self.zoom_frame = ctk.CTkToplevel(self.frame)   
        self.zoom_frame.title("الصور مكبره") 
        self.zoom_frame.geometry("1100x600")
      #  self.zoom_frame.grab_set()
       # self.zoom_frame.overrideredirect(True)
       
       
       
        path_after = self.file / f"lib/photo/after.png"
        path_before =  self.file / f"lib/photo/before.png"
        path_loding =  self.file / f"lib/photo/loading.png"
             
        
        before= ctk.CTkFrame(self.zoom_frame,corner_radius=10  )
        before.place(x=550,y= 20 )
        ctk.CTkLabel(before,text="قبل",font=self.font).pack()
        photo = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(500,500)) 
        self.before_zoom = ctk.CTkLabel(before,image=photo,text="")
        self.before_zoom.pack(pady=0)



        after= ctk.CTkFrame(self.zoom_frame,corner_radius=10  )
        after.place(x=10,y= 20)
        ctk.CTkLabel(after,text="بعد",font=self.font).pack()
        photo = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(500,500)) 
        self.after_zoom =ctk.CTkLabel(after,image=photo,font=self.font,text="")
        self.after_zoom.pack(pady=0)

        
        
    def infromation(self):
        infromation = ctk.CTkToplevel(self.frame)   
        infromation.title("التعليمات") 
        infromation.geometry("600x500")
      #  self.zoom_frame.grab_set()
       # self.zoom_frame.overrideredirect(True)
        text="""
               
برنامج "مترجمي"

مترجمي هو برنامج مصمم لترجمة الكتب القديمة المصوّرة باستخدام الذكاء الاصطناعي  يقوم البرنامج بتحويل صفحات ال PDF إلى صور
ثم استخراج النصوص منها
وبعدها ترجمتها بدقة عالية للحصول على أفضل نتيجة ممكنة.
____________________________________________________________________________


"كيفية ترجمة كتاب"

اتبع الخطوات التالية لترجمة أي كتاب بصيغة PDF بسهولة:

اضغط على "اختر الملف" وحدد الكتاب المطلوب ترجمته.
اختر لغة الكتاب الأصلية حسب محتواه.
اختر نوع الكتاب (علمي أو أدبي).
اختر المترجم المناسب (قوقل – الذكاء الاصطناعي – ديب سيك).
اضغط زر "تشغيل"، وستجد الملف المترجَم في مجلد output.

____________________________________________________________________________

"نوع الكتاب"
الكتب تختلف في أسلوبها ومحتواها، ولهذا يتيح البرنامج خيارين:
الكتب العلمية:
تحتوي عادةً على معادلات ورموز هندسية أو تقنية.
يتجاهل البرنامج ترجمة المعادلات للحصول على نتائج أدق.

الكتب الأدبية:
يترجم البرنامج كل ما يظهر في الصفحة دون استثناء.
____________________________________________________________________________

"من هم المترجمين "
يوفر البرنامج ثلاثة خيارات للترجمة:
قوقل (مجاني)
OpenAI (مدفوع – يحتاج مفتاح )
DeepSeek (مدفوع – يحتاج مفتاح )

نصيحة:
للكتب الأدبية يفضل استخدام قوقل لأنه مجاني.
للكتب العلمية يفضل استخدام الذكاء الاصطناعي للحصول على دقة أعلى.

"ماذا تعني جودة الحفظ ودقة الصورة (DPI)"
مقياس لرفع الدقة
رفع الدقة يساعد المحرك على اكتشاف النصوص بشكل أفضل، خصوصاً في الكتب القديمة أو الصفحات ذات الطباعة الضعيفة.

افضل الخيارات هي:،

عند معالجة كتب واضحه يفضل وضعها ثلاث مئة

وعند الكتب الغير واضحة ويصعب قرائتها توضع اكثر من ثلاث مئة

رفع  DPI يزيد حجم الملف بشكل كبير،
،
لذلك تمت إضافة خيار جودة الحفظ لتقليل الحجم عند رفع الدقة.
يفضل ضبط الجودة على اربعين بالمئة عند معالجة الكتب القديمة.
____________________________________________________________________________

"كيف أحصل على ملفات الترجمة (اللغات)"

بسبب حجم ملفات اللغات الكبير، لم يتم تضمينها داخل البرنامج.
يمكنك تنزيل اللغة المطلوبة من رابط GitHub ثم وضعها داخل المسار:

tesseract/tessdata

بعدها أعد تشغيل البرنامج وسيتم تفعيل اللغة مباشرة.
____________________________________________________________________________

ما معنى "حساسية الجملة"
هي ميزة مخصّصة لمنع ظهور الجمل غير المفهومة أو الممتلئة بالرموز الغريبة.
 عند ضبط الحساسية على ثلاثين يقوم البرنامج

بحذف أي جملة تحتوي على أكثر من "ثلاثين" رموز غير عربية أو نصوص مشوهة.
الهدف هو تحسين دقة الترجمة النهائية وجعلها أكثر وضوحاً."""
        box = ctk.CTkTextbox(infromation,width=600,height=500)
        box.pack(fill="both", expand=True)
        box.tag_config("right", justify="right")
        box.insert("1.0",get_display(arabic_reshaper.reshape(text)), "right")
        box.configure(font =self.font,state="disabled")
    def wrong(self,text):
    
     #   print(self.frame.winfo_x())
        self.wrong_frame = ctk.CTkToplevel(self.frame)   
        self.wrong_frame.title("خطأ") 
        self.wrong_frame.geometry("300x50")
        self.wrong_frame.grab_set()
        self.wrong_frame.overrideredirect(True)
        self.wrong_frame.update_idletasks()
        x = self.frame.winfo_x() + (self.frame.winfo_width() - self.wrong_frame.winfo_width()) // 2
        y = self.frame.winfo_y() + (self.frame.winfo_height() - self.wrong_frame.winfo_height()) // 2
        self.wrong_frame.geometry(f"+{x}+{y}")
        self.wrong_frame.resizable(False,False)
        self.wrong_frame.anchor("center")
        self.wrong_frame.iconbitmap( rf"{self.file1}\lib\photo\pdf.ico")
        label = ctk.CTkLabel(self.wrong_frame,text=text,font=self.font).pack()
        self.wrong_frame.after(1000,self.wrong_frame.destroy)






    def clear_json(self,data2):
        with open(rf"{self.json_data}", "w", encoding="utf-8") as data_file:
            json.dump(data2, data_file, ensure_ascii=False, indent=4)
    def check_lang(self,lang):
        path = data['path'].split("\\")[:-1]
        path = "\\".join(path)
        path = f"{path}\\tessdata\\{lang}.traineddata"
      #  print(path)
        try:
            with open(path,"r")as a:
                return 1
            
        except:
            return 0
    def update_Setting(self):
        # تحديث القيم في data من الخيارات اللي اختارها المستخدم
     #   data["defult"]["texter"] = self.texter.get()
        self.buttun_save.configure(text="تم الحفظ بنجاح")
        data["defult"]["translter"] = self.translter.get()
        data["defult"]["lang"] = self.lang.get()
        data["defult"]["type"] = self.type1.get()
        data["defult"]["quality"] = self.qualitys.get()
        data["defult"]["keys"]["openai"] = self.input_key_openai.get()      # حفظ مفتاح OpenAI
        data["defult"]["keys"]["deepseek"] = self.input_Deeb_Seek.get() # حفظ مفتاح DeebSeek
        data["defult"]["DPI"] = self.DPI.get()
        data['path']=self.de_path.get()
        t = round(self.alletgy_sentence.get())
        t = int(t)
        data["defult"]["alletgy_sentence"]= t
        #self.Setting.after(2000, self.buttun_save.configure(text="تم الحفظ بنجاح"))

        # حفظ البيانات في الملف
        with open(rf"{self.json_data}", "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)

    def Setting(self):
        self.Setting = ctk.CTkToplevel(self.frame)   
        self.Setting.title("الأعدادات") 
        self.Setting.geometry("680x350")
        self.Setting.grab_set()
        self.Setting.resizable(False,False)
        self.Setting.wm_iconbitmap( rf"{self.file1}\lib\photo\pdf.ico")
        
        frame_menu1= ctk.CTkFrame(self.Setting,corner_radius=10)
        frame_menu1.place(x=10,y= 20)
        ctk.CTkLabel(frame_menu1,text="الفلترة",font=self.font).pack()
        
        filter_text = ctk.CTkLabel(frame_menu1,text="حساسية الجملة",font=self.font)
        filter_text.pack()

        self.alletgy_sentence = ctk.CTkSlider(frame_menu1,from_=0,to=100,command= self.update_allergy)
        self.alletgy_sentence.pack()
        self.alletgy_sentence.set(data["defult"]["alletgy_sentence"])
        self.allergy = ctk.CTkLabel(frame_menu1,text=f"الحساسية : {self.alletgy_sentence.get()}",font=self.font)
        self.allergy.pack()
        
        #label = ctk.CTkLabel(frame_menu1,text="حساسية الأحرف ",font=self.font).pack()
        #scroll_filter = ctk.CTkSlider(frame_menu1,from_=0,to=100,orientation="horizontal")
        #scroll_filter.pack()


        frame_menu= ctk.CTkFrame(self.Setting,corner_radius=10)
        frame_menu.place(x=250,y= 20)
        ctk.CTkLabel(frame_menu,text="المترجمين",font=self.font).pack()
        label = ctk.CTkLabel(frame_menu,text="Open Ai مفتاح",font=self.font)
        label.pack()
        global input_key_openai
        var = ctk.StringVar(value=data["defult"]["keys"]["openai"])
        self.input_key_openai = ctk.CTkEntry(frame_menu,width=230,justify="right",textvariable=var)
        self.input_key_openai.pack()
 
        
        label = ctk.CTkLabel(frame_menu,text="مفتاح Deeb Seek",font=self.font)
        label.pack()
        
        
        var = ctk.StringVar(value=data["defult"]["keys"]["deepseek"])
        global input_Deeb_Seek
        self.input_Deeb_Seek = ctk.CTkEntry(frame_menu,width=230,justify="right",textvariable=var)
        self.input_Deeb_Seek.pack()
        
    
        label = ctk.CTkLabel(frame_menu,text="مسار pytesseract",font=self.font)
        label.pack()
        global de_path
        self.path_var = ctk.StringVar(value=data["path"])
        self.de_path = ctk.CTkEntry(frame_menu,width=230,justify="right",textvariable=self.path_var)
        self.de_path.pack()
        self.de_path.configure(textvariable = self.path_var)
        
        frame_menu= ctk.CTkFrame(self.Setting,corner_radius=10)
        frame_menu.place(x=500,y= 20)
        ctk.CTkLabel(frame_menu,text="النصوص والصور",font=self.font).pack()
        label_but = ctk.CTkLabel(frame_menu,text=" جودة الحفظ", font=self.font)
        label_but.pack()
        global qualitys
        self.qualitys = ctk.CTkOptionMenu(frame_menu,values=list(data["quality"].keys()) , font=self.font, fg_color=self.fg_color)
        self.qualitys.pack()
        self.qualitys.set(data["defult"]["quality"])

        
        ctk.CTkLabel(frame_menu,text="(DPI) زيادة دقة الصورة",font=self.font).pack()
        global DPI
        self.DPI = ctk.CTkOptionMenu(frame_menu,values=list(data["DPI"].keys()) , font=self.font, fg_color=self.fg_color)
        self.DPI.pack()
        self.DPI.set(data["defult"]["DPI"])
        
        
        
        
        #ctk.CTkLabel(frame_menu,text=" لون النص والخلفية", font=self.font).pack()


       # self.texter = ctk.CTkOptionMenu(frame_menu,values=list(data["texter"].keys()) , font=self.font, fg_color=self.fg_color)
      #  self.texter.pack()
     #   self.texter.set(data["defult"]["texter"])
        
        
        
        self.buttun_save = ctk.CTkButton(self.Setting,command=self.update_Setting,text="حفظ",font=self.font, fg_color=self.fg_color, hover_color=data["hover_color"])
        self.buttun_save.place(x = 300,y=320)


    def update_allergy(self ,t):
        t = round(t)
        t = int(t)
        self.allergy.configure(text=f"الحساسية : {t}")











    def t():
    # label_but.grid_forget()
        pass
    #menu_lang.after(4000, t)
    def update_bar(self):
        try:
        #    print("!1")
            with open(rf"{self.json_data}","r", encoding="utf-8") as datah:
                dataa = json.load(datah)

            self.lab.configure(text=f" %   {int(dataa['bar']*100)}    :التقدم  ")
            self.bar.set(dataa['bar'])
            
            
            path_after = self.file / f"lib/photo/after.png"
            path_before =  self.file / f"lib/photo/before.png"
            path_loding =  self.file / f"lib/photo/loading.png"
            try:
                photo_after = ctk.CTkImage(Image.open(rf"{path_after}"),size=(150,150)) 
                self.after.configure(image=photo_after)
            except:
                photo_after = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(150,150)) 
                self.after.configure(image=photo_after)
            
            
            try:
                photo_before = ctk.CTkImage(Image.open(rf"{path_before}"),size=(150,150)) 
                self.before.configure(image=photo_before)
            except:
                photo_before = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(150,150)) 
                self.before.configure(image=photo_before)
            
            try:
                status_frame =self.zoom_frame.winfo_exists()
            except:
                status_frame =False
            
            if status_frame:
                try:
                    
                        
                    photo_after = ctk.CTkImage(Image.open(rf"{path_after}"),size=(500,500)) 
                    self.after_zoom.configure(image=photo_after)
                        
                    photo_before = ctk.CTkImage(Image.open(rf"{path_before}"),size=(500,500)) 
                    self.before_zoom.configure(image=photo_before)
                    
                except:
                    try:
                        photo_after = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(500,500)) 
                        self.after_zoom.configure(image=photo_after)
                            
                        photo_before = ctk.CTkImage(Image.open(rf"{path_loding}"),size=(500,500)) 
                        self.before_zoom.configure(image=photo_before)
                    except:
                        pass
                    
                
                
            self.label_Page.configure(text=f"الصفحات \n {dataa['page_now']} / {dataa['all_page']}")
            if dataa["status"] ==0:
                self.lab.configure(text=f" %   {int(dataa['bar']*100)}    :اكتملت عملية الترجمة بنجاح.  ")
            if self.status == 1:
                self.bar_f.after(3000,self.update_bar)
        except Exception as r:
            print(str(r))

    def update_settings1(self):

        self.value += 0.01
        if self.value > 1.0:
            self.value = 0.0  # ارجع للصفر بعد اكتمال الشريط
        self.bar.set(self.value)  # تحديث شريط التقدم
        self.lab.configure(text=f" %   {int(self.bar.get()*100)}    :التقدم  ")

        # استدعاء نفسه بعد 1000 ملي ثانية (1 ثانية)
        self.frame.after(100, self.update_settings1)
































































if __name__ == "__main__":
    app = main()






















