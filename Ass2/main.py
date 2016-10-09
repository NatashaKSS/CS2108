# import the necessary packages
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

import os
import query_logic as query_logic_package

class UI_class:
    def __init__(self, master, search_path, frame_storing_path):
        # Initialize required classes
        self.query_logic = query_logic_package.QueryLogic()

        # Initialize paths to datasets
        self.search_path = search_path
        self.frame_storing_path = frame_storing_path

        # Set up Tkinter main object Tk()
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()

        # Set up Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an video ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Estimate its venue ", command=self.show_venue_category)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()

    def browse_query_img(self):
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        self.filename = filedialog.askopenfile(title='Choose an Video File').name

        # List of all frameIDs in the path that contains all video frames
        allframes = os.listdir(self.frame_storing_path)

        # Set videoname as video ID without its file extension
        self.videoname = self.filename.strip().split("/")[-1].replace(".mp4","")

        # Set path to frame as '<path><videoname>-frame<frameindex>.jpg'
        # E.g. 'deeplearning/data/frame/1-frame0.jpg' for
        # videoname '1''s first frame
        self.frames = []
        for frame in allframes:
            if self.videoname +"-frame" in frame:
                self.frames.append(self.frame_storing_path + frame)

        # Set up display grid for the video frames
        COLUMNS = len(self.frames)
        self.columns = COLUMNS
        image_count = 0

        if COLUMNS == 0:
            self.frames.append("none.png")
            print("Please extract the key frames for the selected video first!!!")
            COLUMNS = 1

        for frame in self.frames:
            r, c = divmod(image_count, COLUMNS)

            try:
                im = Image.open(frame)
                resized = im.resize((100, 100), Image.ANTIALIAS)
                tkimage = ImageTk.PhotoImage(resized)

                myvar = Label(self.query_img_frame, image=tkimage)
                myvar.image = tkimage
                myvar.grid(row=r, column=c)

                image_count += 1
                self.lastR = r
                self.lastC = c

            except Exception as e:
                continue

        self.query_img_frame.mainloop()


    def show_venue_category(self):
        if self.columns == 0:
            print("Please extract the key frames for the selected video first!!!")
        else:
            # Please note that, you need to write your own classifier to estimate the venue category to show blow.
            if self.videoname == '1':
               venue_text = "Home"
            elif self.videoname == '2':
                venue_text = 'Bridge'
            elif self.videoname == '4':
                venue_text = 'Park'

            venue_img = Image.open("venue_background.jpg")
            draw = ImageDraw.Draw(venue_img)

            font = ImageFont.truetype("Arial.ttf",size=66)

            draw.text((50,50), venue_text, (0, 0, 0), font=font)

            resized = venue_img.resize((100, 100), Image.ANTIALIAS)
            tkimage =ImageTk.PhotoImage(resized)

            myvar = Label(self.query_img_frame, image=tkimage)
            myvar.image= tkimage
            myvar.grid(row=self.lastR, column=self.lastC+1)

        self.query_img_frame.mainloop()

root = Tk()
window = UI_class(root, search_path='deeplearning/data/video/',
                        frame_storing_path='deeplearning/data/frame/')
