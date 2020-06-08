from tkinter import *
import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime
import os


def get_datetime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


class SelectionPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        mainframe = tk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)
        tkvar = StringVar(self)
        choices = {'add_sub', 'add'}
        Label(mainframe, text="Choose a test").grid(row=1, column=1)
        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        popupMenu.config(width=20)

        popupMenu.grid(row=2, column=1)


        def start_practice():
            print(tkvar.get())
            time = 180

            tol = 0.1 # approximation error tol
            root = Tk()
            choices_dict = {'add_sub': ['add', 'sub'],
                            'add': ['add']}

            app = App(root, time, tol, choices_dict[tkvar.get()])
            root.mainloop()

        MyButton1 = Button(mainframe, text="Submit", width=10, command=start_practice)
        MyButton1.grid(row=3, column=1)



class App(tk.Frame):
    def __init__(self, parent, time, tol, choices):
        tk.Frame.__init__(self, parent)
        self.count = time
        self.scr = 0
        self.ans = 5
        self.exact = True
        self.tol = tol

        self.choices = choices

        self.parent = parent



        self.parent.title("MENTAL MATH QUANT GRIND")
        self.parent.geometry("700x130")

        self.prompt = Label(self, text="2+3=", bg="gainsboro", width=10,
                        font = ("Roman", 40), anchor = 'e')  # shift text to left: east

        self.answer = Entry(self, font=("Roman", 40), width=20)
        self.answer.bind("<Return>", self.check_answer)


        self.timer = Label(self, text="Seconds left: 1")
        self.score = Label(self, text="score: 0")

        motive = "[Chorus] Just like Citadel, Jane Street, Two Sigma, Akuna" \
                 "\nAll I need, yeah, you're all I need."

        self.motive = Label(self, text=motive, font=("Helvetica", 10, "italic"))

        self.correct_ans = Label(self, font=("Roman", 20))

        self.prompt.grid(row=0)
        self.answer.grid(row=0, column=1)
        self.score.grid(row=1)
        self.timer.grid(row=1, column=1)
        self.correct_ans.grid(row=2)
        self.motive.grid(row=2, column=1)
        self.pack()

        self.onUpdate()

    def speak(self, prompt):
        #self.engine.say(prompt)
        #self.engine.runAndWait()
        os.system("say -v vicki \"" + prompt + "\" -r 120 &") # & to prevent blocking thread

    def next_question(self):
        def mul9():
            x = random.randint(1, 9)
            prompt = '{} x 9 ='.format(x)
            self.ans = x * 9
            return prompt

        def square5():
            x = random.randint(1, 9)
            prompt = '{}^2 ='.format(10*x + 5)
            self.ans = (10*x + 5)**2
            return prompt
        # ab * 11
        # ab * 10 + ab
        # a*100 b*10 + a*10   b
        def mul11():
            x = random.randint(1, 100)
            prompt = '{} x 11 ='.format(x)
            self.ans = x * 11
            return prompt

        # ba * bc
        # ...
        def mul_firstsame_last10():
            x = random.randint(1, 9)
            y = random.randint(1, 9)
            prompt = '{}{} x {}{} ='.format(x, y, x, 10-y)
            self.ans = (10*x + y) * (10*x + 10-y)
            return prompt


        def square():
            x = random.randint(1, 10)
            prompt = '{}^2 ='.format(x)
            self.ans = x ** 2
            return prompt

        def square_root():
            x = random.randint(1, 100)
            prompt = '\sqrt {} ='.format(x)
            self.ans = x ** (0.5)
            self.exact = False
            return prompt

        def add():
            x = random.randint(1, 100)
            y = random.randint(1, 100)
            prompt = '{} + {} ='.format(x, y)
            self.ans = x + y
            return prompt

        def sub():
            x = random.randint(1, 100)
            y = random.randint(1, 100)
            x, y = sorted([x, y])
            prompt = '{} - {} ='.format(y, x)
            self.ans = y - x
            return prompt

        def mul12():
            x = random.randint(1, 100)
            prompt = '{} * 12 ='.format(x)
            self.ans = x * 12
            return prompt

        this_fn = locals()
        self.tests = [this_fn[i] for i in self.choices]
        #self.tests = [add, sub]

        #self.tests = [sub]
        #self.tests = [mul12]
        #self.tests = [mul9, mul11, square5, \
        #              mul_firstsame_last10, square_root, \
        #              square, square_root, add, sub]

        #self.tests = [square_root, square]
        #self.tests = [square_root]

        #self.tests = [add, square_root]


        return random.choice(self.tests)()

    def check_answer(self, event):

        user_ans = float(self.answer.get().strip())
        diff = abs(user_ans - self.ans)
        print('diff:', diff, '|exact?', self.exact, '| tol:', self.tol, '| my ans:', user_ans)

        if diff == 0 or (not self.exact and diff < self.tol):
            self.exact = True
            self.correct_ans["text"] = self.prompt["text"] + ('%.3f'% self.ans)
            prompt = self.next_question()
            self.prompt["text"] = prompt
            #self.speak(prompt)
            self.scr += 1
            self.answer.delete(0, 'end')
        else:
            self.scr -=1

        self.score["text"] = "score: " + str(self.scr)

    def onUpdate(self):
        # update displayed time
        self.count -=1
        if self.count <= 0:
            messagebox.showinfo("TIME'S UP!", "YOUR SCORE = {}".format(self.scr))
            self.parent.destroy()
        else:
            self.timer['text'] = "Seconds left: " + str(self.count)
            # schedule timer to call myself after 1 second
            self.parent.after(1000, self.onUpdate)

if __name__ == '__main__':
    # https://pythonspot.com/tk-dropdown-example/
    #root = Tk()
    #time = 180

    #tol = 0.1 # approximation error tol

    #app = App(root, time, tol)
    #root.mainloop()

    ## LOGGING
    # LEGACY
    #datetime = get_datetime()
    #log_score = "grind_sheet.txt"
    #log = datetime + " | " + "score = " + str(app.scr) + " | " + "time = " \
    #      + str(time) + " | " + "tests = " + " ;".join([fn.__name__ for fn in app.tests]) \
    #      + "\n"

    #print("Result >>", log)
    #with open(log_score, "a") as f:
    #    f.write(log)

    app = SelectionPage()
    app.mainloop()

