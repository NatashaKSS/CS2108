# import the necessary packages
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

import os
import query_logic as query_logic_package

class UI_class:
    exist_prev_query = False
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

        #self.audio_mfcc = IntVar()
        #self.audio_mfcc_button = Checkbutton(master, text="MFCC", variable=self.audio_mfcc)
        label_mfcc = Label(root, text="MFCC Weight")
        self.Emfcc = Entry(root, bd=5, width = 10) # to get string, use self.Emfcc.get()

        #self.audio_energy = IntVar()
        #self.audio_energy_button = Checkbutton(master, text="Energy", variable=self.audio_energy)
        label_energy = Label(root, text="Energy Weight")
        self.Eenergy = Entry(root, bd=5, width = 10) # to get string, use self.Eenergy.get()

        #self.audio_zerocrossing = IntVar()
        #self.audio_zerocrossing_button = Checkbutton(master, text="Zero Crossing", variable=self.audio_zerocrossing)
        label_zerocrossing = Label(root, text="Zero Crossing Weight")
        self.Ezerocrossing = Entry(root, bd=5, width = 10) # to get string, use self.Ezerocrossing.get()

        #self.mel = IntVar()
        #self.mel_button = Checkbutton(master, text="Mel (Magnitude Spectrum)", variable=self.mel)
        label_mel = Label(root, text="Mel (Magnitude Spectrum) Weight")
        self.Emel = Entry(root, bd=5, width = 10) # to get string, use self.Emel.get()

        #self.visual = IntVar()
        #self.visual_button = Checkbutton(master, text="Visual Matching", variable=self.visual)
        label_visual = Label(root, text="Visual Matching Weight")
        self.Evisual = Entry(root, bd=5, width = 10) # to get string, use self.Evisual.get()

        spacer1 = Label(root, text="________________________________________________________________________________________________________________________________________________",font=(None, 1))
        spacer2 = Label(root, text="________________________________________________________________________________________________________________________________________________",font=(None, 1))
        spacer3 = Label(root, text="________________________________________________________________________________________________________________________________________________",font=(None, 1))
        spacer4 = Label(root, text="________________________________________________________________________________________________________________________________________________",font=(None, 1))

        # Arrange the checkboxes
        #self.audio_mfcc_button.pack(side='top')
        label_mfcc.pack()
        self.Emfcc.pack()
        spacer1.pack()
        #self.audio_energy_button.pack(side='top')
        label_energy.pack()
        self.Eenergy.pack()
        spacer2.pack()
        #self.audio_zerocrossing_button.pack(side='top')
        label_zerocrossing.pack()
        self.Ezerocrossing.pack()
        spacer3.pack()
        #self.mel_button.pack(side='top')
        label_mel.pack()
        self.Emel.pack()
        spacer4.pack()

        label_visual.pack()
        self.Evisual.pack()

        # Check buttons for ACOUSTIC, VISUAL AND TEXT features
        self.acoustic = IntVar()
        self.acoustic_button = Checkbutton(master, text="Acoustic", variable=self.acoustic)
        self.acoustic_button.pack(side='top')

        self.visual = IntVar()
        self.visual_button = Checkbutton(master, text="Visual", variable=self.visual)
        self.visual_button.pack(side='top')

        self.text = IntVar()
        self.text_button = Checkbutton(master, text="Text", variable=self.text)
        self.text_button.pack(side='top')

        self.master.mainloop()

    def browse_query_img(self):
        if (self.exist_prev_query):
            self.query_img_frame.destroy()
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
        print (self.frames)
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
        self.exist_prev_query = True
        self.query_img_frame.mainloop()

    def show_venue_category(self):
        self.toggle_search = [self.acoustic.get(), self.visual.get(), self.text.get()]
        self.audio_weights = [self.Emfcc.get(), self.Eenergy.get(), self.Ezerocrossing.get(), self.Emel.get()]

        print("Swtiches: ", self.acoustic.get(), self.visual.get(), self.text.get())
        print("Acoustic Weights: ", self.Emfcc.get(), self.Eenergy.get(), self.Ezerocrossing.get(), self.Emel.get())
        print()

        # Run search operation using the QueryLogic class
        results = self.query_logic.get_search_results(self.toggle_search, self.audio_weights)

        # Display venue of query video
        if self.columns == 0:
            print("Please extract the key frames for the selected video first!!!")
        else:
            # Please note that, you need to write your own classifier to estimate the venue category to show below.
            # final_venue = results[0]
            # umbrella_group_venues = results[1]

            if self.videoname == '1':
               venue_text = "Hello"
            elif self.videoname == '2':
                venue_text = 'It\'s'
            elif self.videoname == '4':
                venue_text = 'Me'

            # Set background and draw text with specified font type
            venue_img = Image.open("background.jpg")
            draw = ImageDraw.Draw(venue_img)
            font = ImageFont.truetype("Avenir.otf",size=66)
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
