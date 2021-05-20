import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Text, messagebox
import os
import json
from tkinter import simpledialog
from tkinter import StringVar
import ctypes


# __init__ is used when creating a class or objects or self, it is used
#   when you need to assign a certain value to functions within a class

os.getcwd()

class Firstpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #create jsonfile on open
        def Json_check(json_file):
            return os.path.exists(json_file)

        if Json_check('quiz.json'):
            pass
        else:
            quiz={}
            with open('quiz.json', 'w') as fp:
                json.dump(quiz, fp)



        #BORDER
        border_blue= tk.LabelFrame(self, bg="Blue", bd=10)
        border_blue.pack(fill="both", expand="yes", padx=10, pady=20)

        # FUNCTIONS FOR BUTTONS
        def Update(side):
            with open ('quiz.json', 'r') as fp:
                quiz= json.load(fp)
            if side == "Vocab":
                vocab_list=[]
                for line in quiz:
                    vocab_list.append(line)
                vocab_return= str(vocab_list)
                vocab_return = vocab_return.replace('[','').replace(']','').replace(',', '\n')
                return vocab_return
            elif side == "Mean":
                mean_list=[]
                for line in quiz:
                    mean_list.append(quiz[line])
                mean_return = str(mean_list)
                mean_return = mean_return.replace('[', '').replace(']', '').replace(',','\n')
                return mean_return
            else:
                print('thats not a valid choice')





        def Add():
            #input for vocab and meaning
            Vocab_input= simpledialog.askstring(title="Vocab", prompt=" input vocab")
            Mean_input= simpledialog.askstring(title="meaning", prompt="input meaning")
            input_data= {Vocab_input:Mean_input}

            #create a json file if one is not found
            try:
                with open('quiz.json', 'r') as fp:
                    quiz = json.load(fp)

            except IOError:
                quiz = {}

            #Add dic to json
            with open('quiz.json', 'w') as fp:
                quiz.update(input_data)
                json.dump(quiz, fp, indent=4)
            v.set(Update("Vocab"))
            m.set(Update("Mean"))


        def Del():
            Vocab_del = simpledialog.askstring( title='del vocab', prompt="input vocab to delete")
            with open ('quiz.json', 'r+') as fp:
                quiz= json.load(fp)
                for key in quiz:
                    if key ==Vocab_del:
                        quiz.pop(Vocab_del)
                        fp.seek(0)
                        json.dump(quiz, fp, indent=4)
                        fp.truncate()
                        break
                    else:
                        pass
            v.set(Update("Vocab"))
            m.set(Update("Mean"))


        Label= tk.Label(border_blue, text="Quiz Project", bg="blue", font=("Arial Bold", 30))
        Label.place(x=180, y=10)

        Label_Vocab= tk.Label(border_blue, text="Vocab", bg="white", bd=5, font=("Arial Bold", 15))
        Label_Vocab.place(x=100, y=70)

        Label_Meaning= tk.Label(border_blue, text="Meaning", bg="white", bd=5, font=("Arial Bold", 15))
        Label_Meaning.place(x=400, y=70)

        #bd is the entry border size

        v=StringVar()
        v.set(Update("Vocab"))
        Vocab_text= tk.Label(border_blue, width=30, height=15, bd=5, textvariable=v)
        Vocab_text.place( x=100, y=100)

        
        m=StringVar()
        m.set(Update("Mean"))
        Meaning_text= tk.Label(border_blue, width=30, height=15, bd=5, textvariable=m)
        Meaning_text.place( x=400, y=100)


    
        Button_add = tk.Button(border_blue, text="Add", font=("Arial",15), command=lambda:Add())
        Button_add.place(x=565, y=390)

        Button_del = tk.Button(border_blue, text="Delete", font=("Arial",15), command=lambda:Del())
        Button_del.place(x=620, y=390)

        Button_start = tk.Button (border_blue, text="Quiz", font=("Arial",15), command=lambda: controller.show_frame(Secondpage))
        Button_start.place(x=695, y=390)

        


class Secondpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #border
        border_red= tk.LabelFrame(self, bg="Red", bd=10)
        border_red.pack(fill="both", expand="yes", padx=10, pady=20)


        def Start_function():
            with open('quiz.json','r') as fp:
                quiz =json.load(fp)
                score = 0 
                for key in quiz:
                    mean= quiz[key]
                    q.set(question_dis(key))
                    key_input = simpledialog.askstring(title= ' meaning', prompt=' input meaning')
                    if key_input == mean:
                        score = score +1
                        v.set(question_meaning('correct'))
                    elif key_input != mean :
                        v.set(question_meaning(mean))
                score_total = (((score)/(len(quiz)))*100)
                score_precent= (str(score_total) +'%')
                score_conv = str(score_precent)
                s.set(final_score(score_conv))
                    

        def question_meaning(verdict):
            if verdict == 'correct':
                display = ('correct')
                return display
            elif verdict == None:
                display = ('')
                return display
            else:
                display = ('incorrect, the meaning is ' + str(verdict))
                return display

        def final_score(score):
            if score == 'blank':
                display= ('your final score will be displayed here')
            else:
                display= ('your final score is ' + score )
                return display



        def question_dis(key):
            if key == None:
                display=('please press the start button')
                return display
            else:
                display = ("what is the meaning of " + str(key))
                return display

        q=StringVar()
        q.set(question_dis(None))


        question_border= tk.Label(border_red, height=10, width=80, textvariable=q)
        question_border.place(x=100, y=100)

        v=StringVar()
        v.set(question_meaning(None))

        question_meaning_label= tk.Label(border_red, height= 5, width=80, textvariable=v)
        question_meaning_label.place(x=100, y=250)

        s=StringVar()
        s.set(final_score('blank'))

        final_score_label = tk.Label(border_red, height = 1, width =80, textvariable=s)
        final_score_label.place(x=100, y=350)

                
    
        Button_start = tk.Button (border_red, text="start", font=('Arial',15), command= lambda:Start_function())
        Button_start.place(x=485, y=390)

        Button_back = tk.Button (border_red, text="Back", font=("Arial",15), command=lambda: controller.show_frame(Firstpage))
        Button_back.place(x=585, y=390)

        

        








class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        #creating a window for each page

        window=tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize= 500)
        window.grid_columnconfigure(0, minsize=800)


        self.frames={}
        for F in (Firstpage, Secondpage):
            frame= F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if self.frames ==[]:
            print('Error in loading program')
        self.show_frame(Firstpage)

    def show_frame(self, controller):
        frame=self.frames[controller]
        frame.tkraise()









app = Application()
app.maxsize(1000,800)
app.mainloop()


# stopped at 20:19 of the multip window gui video

