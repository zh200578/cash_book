import tkinter
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class CashbookApp:
    def __init__(self, root):

        self.root = root
        self.root.title = "现金账簿"
        self.conn = sqlite3.connect("ZHANG.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

        # 保存键文本与按钮
        self.text_1 = tkinter.Text(self.root, height=2, width=15)
        self.text_1.pack(pady=15)
        b1 = tkinter.Button(self.root, text="保存至数据库", command=self.cunru, width="20")
        b1.pack(padx=20)

        # 查询键文本与按钮
        self.text_2 = tkinter.Text(self.root, height=2, width=15, wrap=tk.WORD)
        self.text_2.bind("<Control-v>", self.on_paste)
        self.text_2.bind("<Key>", self.on_key_press)
        self.text_2.pack(pady=10)
        b2 = tkinter.Button(self.root, text="查询数据", command=self.cha, width=20)
        b2.pack(pady=15, padx=15)
        # 删除键文本和按钮
        b3 = tkinter.Button(self.root, text="删除数据", command=self.delete, width=10)
        b3.pack()

    def date(self):
        now = datetime.now()
        fa_now = now.strftime("%Y-%m-%d")
        self.cur.execute("INSERT INTO cashbook(data) VALUES(?)", (fa_now,))
        self.conn.commit()
        return fa_now

    def cunru(self):
        text_store = self.text_1.get("1.0", tk.END)
        text_xiu = text_store.strip()
        if not text_xiu:
            tkinter.messagebox.showwarning("警告！", "存入内容不能为空！请重新输入")
            self.text_1.delete("1.0", tk.END)
        else:
            self.text_1.delete("1.0", tk.END)
            messagebox.showinfo("提示", "已保存至数据库")
            self.cur.execute("INSERT INTO cashbook(ru) VALUES(?)", (text_store,))
        self.conn.commit()

    def cha(self):
        self.cur.execute("SELECT ru  FROM cashbook")
        self.conn.commit()
        rows = self.cur.fetchall()
        self.text_2.delete("1.0", tk.END)
        for row in rows:
            self.text_2.insert(tk.END, str(row[0]) + '\n')
        if not rows:
            messagebox.showwarning("提示", "未找到相关数据！请更换查找条件")
        else:
            messagebox.showwarning("提示", "数据已查询完毕！")

    def delete(self):
        self.cur.execute("DELETE FROM cashbook")
        messagebox.showwarning("提示", "数据已全部删除！")

    def on_paste(self, event):
        messagebox.showinfo("提示", "粘贴操作已被禁用。")
        return "break"

    def on_key_press(self, event):
        return "break"


root = tk.Tk()
root.geometry("800x600")
app = CashbookApp(root)

root.mainloop()
