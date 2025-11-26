from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import pytesseract 
from pytesseract import Output
from deep_translator import GoogleTranslator
import arabic_reshaper
# from bidi.algorithm import get_display # REMOVED: Obsolete package
import cv2
from collections import Counter
import fitz
import img2pdf
from pathlib import Path
#import translators as ts
from openai import OpenAI
import numpy as np
import json,time
global data
file = Path(__file__).parent

tester= """
أنت مترجم عالمي محترف. يمكنك التعرف على جميع اللغات وترجمتها إلى العربية.

مهمتك:
1. ترجم النص إلى العربية حتى لو كان:
   - مكتوب بلغة غير الإنجليزية.
   - يحتوي أخطاء إملائية أو نحوية.
   - يحتوي كلمات ناقصة.
   - مكتوب بخليط لغات أو لهجة.
   - مكتوب بشكل سيء لكنه ما زال يحتوي كلمات يمكن فهمها.

2. إذا كانت الكلمات أو الجُمل قابلة للتخمين أو تحتوي أجزاء مفهومة → ترجمها.

3. لا ترجع (0) إلا في حالة واحدة فقط:
   - إذا كان النص عبارة عن رموز عشوائية، أو حروف بلا معنى، أو نص مشوّه بالكامل وغير قابل للفهم بأي شكل.

4. لا تشرح، لا تقدّم ملاحظات، لا تضيف أي شيء.
   الناتج يجب أن يكون:
   - ترجمة عربية فقط.
   - أو الرقم (0) فقط في حال كان النص غير قابل للفهم.

التزم بهذه القواعد بدقة.


"""






def main():
    global data_config,data_json
    data_json = file / "config.json"

    with open(rf"{data_json}","r", encoding="utf-8") as dataa:
        data_config = json.load(dataa)
#    print(f"link {file} \n \n \n \n")
    pass
    file_output = data_config["target_file"].split(".",2)[0]
    file_output = f"{file_output}_output.pdf"
    pytesseract.pytesseract.tesseract_cmd =  data_config['path']
   # trans = Translator()
    pdf = fitz.open(fr"{data_config['target_path']}")
    images_pdf = []
    
    c = len(pdf)
    
    for ia in range(c):

            
        print(f" {ia} / {c}")
      #  print("start in pdf"+str(ia))

       # print(pytesseract.get_languages(config=''))
        data_image = pdf[ia].get_image_info()
        x,h,width,hieght = data_image[0]["bbox"][0],data_image[0]["bbox"][1],data_image[0]["bbox"][2],data_image[0]["bbox"][3]
            
        page = pdf.load_page(ia)
        DPI_value = int(data_config["DPI"][data_config["defult"]["DPI"]])
        pix = page.get_pixmap(dpi=DPI_value)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.convert("RGB")
        img = img.filter(ImageFilter.MedianFilter(size=3))
        img = ImageOps.autocontrast(img) 
        #intw = int(width)
       # inth = int(hieght)
        quality = data_config["quality"][data_config["defult"]["quality"]]
        img_cv = np.array(img)
     #   img = img.
        image = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        _, thresh = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY_INV)
        blur = cv2.GaussianBlur(thresh,(5,5),0)

        img.save(rf"{file}\lib\photo\before.png")
        data = pytesseract.image_to_data(thresh, output_type=Output.DICT,config=data_config["config"],lang=data_config['lang'][data_config["defult"]["lang"]])
        ig =ImageDraw.Draw(img)
        new={}
        for i in range(len(data["text"])):
            if data["text"][i].split():
                add={
                    "text":data["text"][i],
                    "left":data["left"][i],
                    "top":data["top"][i],
                    "width":data["width"][i],
                    "height":data["height"][i],   
                    "conf":data["conf"][i], 
                }
                new.setdefault(data["block_num"][i],[]).append(add)
        #print(new)
        for i in new:

            gmlh=""
            coordinates= {
                "min_left":9999999999999999,
                "min_top":9999999999999999,
                "min_width":9999999999999999,
                "min_height":9999999999999999,
                "max_left":0,
                "max_top":0,
                "max_width":0,
                "max_height":0,
                "conf":0,
            }
            for s in new[i]:
                coordinates["min_left"] = min(coordinates["min_left"],(s["left"]))
                coordinates["min_top"] = min(coordinates["min_top"],(s["top"]))
                coordinates["min_width"] = min(coordinates["min_width"],s["width"])
                coordinates["min_height"] = min(coordinates["min_height"],s["height"])
                coordinates["max_left"] = max(coordinates["max_left"],(s["left"]+s["width"]))
                coordinates["max_top"] = max(coordinates["max_top"],(s["top"]))
                coordinates["max_width"] = max(coordinates["max_width"],s["width"])
                coordinates["max_height"] = max(coordinates["max_height"],s["height"])
                coordinates["conf"] = max(coordinates["conf"],s["conf"])
                gmlh += s["text"]+ " "
            
            coor_top=coordinates["min_top"]
            #print(gmlh)
            type_translete = data_config['translter'][data_config['defult']['translter']]
            text_arabic1 = transleter(type_translete,gmlh)
            MAX_X=coordinates["max_left"]
            MIN_X=coordinates["min_left"]
            MAX_Y=coordinates["max_top"]
            MIN_Y=coordinates["min_top"]
            MAX_W=coordinates["max_width"]
            MIN_W=coordinates["min_width"]
            MAX_H=coordinates["max_height"]
            MIN_H=coordinates["min_height"]
            CONF=coordinates["conf"]
            try:
                text_arabic1= " ".join(text_arabic1.split())
            except:
                text_arabic1=0
                
            # FIX: Use arabic_reshaper directly
            text0=arabic_reshaper.reshape(text_arabic1)

       #     print(f"""
               # ______________________________________
               # block is :{i}
               # text:{text0}
               # min_left:{MIN_X}
               # max_left:{MAX_X}
                
               # min_top:{MIN_Y}
              #  max_top:{MAX_Y}
                
             #   min_width:{MIN_W}
            #    max_width:{MAX_W}
                
           #     min_height:{MIN_H}
          #      max_height:{MAX_H}

                
         #       conf:{CONF}
          #      ____________________________________
        #        """)
            block = {"MAX_X":MAX_X,"MIN_X":MIN_X,"MIN_Y":MIN_Y,"MAX_Y":MAX_Y,"MIN_W":MIN_W,"MAX_W":MAX_W,"MIN_H":MIN_H,"MAX_H":MAX_H,"text":text0}
            
            background,color_text =0,0
            if CONF > 80 and text0 != "1" :
                good_size = get_good_size_text(text0,block)
                if data_config["type"][data_config["defult"]["type"]] == 1:
                    status_Filter = Filter(text=text0,block=block,font_size=good_size)
                else:
                    status_Filter = True
                    
                    
                font = ImageFont.truetype("arial.ttf",good_size)
                status_block = 0
                if (MAX_Y< 120):

                        #ig.rectangle([(coordinates["min_left"],coordinates["min_top"]),(coordinates["max_left"]+(coordinates["min_width"])),(coordinates["max_top"]+coordinates["max_height"])],fill=color_background)
                        status_block = 0
                else:
                
                    if text0 != "0" and status_Filter == True:
                            get_colors = img.crop((MIN_X,MIN_Y,MAX_X,MAX_Y+MAX_H))
                    #     get_colors.show()
                            co = img.quantize(colors=2,method=2).getpalette()
                            background,color_text = tuple(co[:3]),tuple(co[3:6])
                           # color_background = img.getpixel((coordinates["min_left"],coordinates["max_top"]))
                           # get_colors = get_colors.getcolors(get_colors.size[0]*get_colors.size[1])
                           # get_colors=Counter(get_colors)
                           # get_colors = list(get_colors.most_common(10))
                           # print(get_colors)
                           # background = get_colors[0][0][1]
                          # color_text = get_contrast_color(background)
                            #print(f"color_text : {color_text} background :{background}")
                            ig.rectangle([(MIN_X,MIN_Y),(MAX_X),(MAX_Y+MAX_H)],fill=background)
                            status_block = 1
            ###################################################
            # هذا المربع يختص في ترتيب الكلام وكتابته على الصورة
            #   
                length_text_last=0
                coor = MAX_X
                for text in text0.split(" ")[::-1]:
                        if status_block == 1:
                            text_arabic= "".join(text.split())
                            length_text = font.getlength(text_arabic) 
                            if coor <= (MIN_X+(length_text*0.9)):
                                coor_top = (coor_top + MAX_H +MIN_H)
                                coor = MAX_X-length_text
                                length_text_last = length_text
                            else:
                                coor  = coor - length_text  - (length_text_last /4)
                                length_text_last = length_text
                            ig.text((coor,coor_top),text=text,fill=color_text,font=font)
                img.save(rf"{file}\lib\photo\after.png")
     #   img.thumbnail((intw,inth))
        img.save(rf"{file}\lib\photo\last_translete.jpg",subsampling=0,optimize=True,quality=quality)
            
        #print("start operation2"+str(i))
        ii = (ia+1)
        bar = ii / c
        st= check_prossecr()
        if st == 0:
            break
        if ii == c:
            data_config["status"] = 0

        update_json(bar,ii,c,data_config["status"])
        if ia == 0:
                file_pdf = fitz.open()
                
                newpage = file_pdf.new_page(width = img.width,height=img.height)
                rect_image = fitz.Rect(0,0,img.width,img.height)
                newpage.insert_image(rect_image,filename=rf"{file}\lib\photo\last_translete.jpg")
                file_pdf.save(rf"{file}\output\{file_output}")

        else:
                file_pdf = fitz.open(rf"{file}\output\{file_output}")
                newpage = file_pdf.new_page(width = img.width,height=img.height)
                rect_image = fitz.Rect(0,0,img.width,img.height)
                newpage.insert_image(rect_image,filename=rf"{file}\lib\photo\last_translete.jpg")
                file_pdf.saveIncr()
                file_pdf.close()
                
       


def isEngilsh(word):
    w = [",",".","(",")","_",";","%","$","#","!",'"',"'"]
    for i in w:
        if i in word:
            return False
    return word.isascii()

def get_contrast_color(rgb_bg):
    r, g, b = rgb_bg
    # صيغة YIQ لتحديد السطوع
    yiq = (r*299 + g*587 + b*114) / 1000
    return (0,0,0) if yiq > 128 else (255,255,255)

def check_high(block):
    coor_top=block["MIN_Y"]
    coor = block["MAX_X"]
    length_text_last=0
    size_words = 0
    count_words_engilsh= 0
    for text in block["text"].split(" "):
        font = ImageFont.truetype("arial.ttf",block["MAX_H"])
        text_arabic= "".join(text.split())
        
        length_text = font.getlength(text_arabic) 
        if isEngilsh(text_arabic) == True:
            count_words_engilsh+=1
            
        size_words+= length_text

        if coor <= (block["MIN_X"]+(length_text*0.9)):
                                        
            coor_top = (coor_top + block["MAX_H"] +block["MIN_H"])
                
            coor = block["MAX_X"]-length_text
            length_text_last=length_text
        else:
            coor  = coor - length_text  - (length_text_last /4)
            length_text_last = length_text


    return (coor_top),size_words,count_words_engilsh


def check_count_words(text):
    count = 0
    for _ in text.split(" "):
        count+=1
    return count

def Filter(text,block,font_size):
    global data_config,data_json
    count_words = check_count_words(text=text)
    filter_high,size_words,count_words_engilsh = check_high(block=block)    
 #   filter_high= filter_high / count_words
    width = block["MAX_Y"] - block["MIN_Y"]
    width = width* 0.8
    allergy = data_config['defult']['alletgy_sentence'] * 0.01
    #print(f" words: {count_words/3}  engilsh: {count_words_engilsh}")
    #print("filter_high:"+str(filter_high))
    if (count_words/allergy) < count_words_engilsh:      
        return False
    if width >= size_words:
        return False
    if  ((block["MAX_Y"]-block["MIN_Y"]) *0.3)  > (filter_high-block["MIN_Y"]):
        return False
   # if font_size > 30 and filter_high> 100 or count_words > 10:
    #    return False
    
    return True
def get_good_size_text(text_arabic,block):
    size = block["MAX_H"]
    for X in range(3):
        length_text_last=0
        coor_top=block["MIN_Y"]
        coor = block["MAX_X"]
        for text in text_arabic.split(" "):
            font = ImageFont.truetype("arial.ttf",size)

            text_arabic= "".join(text.split())
            length_text = font.getlength(text_arabic) 
            if coor <= (block["MIN_X"]+(length_text*0.9)):
                                        
                coor_top = (coor_top + block["MAX_H"] +block["MIN_H"])
                coor = block["MAX_X"]-length_text
                length_text_last=length_text
            else:
                coor  = coor - length_text  - (length_text_last /4)
                length_text_last = length_text

        if  coor_top >= block["MIN_Y"]:
         #   print("تم تنفيذ الشرط")
            size = size - (size/7)
            X = X-1
        else:
            break
    return size

def openai_send(text12,type_):
    global data_config,data_json
    for i in range(5):
        try:
            if type_ == 1:
                model='gpt-3.5-turbo'
                client = OpenAI(
        api_key=data_config['defult']['keys']['openai'],)
            elif type_ == 2:
                model = "deepseek-chat"
                client = OpenAI(api_key=data_config['defult']['keys']['deepseek'],base_url="https://api.deepseek.com/v1") 
            response = client.chat.completions.create(model=model,
                messages=[{"role": "system", "content": tester},{"role": "user", "content": f"{text12}"}],temperature=0.2)
    
            return response.choices[0].message.content
        except Exception as d:
       #     print(str(d))
             pass
            

def check_prossecr():
    global data_config,data_json
    with open(rf"{data_json}","r", encoding="utf-8") as dataa:
        data_config= json.load(dataa)
    if data_config['status'] == 0:
        return 0
def update_json(number,i,c,h):
    global data_config,data_json
    data_config["bar"]= number
    data_config["all_page"] =  c
    data_config["page_now"] = i
    if h == 0:
        data_config["status"] =0
    with open(rf"{data_json}", "w", encoding="utf-8") as data_file:
        json.dump(data_config, data_file, ensure_ascii=False, indent=4)
def transleter(type_transleter,gmlh):
    text  = gmlh
    if type_transleter == 0:
        return translet_google(text= text)
    elif type_transleter== 1:
        return openai_send(type_=1,text12= text)
    elif type_transleter == 2:
        return openai_send(type_=2,text12= text)

def translet_google(text):
    for _ in range(5):
        try:
            translated = GoogleTranslator(source='auto', target='ar').translate(text)
            return translated
        except Exception as w:
            #print(str(w))          
            pass