import tkinter as tk

root = tk.Tk()
root.geometry("450x600")
root.resizable(width=False, height=False)
root.title("Мой Калькулятор")
root.config(bg = "pink")

flowers = tk.Label(root, text=" ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀ ", font=("Segoe UI Symbol", 22), bg="pink", fg = "#b83280")
flowers.grid(row=0, column=0, columnspan=4, pady=5)

root.grid_anchor("n")

#оформление строки ввода
display = tk.Entry(
    root, 
    font = ("Times New Roman", 24), 
    justify ="right", 
    relief =  tk.SUNKEN,
    borderwidth = 4,
    highlightthickness = 3,
    highlightbackground = "#4A0F22",
    highlightcolor = "#9E6D7C",
    state="readonly")
display.grid(row=1, column=0, columnspan=4, padx=10, pady=20, ipadx= 30, ipady = 9)


#оформление цифры

button_style = {
    "font": ("Times New Roman", 20, "bold"),
    "width": 5,
    "height": 2,
    "bg": "#DDE9D9",
    "fg": "#9C3568",
    "activebackground": "#D5859F",
    "activeforeground": "white",
    "relief": tk.RAISED,
    "borderwidth": 4,
    "highlightthickness": 3,
    "highlightbackground": "#4A0F22",
    "highlightcolor": "#9E6D7C"
}

def click(number):
    global expression
    expression = ""
    display['state'] = "normal"
    
    value = display.get() + str(number)
    display.delete(0,tk.END)
    display.insert(0, value)
    
    display['state'] = "readonly"

    
btn7 = tk.Button(root, text="7", command=lambda: click("7"), **button_style)
btn7.grid(row=2, column=0, padx=5, pady=5)

btn8 = tk.Button(root, text="8", command=lambda: click("8"), **button_style)
btn8.grid(row=2, column=1, padx=5, pady=5)

btn9 = tk.Button(root, text="9", command=lambda: click("9"), **button_style)
btn9.grid(row=2, column=2, padx=5, pady=5)

btn4 = tk.Button(root, text="4", command=lambda: click("4"), **button_style)
btn4.grid(row=3, column=0, padx=5, pady=5)

btn5 = tk.Button(root, text="5", command=lambda: click("5"), **button_style)
btn5.grid(row=3, column=1, padx=5, pady=5)

btn6 = tk.Button(root, text="6", command=lambda: click("6"), **button_style)
btn6.grid(row=3, column=2, padx=5, pady=5)

btn1 = tk.Button(root, text="1", command=lambda: click("1"), **button_style)
btn1.grid(row=4, column=0, padx=5, pady=5)

btn2 = tk.Button(root, text="2", command=lambda: click("2"), **button_style)
btn2.grid(row=4, column=1, padx=5, pady=5)

btn3 = tk.Button(root, text="3", command=lambda: click("3"), **button_style)
btn3.grid(row=4, column=2, padx=5, pady=5)

btn0 = tk.Button(root, text="0", command=lambda: click("0"), **button_style)
btn0.grid(row=5, column=1, padx=5, pady=5)


#оформление операций

button_style2 = {
    "font": ("Times New Roman", 20, "bold"),
    "width": 5,
    "height": 2,
    "bg": "#FCF9DB",
    "fg": "#9C3568",
    "activebackground": "#D5859F",
    "activeforeground": "white",
    "relief": tk.RAISED,
    "borderwidth": 4,
    "highlightthickness": 3,
    "highlightbackground": "#4A0F22",
    "highlightcolor": "#9E6D7C"
}

def operation(sign):
    global expression
    expression = ""
    display['state'] = "normal"
    value = display.get()
    
    if value[-1] in '-+/*':
        value = value[:-1]
        
    display.delete(0,tk.END)
    display.insert(0, value+sign)
    
    display['state'] = "readonly"

btn_plus = tk.Button(root, text="+", command=lambda: operation("+"), **button_style2)
btn_plus.grid(row=5, column=3, padx=5, pady=5)

btn_minus = tk.Button(root, text="-", command=lambda: operation("-"), **button_style2)
btn_minus.grid(row=4, column=3, padx=5, pady=5)

btn_mult = tk.Button(root, text="*",command=lambda: operation("*"), **button_style2)
btn_mult.grid(row=3, column=3, padx=5, pady=5)

btn_devide = tk.Button(root, text="/", command=lambda: operation("/"), **button_style2)
btn_devide.grid(row=2, column=3, padx=5, pady=5)

def result():
    global expression
    expression = ""
    display['state'] = "normal"
    
    value = display.get()
    display.delete(0, tk.END)
    display.insert(0,eval(value))
    
    display['state'] = "readonly"

btn_result = tk.Button(root, text="=", command=result, **button_style2)
btn_result.grid(row=5, column=2, padx=5, pady=5)


    
btn_c = tk.Button(root, text="C", command=lambda: bt_clear(), **button_style2)
btn_c.grid(row=5, column=0, padx=5, pady=5)

root.mainloop()
