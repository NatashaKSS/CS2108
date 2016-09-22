# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import cv2
from Tkinter import *
import tkFileDialog
import os
from PIL import Image, ImageTk


class UI_class:

    def __init__(self, master, search_path):
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()

        # Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton = Button(topframe, text=" Choose an image ",
                              command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ",
                              command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()

    def browse_query_img(self):

        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(
            title='Choose an Image File').name
        
        self.get_image_attrs(self.filename)

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
        
        results = self.get_search_results()

        # show result pictures
        COLUMNS = 5
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
    
    def get_image_attrs(self, file_path):
        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        # load the query image and describe it
        query = cv2.imread(file_path)
        self.queryfeatures = cd.describe(query)
    
    def get_search_results(self):
        # perform the search
        searcher = Searcher("index.csv")
        results = searcher.search(self.queryfeatures)
        return results
    


root = Tk()
window = UI_class(root, 'dataset')
