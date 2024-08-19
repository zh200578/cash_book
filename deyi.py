import tkinter
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time


class CashbookApp:
    def __init__(self, root):

        self.root = root
        self.root.title = "现金账簿"
        self.conn = sqlite3.connect("ZHANG.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

        # 保存键文本与按钮
        # 日期输入文本框
        self.text_1_date = tkinter.Text(self.root, height=10, width=18)
        self.text_1_date.grid(row=0, column=1, pady=15, padx=12)
        # 入库数量文本框
        self.text_1_ru = tkinter.Text(self.root, height=10, width=18)
        self.text_1_ru.grid(row=0, column=0, pady=15, padx=12)
        # 出库数量文本框
        self.text_1_chu = tkinter.Text(self.root, height=10, width=18)
        self.text_1_chu.grid(row=0, column=2, pady=15, padx=12)
        b1 = tkinter.Button(self.root, text="保存至数据库", command=self.cunru, width="20")
        b1.grid(row=1, column=1, pady=25)

        # 查询键文本与按钮
        self.text_2 = tkinter.Text(self.root, height=8, width=60, wrap=tk.WORD)
        self.text_2.bind("<Control-v>", self.on_paste)
        self.text_2.bind("<Key>", self.on_key_press)
        self.text_2.grid(row=2, column=1, pady=60)
        b2 = tkinter.Button(self.root, text="查询数据", command=self.cha, width=20)
        b2.grid(pady=15, padx=15)
        # 删除键文本和按钮
        b3 = tkinter.Button(self.root, text="删除数据", command=self.delete, width=10)
        b3.grid()

    def date(self):
        now = datetime.now()
        fa_now = now.strftime("%Y-%m-%d")
        self.cur.execute("INSERT INTO cashbook(data) VALUES(?)", (fa_now,))
        self.conn.commit()
        return fa_now

    def cunru(self):
        text_store_ru = self.text_1_ru.get("1.0", tk.END).strip().splitlines()
        text_store_date = self.text_1_date.get("1.0", tk.END).strip().splitlines()
        text_store_chu = self.text_1_chu.get("1.0", tk.END).strip().splitlines()
        text_lines = min(len(text_store_ru), len(text_store_date), len(text_store_chu))
        if text_lines == 0:
            tkinter.messagebox.showwarning("警告！", "存入内容不能为空！请重新输入")
            self.text_1_ru.delete("1.0", tk.END)
        else:
            for index, (ru, data, chu) in enumerate(zip(text_store_ru, text_store_date, text_store_chu), start=1):
                try:
                    self.cur.execute("INSERT INTO cashbook(ru, data, chu) VALUES(?, ?, ?)",
                                 (ru, data, chu))
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    messagebox.showwarning(f"警告！",f"第{index}行所对应数据{data}，请重新输入")
                    break
            messagebox.showwarning("提示", "所有有效数据已成功保存至内置数据库中")
            self.conn.commit()

    def cha(self):
        self.cur.execute("SELECT data,ru,chu  FROM cashbook")
        self.conn.commit()
        rows = self.cur.fetchall()
        self.text_2.delete("1.0", tk.END)
        for row in rows:
            self.text_2.insert(tk.END, f"日期：{row[0]}入库数量：{row[1]}出库数量：{row[2]}" + '\n')
        if not rows:
            messagebox.showwarning("提示", "未找到相关数据！")
        else:
            time.sleep(0.2)
            messagebox.showwarning("提示", "数据已查询完毕！")

    def delete(self):
        self.cur.execute("DELETE FROM cashbook")
        messagebox.showwarning("提示", "数据已全部删除！")

    def on_paste(self, event):
        messagebox.showinfo("提示", "粘贴操作已被禁用。")
        return "break"

    def on_key_press(self, event
                     ):
        return "break"


root = tk.Tk()
root.geometry("800x600")
app = CashbookApp(root)
root.mainloop()
