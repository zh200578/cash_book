import tkinter
import sqlite3
import tkinter as tk
from tkinter import messagebox

win = tkinter.Tk()
win.geometry("400x400")
conn = sqlite3.connect("ZHANG.db")
cur = conn.cursor()
#


def on_key_press(event):

    return "break"
def cunru():
    data = text_1.get("1.0", tk.END)

    cur.execute("INSERT INTO cashbook(data) VALUES(?)", (data,))
    conn.commit()
    text_1.delete("1.0", tk.END)
    tk.messagebox.showinfo("保存成功", "数据已成功保存到数据库！")

def cha():
    cur.execute("SELECT data FROM cashbook")
    conn.commit()
    rows=cur.fetchall()
    text_2.delete("1.0",tk.END)
    for row in rows:
        text_2.insert(tk.END, row[0])




text_1 = tkinter.Text(win, height=10, width=10)
text_1.pack(pady=10)
b1 = tkinter.Button(win, text="保存至数据库", command=cunru, width="20")
b1.pack()
text_2 = tkinter.Text(win,height=10,width=10)
text_2.bind("<Key>", on_key_press)
text_2.pack(pady=20)
b2 = tkinter.Button(win,text="查询数据",command=cha,width=20)
b2.pack()
win.mainloop()

































#cur.execute('''CREATE TABLE cashbook
#             (data text UNIQUE,
#             chu int,
#             ru int,













#             yu int)''')