# -*- coding: utf-8 -*-

# from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.pdfbase import pdfmetrics
# import arabic_reshaper
from datetime import datetime
import platform
# from reportlab.pdfbase.ttfonts import TTFont
# from bidi.algorithm import get_display
# from reportlab.lib.units import mm, inch
from prettytable import PrettyTable as pt
if platform.system == "windows" : 
	import win32print
else : 
	win32print = ""
import os 

# def text_ar(text_ar) : 
    
#     text = arabic_reshaper.reshape(str(text_ar))
#     text = get_display(text)
#     return text 

# def createReceipt(id , seller , data , intotal) :
#     pdfmetrics.registerFont(TTFont('Arabic', "statics/fonts/receitFont.ttf"))
    
#     DATA = [[text_ar("اسم الصنف") , text_ar("الكميه") , text_ar("السعر")]]
#     for x in data  : 
#         DATA.append([text_ar(x['name']) , text_ar(x['amount']) ,text_ar("جنيه") + " " + str(text_ar(int(x['price']) * int(x['amount'])) )]) 

#     print(help(SimpleDocTemplate))
#     pdf = SimpleDocTemplate( "statics/pdf/receipt.pdf" , pagesize= (60 * mm, 106 * mm) )
#     styles = getSampleStyleSheet()
    
    
#     title_style = styles[ "Heading1" ]
#     title_style.alignment = 1
#     title_style.fontName = "Arabic"
#     title_style.fontSize = 11


#     title_style2 = styles[ "Heading2" ]
#     title_style2.alignment = 1
#     title_style2.fontName = "Arabic"
#     title_style2.fontSize = 11

    
    
#     seller_style = styles[ "Heading4" ]
#     seller_style.alignment = 1
#     seller_style.fontName = "Arabic"

 
#     cp_style = styles[ "Heading5" ]
#     cp_style.alignment = 1
#     cp_style.fontName = "Arabic"
#     cp_style.fontSize = 10



#     receitId_style = styles[ "Heading5" ]
#     receitId_style.alignment = 1
#     receitId_style.fontName = "Arabic"
#     receitId_style.fontSize = 10


#     datetime_style = styles[ "Heading5" ]
#     datetime_style.alignment = 1
#     datetime_style.fontName = "Arabic"


#     receitid = Paragraph(  text_ar(f"رقـم الفـاتوره : {id}")  , receitId_style )

#     title = Paragraph( text_ar("<span>fsdsad</span>مخــابز الأداره")  , title_style )
#     title2 = Paragraph( text_ar("قسـم الأفـــران") , title_style2 )
#     datetimer = Paragraph(  text_ar(datetime.now().strftime("%D/%m/%Y @ %H:%M:%S %p"))  , datetime_style)

#     seller = Paragraph(  text_ar(f"كــاشير : {seller}")  , seller_style )
#     cp = Paragraph(text_ar("تم التصـميم بواسطه د.وليد أسامه") , cp_style )

#     style = TableStyle(
#         [
#             ('ALIGN',(0,-1),(-1,-1),'CENTER'),
#             ( "BOX" , ( 0, 0 ), ( -1, -1 ), 1 , colors.black ),
#             ( "GRID" , ( 0, 0 ), ( 4 , 4 ), 1 , colors.black ),
#             ( "BACKGROUND" , ( 0, 0 ), ( 3, 0 ), colors.gray ),
#             ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.whitesmoke ),
#             # ('ALIGN',(0,-1),(1,1),'CENTER'),
#             ("VALIGN" , ( 0, 0), ( 0, 0 ) , "TOP" ),
#             ( "BACKGROUND" , ( 0 , 1 ) , ( -1 , -1 ), colors.beige ),
#             ("FONTNAME" , (0 , 0) , (3 , 3) , "Arabic")
#         ]
#     )
#     # (receit_width / 3) -20
#     table = Table( DATA , style = style  , colWidths = [100 , 40 , 40])
#     total = Table([[text_ar("الاجمالي") , text_ar(f"{intotal} جنيه")]] , style = style , colWidths = [90 , 90 ])
#     pdf.build([title,table , total])
#     # pdf.build([ title , title2 ,receitid, table , total , seller  , datetimer ,cp ])
#     path = os.path.join(os.getcwd() , 'statics' , 'pdf' ,"receipt.pdf")
#     try : 
        
#         os.startfile(path , "print")
#         return {"state" : True }
#     except : 
#         return {"state" : False , "reason" :"no.printer.detected"}
    

def newPrint(data , type = str) : 
    import win32ui
    fontdata = { 'name':'Arial', 'height':13}
    if type == "sales" : 
            fontdata = { 'name':'Arial', 'height':10}

# X from the left margin, Y from top margin
# both in pixels
    X=20; Y=52
    multi_line_string = data
    hDC = win32ui.CreateDC ()
    font = win32ui.CreateFont(fontdata)
    hDC.CreatePrinterDC (win32print.GetDefaultPrinter())
    hDC.StartDoc ("receipt")
    hDC.StartPage ()
    hDC.SelectObject(font)
    for line in multi_line_string:
        hDC.TextOut(X,Y,line )
        Y += 30
    hDC.EndPage ()
    hDC.EndDoc ()
    
    
def receipt(seller  = "مجهول" , id_ = '0' , data_ = [{"name":"??" , "amount" : "??" , "price" : "??"}] , intotal = 0 , isbonus = 0) : 
    casher = seller
    receitId = id_
    data = pt(["الصنف" , "الكميه" , "السعر"] ,)
    data.encoding = "utf-8"
    data.align['الصنف'] = 'l'
    data.align['الكميه'] = 'c'
    data.align['السعر'] = 'r'
    data.valign = "m"
    data.title = f"فــاتوره رقم : {receitId}"

    
    for i,x  in enumerate(data_) : 
        # print(f"{i} → {x}")
        if len(data_) == i + 1  :
            data.add_row([x['name'].strip(" ") , x['amount'] , float(x['price'])*int(x['amount'])] , divider = True)
        else : 
            data.add_row([x['name'].strip(" ") , x['amount'] , float(x['price'])*int(x['amount'])])

  
    data.add_row(["الأجمالي" , "" , f"{float(intotal)}"])
    # print(data)
    table_width = 0 
    
    for x,y in enumerate(str(data)) : 
        if y == "+"     : 
            if x != 0 : 
                table_width = x+1
                # print(table_width)
                break 
            



    footer = "\n"
    footer += f"كاشير : {casher}".center(table_width)
    footer += "\n"
    footer += (datetime.now().strftime("%d/%m/%Y @ %I:%M:%S %p")).center(table_width)
    footer += "\n"
    footer += "-- د.وليدأسامه --".center(table_width)

    if bool(int(isbonus)) : 
        title = "مخــــابز الإدارة".center(table_width) + "\n" + "$بون سحب خاص ب أمين الشرطه$".center(table_width) + "\n"
    else : 
        title = "مخــــابز الإدارة".center(table_width) + "\n" 

    data = title + str(data) + str(footer)
    print(data)
    data = data.split("\n")
 
    newPrint(data)
    
    
    
    
    
    
    
    
    
# Copy receit Function Creation 
#       By . Waleed Osama 
# Omega POS system V 6
# edited in 21/6/2024

def copy_receipt(seller  = "مجهول" , id_ = '0' , data_ = [{"name":"??" , "amount" : "??" }] ) : 

    casher = seller
    receitId = id_
    data = pt([ "الكميه" , "الصنف"] ,)
    data.encoding = "utf-8"
    data.align['الصنف'] = 'c'
    data.align['الكميه'] = 'l'
    data.valign = "m"
    data.title = f"فــاتوره رقم : {"$"+receitId }"

    
    for i,x  in enumerate(data_) : 
        # print(f"{i} → {x}")
        if len(data_) == i + 1  :
            data.add_row([x['name'].strip(" ") , x['amount'] ] , divider = True)
        else : 
            data.add_row([x['name'].strip(" ") , x['amount'] ])

  
    # data.add_row(["هذا الصنف مخصص للمخزن فقط" , ""])
    # print(data)
    table_width = 0 
    
    for x,y in enumerate(str(data)) : 
        if y == "+"     : 
            if x != 0 : 
                table_width = x+1
                # print(table_width)
                break 
            



    footer = "\n"
    footer += f"كاشير : {casher}".center(table_width)
    footer += "\n"
    footer += (datetime.now().strftime("%d/%m/%Y @ %I:%M:%S %p")).center(table_width)
    footer += "\n"
    footer += "-- د.وليدأسامه --".center(table_width)

    title = "مخــــابز الإدارة".center(table_width) + "\n" + "نسخه بون خـاصه للمخزن".center(table_width) + "\n"
    data = title + str(data) + str(footer)
    print(data)
    data = data.split("\n")
 
    newPrint(data)




    
# newPrint()


# newPrint(receipt=receipt())



def print_total_day_sales(seller  = "مجهول" , id_ = '0' , data_ = [{"name":"??" , "amount" : "??" , "price" : "??" }] , intotal = 0) : 

    casher = seller
    receitId = id_
    data = pt(["الصنف" , "الكميه"  , "سعر القطعه", "الإجمالي"] ,)
    data.encoding = "utf-8"
    data.align['الصنف'] = 'l'
    data.align['الكميه'] = 'c'
    data.align['سعر القطعه'] = 'c'
    data.align['السعر'] = 'r'
    data.valign = "m"
    data.title = f"إجمالي يومية {datetime.now().strftime("%d/%m/%Y @ %I:%M:%S %p")}"

    
    for i,x  in enumerate(data_) : 
        # print(f"{i} → {x}")
        if len(data_) == i + 1  :
            data.add_row([x['name'].strip(" ") , x['amount'] , x['price'],  float(x['price'])*int(x['amount'])] , divider = True)
        else : 
            data.add_row([x['name'].strip(" ") , x['amount'] , x['price'] , float(x['price'])*int(x['amount'])])

  
    data.add_row(["الأجمالي" , ""  , " ", f"{float(intotal)}"])
    # print(data)
    table_width = 0 
    
    for x,y in enumerate(str(data)) : 
        if y == "+"     : 
            if x != 0 : 
                table_width = x+1
                # print(table_width)
                break 
            



    footer = "\n"
    # footer += f"كاشير : {casher}".center(table_width)
    # footer += "\n"
    footer += (datetime.now().strftime("%d/%m/%Y @ %I:%M:%S %p")).center(table_width)
    footer += "\n"
    footer += "-- د.وليدأسامه --".center(table_width)

    title = "مخــــابز الإدارة".center(table_width) + "\n"

    data = title + str(data) + str(footer)
    print(data)
    data = data.split("\n")
 
    newPrint(data , type = "sales")
    
    
