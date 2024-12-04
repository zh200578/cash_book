import tkinter
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import time
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from bs4 import BeautifulSoup
import re
import os


class SecondPa(tk.Toplevel):
    def __init__(self):
        super().__init__()

        # 窗口设置
        self.title("二窗口")
        self.geometry("300x200")
        self.resizable(False, False)  # 禁止调整窗口大小

        # 样式设置
        self.configure(bg="lightgray")  # 设置背景颜色
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), bg="blue", fg="white", padx=10, pady=5)

        # 创建按钮并布局
        self.button = tk.Button(self, text="点击这里获取网页内容并保存图片！", command=self.show)
        self.button.pack(pady=20, padx=20)  # 使用pack布局，并设置内边距

    def show(self):
        path = "D:/临时文件/"
        if not os.path.isdir(path):
            os.makedirs(path)
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
            responses = requests.get("https://www.tsvtc.edu.cn/col/1270170474203/2024/09/19/1726729809940.html")
            print(responses.status_code)
            responses.encoding = responses.apparent_encoding
            html = responses.text
            bes = BeautifulSoup(html, "lxml")
            texts = bes.find("div", id="conN")
            cleaned_text = re.sub('[\r\n]', '', texts.text)
            texts_list = re.split(r'\xa0{4}', cleaned_text)
            parr = re.compile('src="(/a.*?)"')
            image = re.findall(parr, responses.text)
            a = 0
            for i in image:
                link = "https://www.tsvtc.edu.cn/" + i
                a += 1
                with open(path + "/{}.jpg".format(str(a)), "wb", ) as img:
                    res = requests.get(link)
                    img.write(res.content)
                    img.close()

            # 可选：显示成功消息框
            messagebox.showinfo("成功", "图片已成功保存！")

        except requests.RequestException as e:
            # 处理请求异常
            messagebox.showerror("错误", f"请求出错：{e}")
        except Exception as e:
            # 处理其他异常
            messagebox.showerror("错误", f"发生错误：{e}")


class CashbookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.second = None
        self.title("现金账簿")
        self.conn = sqlite3.connect("ZHANG.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

        # 标签控件
        self.label1 = tk.Label(self, height=2, text="入库日期:", font=("Arial", 12))
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.label2 = tk.Label(self, height=2, text="入库数量:", font=("Arial", 12))
        self.label2.grid(row=0, column=1, padx=10, pady=10)
        self.label3 = tk.Label(self, height=2, text="出库数量:", font=("Arial", 12))
        self.label3.grid(row=0, column=2, padx=10, pady=10)

        # 日期输入文本框
        self.text_1_date = tk.Entry(self, width=16, font=("", 18))  # 使用Entry代替Text，更适合输入日期
        self.text_1_date.grid(row=1, column=0, padx=10, pady=5)

        # 入库数量文本框
        self.text_1_ru = tk.Entry(self, width=16, font=("", 18))  # 使用Entry代替Text
        self.text_1_ru.grid(row=1, column=1, padx=10, pady=5)

        # 出库数量文本框
        self.text_1_chu = tk.Entry(self, width=18, font=("", 18))  # 使用Entry代替Text
        self.text_1_chu.grid(row=1, column=2, padx=10, pady=5)

        # 保存键按钮
        b1 = tk.Button(self, text="保存至数据库", command=self.cunru, width=20, font=("", 12))
        b1.grid(row=2, column=1, pady=15, padx=10)

        # 查询键文本框与按钮
        self.text_2 = tk.Text(self, height=8, width=60, wrap=tk.WORD)
        self.text_2.grid(row=3, column=0, columnspan=3, pady=10, padx=10)
        b2 = tk.Button(self, text="查询数据", command=self.cha, width=20, font=("", 12))
        b2.grid(row=4, column=1, pady=10, padx=10)

        # 删除键按钮
        b3 = tk.Button(self, text="删除数据", command=self.delete, width=20, font=("", 12))
        b3.grid(row=5, column=0, pady=10, padx=10)

        # 折线图按钮
        b4 = tk.Button(self, text="绘制折线图", command=self.table, width=20, font=("", 12))
        b4.grid(row=5, column=2, pady=10, padx=10)

        # 爬虫按钮
        b5 = tk.Button(self, text="爬虫", command=self.Second, width=20, font=("", 12))
        b5.grid(row=6, column=1, pady=10, padx=10)

    def Second(self):
        self.second = SecondPa()
        # messagebox.showinfo("欢迎!","本工具为VIP人员附赠的爬虫工具包，欢迎使用！")

    def date(self):
        now = datetime.now()
        fa_now = now.strftime("%Y-%m-%d")
        self.cur.execute("INSERT INTO cashbook(data) VALUES(?)", (fa_now,))
        self.conn.commit()
        return fa_now

    def cunru(self):
        # 输入数据处理
        text_store_ru = self.text_1_ru.get("1.0", tk.END).strip().splitlines()
        text_store_date = self.text_1_date.get("1.0", tk.END).strip().splitlines()
        text_store_chu = self.text_1_chu.get("1.0", tk.END).strip().splitlines()
        # 将输入的数据处理为列表
        text_lines = min(len(text_store_ru), len(text_store_date), len(text_store_chu))
        if text_lines == 0:
            tkinter.messagebox.showwarning("警告！", "存入内容不能为空！请重新输入")
            self.text_1_ru.delete("1.0", tk.END)
        else:
            # 跟踪重复的异常日期，并显示索引
            for index, (ru, data, chu) in enumerate(zip(text_store_ru, text_store_date, text_store_chu), start=1):
                try:
                    self.cur.execute("INSERT INTO cashbook(ru, data, chu) VALUES(?, ?, ?)",
                                     (ru, data, chu))
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    messagebox.showwarning(f"警告！", f"第{index}行所对应数据{data}出现异常，请重新输入")
                    break

            messagebox.showwarning("提示", "所有有效数据已成功保存至内置数据库中")
            self.conn.commit()
            self.text_1_chu.delete("1.0", tk.END)
            self.text_1_date.delete("1.0", tk.END)
            self.text_1_ru.delete("1.0", tk.END)

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
        self.text_2.delete("1.0", tk.END)

    def table(self):
        plt.rcParams['font.family'] = 'SimHei'  # 使用黑体
        new_window = tk.Toplevel(self)
        new_window.title("新窗口")
        new_window.geometry("600x400")
        self.cur.execute("SELECT data,ru FROM cashbook")
        rows = self.cur.fetchall()
        time1 = [row[0] for row in rows]
        value = [row[1] for row in rows]
        if not time and not value:
            messagebox.showwarning("警告", "数据异常，无法绘制！")
        fig, ax = plt.subplots()
        plt.plot(time1, value)
        for i, (x_i, y_i) in enumerate(zip(time1, value)):
            # 在数据点旁边添加纵坐标值，偏移量可根据需要调整
            plt.annotate(str(y_i),  # 仅显示纵坐标值
                         xy=(x_i, y_i),  # 数据点坐标
                         xytext=(5, 5),  # 文本相对于数据点的偏移量（正数表示向右上方偏移）
                         textcoords='offset points',  # 偏移量的单位
                         ha='left',  # 文本水平对齐方式（因为是从数据点右侧添加标签）
                         va='bottom')  # 文
        plt.title("入库数量折线图")
        plt.xlabel("时间")
        plt.ylabel("数量")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_paste(self, event):
        messagebox.showinfo("提示", "粘贴操作已被禁用。")
        return "break"

    def on_key_press(self, event):
        return "break"


app = CashbookApp()
app.mainloop()
b = time.time()
