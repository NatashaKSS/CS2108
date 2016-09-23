# import the necessary packages
from pyimagesearch.querylogic import QueryLogic
import cv2
from Tkinter import *
import tkFileDialog
import os
from PIL import Image, ImageTk


class UI_class:

    def __init__(self, master, search_path):
        self.querylogic = QueryLogic()
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()

        # Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)

        self.bbutton = Button(topframe, text=" Choose an image ",
                              command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1, padx = 10)
        self.bbutton.config(height=2, width=20)

        self.cbutton = Button(topframe, text=" Search ",
                              command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=3, padx = 10)
        self.cbutton.config(height=2, width=10)
        downspace = Label(topframe).grid(row=2, columnspan=4)

#text input
        label1 = Label(root, text="Text Input")
        E1 = Entry(root, bd=5)
        def getWord():
            print E1.get()

        self.submit = Button(root, text="Submit", command=getWord)
        self.submit.grid(pady = 10)


        label1.pack()
        E1.pack()
        self.submit.pack()


        self.master.mainloop()

    def browse_query_img(self):

        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(
            title='Choose an Image File').name
        
        self.image_attrs = self.querylogic.get_image_attrs(self.filename)

        # show query image
        image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)
        image_label.pack()

        self.query_img_frame.mainloop()

    def show_results_imgs(self):
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()
        
        results = self.querylogic.get_search_results(self.image_attrs)

        # show result pictures
        COLUMNS = 4
        image_count = 0
        for (score, resultID) in results:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            im = Image.open(self.search_path + os.sep + resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.result_img_frame.mainloop()
    

    


root = Tk()
window = UI_class(root, 'dataset')
