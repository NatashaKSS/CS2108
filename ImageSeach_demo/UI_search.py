# import the necessary packages
from pyimagesearch.querylogic import QueryLogic
import cv2
from Tkinter import *
import tkFileDialog
import os
from PIL import Image, ImageTk

#Keyword text: E1.get()
#Toggle search(selected = 1, unselected = 0): searchVC, searchVK, searchCH

class UI_class:

    def __init__(self, master, search_path):
        self.querylogic = QueryLogic()
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)


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
        label1 = Label(root, text="Text Input for Visual Concept (Text)")
        self.E1 = Entry(root, bd=5, width = 30)
        #to get string, use E1.get()

#Checkboxes
        label2 = Label(root, text="Select search tools")
        label2.pack()
        self.searchVCImage = IntVar()

        self.vci = Checkbutton(
            master, text="Visual Concept (Image)",
            variable=self.searchVCImage)

        self.searchVCText = IntVar()
        self.vct = Checkbutton(
            master, text="Visual Concept (Text)",
            variable=self.searchVCText)

        self.searchVK = IntVar()
        self.vk = Checkbutton(
            master, text="Visual Keyword",
            variable=self.searchVK)

        self.searchCH = IntVar()
        self.ch = Checkbutton(
            master, text="Color Histogram",
            variable=self.searchCH)
        label1.pack()
        self.E1.pack()

        self.vk.pack(side='top')
        self.ch.pack(side='top')
        self.vct.pack(side='top')
        self.vci.pack(side='top')
        topframe.pack(side='bottom')
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
        self.toggle_search = [0,0,0,0]
        if (self.searchVK.get() == 1):
            self.toggle_search[0] = 1
        if (self.searchCH.get() == 1):
            self.toggle_search[1] = 1
        if (self.searchVCText.get() == 1):
            self.toggle_search[2] = 1
        if (self.searchVCImage.get() == 1):
            self.toggle_search[3] = 1
        print self.toggle_search
        print self.E1.get()
        results = self.querylogic.get_search_results(self.image_attrs, self.toggle_search, self.E1.get())

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
