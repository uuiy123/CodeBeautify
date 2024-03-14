from tkinter import *
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import clipboard
import os

def alert(strMsg):
    msgbox.showinfo('알림', strMsg)

## 붙여넣기
def btnPaste():
    ## 초기화
    btnInit()
    #objTextAreaBf.delete(0.0, 'end')
    ## 붙여넣기
    result = clipboard.paste()
    # 파이썬에서 캐리지 리턴의 경우 ?으로 표기 되기 때문에 삭제
    result = result.replace("\r", "")
    # 엔터 문자를 여러번 사용한 경우 엔터문자를 한번만으로 변경
    result = result.replace("\n\n", "\n")
    # 띄어쓰기 4번은 Tab문자로 변경
    result = result.replace("    ", "\t")
    objTextAreaBf.insert(INSERT, result)

# IF문 변환
def convertIf(strTemp):


    searchKeyword1 = "else if"
    searchKeyword2 = "if"
    searchKeyword3 = "else"

    #
    if (searchKeyword1 in strTemp):

        if (("}" + searchKeyword1) in strTemp):
            strTemp = strTemp.replace("} else if (", "} else if ( ")
            strTemp = strTemp.replace("}else if(", "} else if ( ")

        else:
            strTemp = strTemp.replace("else if (", "else if ( ")
            strTemp = strTemp.replace("else if(", "else if ( ")

        if (strTemp[-1] == "{"):
            strTemp = strTemp.replace(") {", " ) {")
            strTemp = strTemp.replace("){", " ) {")
            strTemp = strTemp.replace(" ){", " ) {")

        else:
            strTemp = strTemp.replace(")", " )")

    elif (searchKeyword2 in strTemp):
        strTemp = strTemp.replace("if (", "if ( ")
        strTemp = strTemp.replace("if(", "if ( ")

        if (strTemp[-1] == "{"):
            strTemp = strTemp.replace(") {", " ) {")
            strTemp = strTemp.replace("){", " ) {")
            strTemp = strTemp.replace(" ){", " ) {")

        else:
            strTemp = strTemp.replace(")", " )")

    elif (searchKeyword3 in strTemp):
        #}else{
        if (("}" + searchKeyword3 + "{") in strTemp):
            strTemp = strTemp.replace("}else{", "} else {")
        #} else{
        elif (("} " + searchKeyword3 + "{") in strTemp):
            strTemp = strTemp.replace("} else{", "} else {")
        #}else {
        elif (("}" + searchKeyword3 + " {") in strTemp):
            strTemp = strTemp.replace("}else {", "} else {")
        #} else {
        elif (("} " + searchKeyword3 + " {") in strTemp):
            strTemp = strTemp.replace("} else {", "} else {")
        #}else
        elif (("}" + searchKeyword3) in strTemp):
            strTemp = strTemp.replace("}else", "} else")
        # else{
        elif ((searchKeyword3 + "{") in strTemp):
            strTemp = strTemp.replace("else{", "else {")
    #
    strTemp = strTemp.replace("  ", " ")

    # return
    return strTemp

# For문 변환
def convertFor(strTemp):

    searchKeyword = "for"

    # for(a; b; c){ 형태
    if ((strTemp[-1] == "{") and (searchKeyword in strTemp)) :
        strTemp = strTemp.replace("for(", "for ( ")
        strTemp = strTemp.replace("for (", "for ( ")
        strTemp = strTemp.replace(";", "; ")
        strTemp = strTemp.replace("){", " ) {")
    # if(a) 형태
    elif (searchKeyword in strTemp):
        strTemp = strTemp.replace("for(", "for ( ")
        strTemp = strTemp.replace("for (", "for ( ")
        strTemp = strTemp.replace(";", "; ")
        strTemp = strTemp.replace(")", " )")
    #
    strTemp = strTemp.replace("  ", " ")

    # return
    return strTemp

## 변환부분
def btnConvert():
    os.system('cls')
    strText = objTextAreaBf.get(1.0, "end")
    arText = strText.splitlines()

    strCompText = ""
    
    for x in arText:
        # 초기화
        strTemp = ""
        if (x != ""):
            strTemp = x.rstrip()
            strTemp = convertIf(strTemp)
            strTemp = convertFor(strTemp)
            strCompText += strTemp + "\n" 
        else:
            strCompText += strTemp + "\n" 

    ### 변환 부분 텍스트 AREA로 리턴
    objTextAreaAf.insert(INSERT, strCompText)
    clipboard.copy(strCompText)
    msgbox.showinfo('알림', '복사되었습니다.')

def btnInit():
    ## 초기화
    objTextAreaBf.delete(0.0, 'end')
    objTextAreaAf.delete(0.0, 'end')

## alpha는 창의 투명도를 설정함, 1은 투명도0, 0은 완전 투명
def slide(_):
    root.attributes('-alpha', objSlideBar.get())
    slide_label.config(text=str(round(objSlideBar.get(), 2)))

def changewindowstop():

    if CheckVal1.get() == 1:
        root.wm_attributes("-topmost", 1)
    else:
        root.wm_attributes("-topmost", 0)

# 루트화면 (root window) 생성
root = tk.Tk()

## 화면구성
## aplication을 프레임 설정하여 각 obj를 배치할수 있게 틀을 잡아준다.
frame1 = Frame(root)
frame1.place(x=5, y=0)
frame2 = Frame(root)
frame2.place(x=270, y=0)

frame3 = Frame(root)
frame3.place(x=180, y=450)
#frame3.grid(row=1, column=1)
frame4 = Frame(root)
frame4.place(x=180, y=475)
#frame4.grid(row=2, column=1)

#Label 배치
objLbBefore = Label(frame1, text="변환 전")
objLbBefore.pack(side=TOP)
objLbAfter = Label(frame2, text="변환 후")
objLbAfter.pack(side=TOP)

## SCROLLBAR와, TEXTAREA 객체 배치
objScrollBar1 = Scrollbar(frame1)
objTextAreaBf = Text(frame1, width=35, height=32)
objTextAreaBf.pack(side=LEFT, fill=Y)
objScrollBar1.pack(side=LEFT, fill=Y)
objScrollBar1.config(command=objTextAreaBf.yview)
objTextAreaBf.config(yscrollcommand=objScrollBar1.set)

objScrollBar2 = Scrollbar(frame2)
objTextAreaAf = Text(frame2, width=35, height=32)
objTextAreaAf.pack(side=LEFT, fill=Y)
objScrollBar2.pack(side=LEFT, fill=Y)
objScrollBar2.config(command=objTextAreaAf.yview)
objTextAreaAf.config(yscrollcommand=objScrollBar2.set)


objInitButton = Button(frame3, text="초기화", command=btnInit)
objInitButton.pack(side=LEFT)

## 복사, 변환, 항상위에 객체 배치
objPasteButton = Button(frame3, text="붙여넣기", command=btnPaste)
objPasteButton.pack(side=LEFT)

objConvertButton = Button(frame3, text="변환", command=btnConvert)
objConvertButton.pack(side=LEFT)

CheckVal1 = tk.IntVar()
objTopChkButton = Checkbutton(frame3, text="항상위에", variable=CheckVal1, command=changewindowstop)
objTopChkButton.pack(side=LEFT)

## 투명도 조절 객체 배치
objSlideLabel = Label(frame4, text='투명도 레벨')
objSlideLabel.pack(side="left")
objSlideBar = ttk.Scale(frame4, from_=0.1, to=1.0, value=1, orient=HORIZONTAL, command=slide)
objSlideBar.pack(side="left")

root.geometry("540x500")
root.resizable(False, False)
root.title("마이플랫폼 코드변환")
root.attributes('-alpha', 1)
# 4. 메인루프 실행
root.mainloop()