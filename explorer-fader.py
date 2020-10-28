#!/usr/bin/env python3

# ------------------------------------------------------------------------------
#  Manual slideshow program for creating specific scene for the Capra videos
# ------------------------------------------------------------------------------

# Imports
from PIL import ImageTk, Image          # Pillow image functions
from tkinter import Tk, Canvas, Label, filedialog   # Tkinter, GUI framework in use
from time import sleep                  # Sleep
import datetime, math, os


# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    # GLOBAL CLASS STATE VARIABLES (COUNTERS, BOOLS, ETC)
    TRANSITION_DELAY = 4000         # Autoplay time between pictures (in milliseconds)
    IS_TRANSITION_FORWARD = True    # Autoplay direction (forward or backward)
    PLAY = True                     # Autoplay (Play/Pause) bool
    # IS_ACROSS_HIKES = False         # Is rotary encoder pressed down
    # ROTARY_COUNT = 0                # Used exclusively for testing rotary encoder steps

    def __init__(self, win):
        # Setup the window
        self.window = win
        self.window.title("Explorer Fader")
        self.window.geometry("1280x720")
        self.window.configure(background='purple')
        self.canvas = Canvas(root, width=1280, height=720, background="#888", highlightthickness=0)
        self.canvas.pack(expand='yes', fill='both')
        self.window.bind('<Key>', self.keypress)

        # Initialization for images and associated properties
        self.alpha = 0

        # Get list of all relevant files
        self.fileList = self.getFileList()
        self.index = 0
        # print(self.fileList)
        # print(len(self.fileList))

        # Add the first photo to the screen
        self.current_raw_mid = Image.open(self.fileList[self.index], 'r')
        self.next_raw_mid = Image.open(self.fileList[self.index], 'r')

        self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
        self.image_label_mid = Label(master=self.canvas, image=self.display_photo_image_mid, borderwidth=0)
        self.image_label_mid.pack(side='right', fill='both', expand='yes')

        # Hike labels
        # self.label_index = Label(self.canvas, text='Index: ')
        # self.label_index.place(relx=1.0, y=20, anchor='ne')

        # Start background threads which will continue for life of the class
        root.after(30, func=self.fade_image)
        # root.after(self.TRANSITION_DELAY, func=self.auto_play_slideshow)
        # root.after(10, func=self.update_text)

    def getFileList(self):
        directorypath = filedialog.askdirectory(title="Select directory of photos")

        fileList = []
        for file in os.listdir(directorypath):
            if file.endswith(".jpg"):
                fullpath = os.path.join(directorypath, file)
                fileList.append(fullpath)
        fileList.sort()

        return fileList

    def nextPicture(self):
        print('next')
        self.alpha = 0.1  # Resets amount of fade between pictures
        if self.index + 1 >= len(self.fileList):
            self.index = 0
        else:
            self.index += 1
        self.next_raw_mid = Image.open(self.fileList[self.index], 'r')

    def previousPicture(self):
        print('previous')
        self.alpha = 0.3  # Resets amount of fade between pictures
        if self.index - 1 < 0:
            self.index = len(self.fileList) - 1
        else:
            self.index -= 1
        self.next_raw_mid = Image.open(self.fileList[self.index], 'r')

    # Loops for the life of the program, fading between the current image and the NEXT image
    def fade_image(self):
        # print('Fading the image at alpha of: ', self.alpha)
        # print(time.time())
        if self.alpha < 1.0:
            # Middle image
            self.current_raw_mid = Image.blend(self.current_raw_mid, self.next_raw_mid, self.alpha)
            self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
            self.image_label_mid.configure(image=self.display_photo_image_mid)

            # TODO - how long the image hangs around
            # Lower the longer a piece stays on screen
            # Higher the faster the bit of an image leaves
            # self.alpha = self.alpha + 0.0417
            # self.alpha = self.alpha + 0.0209
            self.alpha = self.alpha + 0.001
        # TODO - Change this value to affect the spee of the fade
        # Lower the number the quicker the fade
        # Higher the number the slower the fade
        root.after(40, self.fade_image)

    # def update_text(self):
    #     index = '{x} / {n}'.format(x=self.picture.index_in_hike, n=hike_sz)
    #     self.label_index.configure(text=index)
    #     root.after(500, self.update_text)

    # TODO - track down where the random number being printed to the terminal is coming from
    def auto_play_slideshow(self):
        # print('Auto incremented slideshow')
        if (self.PLAY):
            if self.IS_TRANSITION_FORWARD:          # Advance forward on autoplay
                self.picture = self.sql_controller.get_next_picture(
                    current_picture=self.picture, mode=self.MODE, is_across_hikes=self.IS_ACROSS_HIKES)
                self._build_next_raw_images(self.picture)
                self.alpha = .2
                self.picture.print_obj()            # This is a print()
            else:                                   # Advance backward on autoplay
                self.picture = self.sql_controller.get_previous_picture(
                    current_picture=self.picture, mode=self.MODE, is_across_hikes=self.IS_ACROSS_HIKES)
                self._build_next_raw_images(self.picture)
                self.alpha = .2
                self.picture.print_obj()            # This is a print()

        root.after(self.TRANSITION_DELAY, self.auto_play_slideshow)

    def keypress(self, event):
        if event.keycode == 8189699:  # Right/Next  TODO: 114 - alternative code
            self.nextPicture()
        elif event.keycode == 8124162:  # Left/Previous  TODO: 113 - alternative code
            self.previousPicture()
        else:
            print(event)


# Create the root window
root = Tk()

root.attributes("-fullscreen", False)
root.bind("<Escape>", exit)
root.update()  # Needed to fix issue with dialog not going away
slide_show = Slideshow(root)
root.mainloop()
