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

        # Set up Feature selection using checkboxes and a text box for TEXT search
        # Text Retrieval


        # Checkboxes for audio and visual features
        label2 = Label(root, text="Select search tools")
        label2.pack()

        self.audio_mfcc = IntVar()
        self.audio_mfcc_button = Checkbutton(
            master, text="MFCC",
            variable=self.audio_mfcc)
        label_mfcc = Label(root, text="MFCC Weight")
        self.Emfcc = Entry(root, bd=5, width = 40) # to get string, use Emfcc.get()

        self.audio_energy = IntVar()
        self.audio_energy_button = Checkbutton(
            master, text="Energy",
            variable=self.audio_energy)
        label_energy = Label(root, text="Energy Weight")
        self.Eenergy = Entry(root, bd=5, width = 40) # to get string, use Emfcc.get()

        self.audio_zerocrossing = IntVar()
        self.audio_zerocrossing_button = Checkbutton(
            master, text="Zero Crossing",
            variable=self.audio_zerocrossing)
        label_zerocrossing = Label(root, text="Zero Crossing Weight")
        self.Ezerocrossing = Entry(root, bd=5, width = 40) # to get string, use Emfcc.get()

        self.mel = IntVar()
        self.mel_button = Checkbutton(
            master, text="Mel (Magnitude Spectrum)",
            variable=self.mel)

        label_mel = Label(root, text="Mel (Magnitude Spectrum) Weight")
        self.Emel = Entry(root, bd=5, width = 40) # to get string, use Emfcc.get()

        self.vc = IntVar()
        self.vc_button = Checkbutton(
            master, text="Visual Matching",
            variable=self.vc)
        label_vc = Label(root, text="Visual Matching Weight")
        self.Evc = Entry(root, bd=5, width = 40) # to get string, use Emfcc.get()        

        spacer = Label(root, text="______________________",font=(None, 10))        
        # Arrange the checkboxes
        self.audio_mfcc_button.pack(side='top')
        label_mfcc.pack()
        self.Emfcc.pack()
        spacer.pack()
        self.audio_energy_button.pack(side='top')
        label_energy.pack()
        self.Eenergy.pack()
        self.audio_zerocrossing_button.pack(side='top')
        label_zerocrossing.pack()
        self.Ezerocrossing.pack()
        self.mel_button.pack(side='top')
        label_mel.pack()
        self.Emel.pack()
        self.vc_button.pack(side='top')
        label_vc.pack()
        self.Evc.pack()
        self.master.mainloop()

    def browse_query_img(self):
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        self.filepath = filedialog.askopenfile(title='Choose an Video File').name

        # List of all frameIDs in the path that contains all video frames
        allframes = os.listdir(self.frame_storing_path)

        # Set videoname as video ID without its file extension
        self.videoname = self.filepath.strip().split("/")[-1].replace(".mp4","")

        # Save the query video's path and video name for processing in
        # query_logic.py
        self.query_logic.set_query_vid_path(self.filepath)
        self.query_logic.set_query_vid_name(self.videoname)

        # Set path to frame as '<path><videoname>-frame<frameindex>.jpg'
        # E.g. 'deeplearning/data/frame/1-frame0.jpg' for the first frame
        # of videoname '1'
        self.frames = []
        for frame in allframes:
            if self.videoname +"-frame" in frame:
                self.frames.append(self.frame_storing_path + frame)

        # Set up display grid for the video frames
        COLUMNS = len(self.frames)
        self.columns = COLUMNS
        image_count = 0

        # If a video has no frames, throw error
        if COLUMNS == 0:
            self.frames.append("none.png")
            print("Please extract the key frames for the selected video first!!!")
            COLUMNS = 1

        # Render every frame as a tile
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
        self.toggle_search = [0,0,0,0,0] # I don't know how many we'll need
        if (self.audio_mfcc.get() == 1):
            self.toggle_search[0] = 1
        if (self.audio_energy.get() == 1):
            self.toggle_search[1] = 1
        if (self.audio_zerocrossing.get() == 1):
            self.toggle_search[2] = 1
        if (self.mel.get() == 1):
            self.toggle_search[3] = 1
        if (self.vc.get() == 1):
            self.toggle_search[4] = 1

        # Run search operation using the QueryLogic class
        # Comment out as it may return error
        # results = self.query_logic.get_search_results(self.toggle_search, self.Emfcc.get())

        # Display venue of query video
        if self.columns == 0:
            print("Please extract the key frames for the selected video first!!!")
        else:
            # Please note that, you need to write your own classifier to estimate the venue category to show blow.
            if self.videoname == '1':
               venue_text = "Hello"
            elif self.videoname == '2':
                venue_text = 'It\'s'
            elif self.videoname == '4':
                venue_text = 'Me'

            # Set background and draw text with specified font type
            venue_img = Image.open("background.jpg")
            draw = ImageDraw.Draw(venue_img)
            font = ImageFont.truetype("Arial.ttf",size=66)
            draw.text((50,50), venue_text, (0, 0, 0), font=font)

            # Draw result image frames and venue labels
            resized = venue_img.resize((100, 100), Image.ANTIALIAS)
            tkimage =ImageTk.PhotoImage(resized)
            myvar = Label(self.query_img_frame, image=tkimage)
            myvar.image= tkimage
            myvar.grid(row=self.lastR, column=self.lastC+1)

        self.query_img_frame.mainloop()

"""
# Main point of execution
"""
root = Tk()
window = UI_class(root, search_path='deeplearning/data/video/',
                        frame_storing_path='deeplearning/data/frame/')
