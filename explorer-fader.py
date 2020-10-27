#!/usr/bin/env python3

# ------------------------------------------------------------------------------
#  Slideshow program for the Explorer projector unit. Displays pictures and
#  allows navigation through them based on 3 modes: time, altitude, and color
# ------------------------------------------------------------------------------

# from classes.capra_data_types import Picture, Hike
# from classes.sql_controller import SQLController
# from classes.sql_statements import SQLStatements
# from adafruit_mcp3xxx.analog_in import AnalogIn  # Reading values from MCP3008
# from gpiozero import Button             # Rotary encoder, detected as button
# from RPi import GPIO                    # GPIO pin detection for Raspberry Pi
# import adafruit_mcp3xxx.mcp3008 as MCP  # Interfacing with MCP3008
# import board                            # Dependancy of MCP3008
# import busio                            # Dependancy of MCP3008
# import digitalio                        # Dependancy of MCP3008

# Imports
from PIL import ImageTk, Image          # Pillow image functions
from tkinter import Tk, Canvas, Label, filedialog   # Tkinter, GUI framework in use
from time import sleep                  # Sleep
import datetime, math, os

# Database location
# DB = '/home/pi/Pictures/capra-projector.db'
# PATH = '/home/pi/Pictures'
PATH = '/Users/Jordan/Developer/eds/capra-video-tools/pictures/'

'''
class Application():
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def browse(self):

        filename = filedialog.askdirectory()

        self.filepath.config(state="normal")
        self.filepath.delete(0, tk.END)
        self.filepath.insert(tk.END, filename)
        self.filepath.config(state="disabled")


class VideoGenerator():
    def __init__(self, filepath, framerate):
        self.filepath = filepath
        self.framerate = framerate

        # make director to save video into
        dir = path.join(self.filepath, 'video')
        if not path.exists(dir):
            mkdir(dir)

    def generate_video(self):
        # get stacked images
        image_filepath = path.join(self.filepath, 'stacked', '*.jpg')
        files = glob.glob(image_filepath)
        files = natsorted(files)

        video = ImageSequenceClip(files, fps=self.framerate)
        video.write_videofile(
            path.join(self.filepath, 'video', 'capra_magic.mp4'), codec='mpeg4', audio=False)
        video.close()
'''

# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    # GLOBAL CLASS STATE VARIABLES (COUNTERS, BOOLS, ETC)
    TRANSITION_DELAY = 4000         # Autoplay time between pictures (in milliseconds)
    IS_TRANSITION_FORWARD = True    # Autoplay direction (forward or backward)
    PLAY = True                     # Autoplay (Play/Pause) bool
    IS_ACROSS_HIKES = False         # Is rotary encoder pressed down
    ROTARY_COUNT = 0                # Used exclusively for testing rotary encoder steps

    def __init__(self, win):
        # Setup the window
        self.window = win
        self.window.title("Capra Slideshow")
        self.window.geometry("1280x720")
        self.window.configure(background='purple')
        self.canvas = Canvas(root, width=1280, height=720, background="#888", highlightthickness=0)
        self.canvas.pack(expand='yes', fill='both')

        # Hardware control events
        self.window.bind('<Key>', self.keypress)

        # Initialization for database implementation
        # self.sql_controller = SQLController(database=DB)
        # self.picture_starter = self.sql_controller.get_first_time_picture_in_hike(10)
        # self.picture_starter = self.sql_controller.get_first_time_picture_in_hike_with_offset(10, OFFSET)
        # self.picture = self.sql_controller.next_time_picture_in_hike(self.picture_starter)

        self.picture_starter = "first picture"
        self.picture = "next picture in directory"

        # Initialization for images and associated properties
        self.alpha = 0

        self.fileList = self.getFileList()
        print(self.fileList)

        # Add the photo to the screen
        self.current_raw_mid = Image.open(self.fileList[0], 'r')
        self.next_raw_mid = Image.open(self.fileList[1], 'r')

        self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
        self.image_label_mid = Label(master=self.canvas, image=self.display_photo_image_mid, borderwidth=0)
        self.image_label_mid.pack(side='right', fill='both', expand='yes')

        # for filename in os.listdir(DIR):
        #     print(filename)

        # for entry in os.scandir(DIR):
        #     if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
        #         print(entry.path)

        # for filename in os.listdir(DIR):
        #     if filename.endswith(".jpg"):
        #         print(os.path.join(DIR, filename))
        #         continue
        #     else:
        #         continue

        # root.after(15, func=self.fade_image)
        # root.after(self.TRANSITION_DELAY, func=self.auto_play_slideshow)



        # NOT NEEDED ANYMORE
        # Initialize current and next images
        # self.current_raw_top = Image.open(self._build_filename(self.picture_starter.camera1), 'r')
        # self.next_raw_top = Image.open(self._build_filename(self.picture.camera1), 'r')


        # self.current_raw_bot = Image.open(blank_path, 'r')
        # self.next_raw_bot = Image.open(blank_path, 'r')
        # self.current_raw_bot = Image.open(self._build_filename(self.picture_starter.camera3), 'r')
        # self.next_raw_bot = Image.open(self._build_filename(self.picture.camera3), 'r')

        # Display the first 3 images to the screen
        # self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
        # self.image_label_top = Label(master=self.canvas, image=self.display_photo_image_top, borderwidth=0)
        # self.image_label_top.pack(side='right', fill='both', expand='yes')
        # self.image_label_top.place(x=20, rely=0.0, anchor='nw')





        # self.image_label_mid.place(x=20, y=405, anchor='nw')

        # self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
        # self.image_label_bot = Label(master=self.canvas, image=self.display_photo_image_bot, borderwidth=0)
        # self.image_label_bot.pack(side='right', fill='both', expand='yes')
        # self.image_label_bot.place(x=20, y=810, anchor='nw')

        # Hike labels
        # self.label_mode = Label(self.canvas, text='Modes: ')
        # self.label_hike = Label(self.canvas, text='Hike: ')
        # self.label_index = Label(self.canvas, text='Index: ')
        # self.label_alt = Label(self.canvas, text='Altitude: ')
        # self.label_date = Label(self.canvas, text='Date: ')

        # self.label_mode.place(relx=1.0, y= 0, anchor='ne')
        # self.label_hike.place(relx=1.0, y=22, anchor='ne')
        # self.label_index.place(relx=1.0, y=44, anchor='ne')
        # self.label_alt.place(relx=1.0, y=66, anchor='ne')
        # self.label_date.place(relx=1.0, y=88, anchor='ne')

        # Start background threads which will continue for life of the class
        # root.after(0, func=self.check_accelerometer)
        # root.after(10, func=self.update_text)


        # root.after(0, func=self.check_mode)

    def getFileList(self):
        directorypath = filedialog.askdirectory(title="Select directory of photos")
        # print(directorypath)

        fileList = []
        for file in os.listdir(directorypath):
            if file.endswith(".jpg"):
                fullpath = os.path.join(directorypath, file)
                fileList.append(fullpath)

        fileList.sort()

        return fileList

    def _build_next_raw_images(self, next_picture):
        # print('build images')
        # self.next_raw_top = Image.open(self._build_filename(next_picture.camera1), 'r')
        self.next_raw_mid = Image.open(self._build_filename(next_picture.camera2), 'r')
        # self.next_raw_mid = Image.open(self._build_filename(next_picture.camera3), 'r')
        # self.next_raw_bot = Image.open(blank_path, 'r')

    def _build_filename(self, end_of_path: str) -> str:
        return '{p}{e}'.format(p=PATH, e=end_of_path)
        # return '{e}'.format(e=end_of_path)

    # Loops for the life of the program, fading between the current image and the NEXT image
    def fade_image(self):
        # print('Fading the image at alpha of: ', self.alpha)
        # print(time.time())
        if self.alpha < 1.0:
            # Top image
            # self.current_raw_top = Image.blend(self.current_raw_top, self.next_raw_top, self.alpha)
            # self.current_raw_top = self.next_raw_top
            # self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
            # self.image_label_top.configure(image=self.display_photo_image_top)

            # Middle image
            self.current_raw_mid = Image.blend(self.current_raw_mid, self.next_raw_mid, self.alpha)
            # self.current_raw_mid = self.next_raw_mid
            self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
            self.image_label_mid.configure(image=self.display_photo_image_mid)

            # Bottom image
            # self.current_raw_bot = Image.blend(self.current_raw_bot, self.next_raw_bot, self.alpha)
            # self.current_raw_bot = self.next_raw_bot
            # self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
            # self.image_label_bot.configure(image=self.display_photo_image_bot)

            self.alpha = self.alpha + 0.0417
            # self.alpha = self.alpha + 0.0209
        root.after(83, self.fade_image)

    # def update_text(self):
    #     self.determine_switch_mode()
    #     if self.MODE == 0:
    #         mode = 'Mode: Time'
    #     elif self.MODE == 1:
    #         mode = 'Mode: Altitude'
    #     elif self.MODE == 2:
    #         mode = 'Mode: Color'
    #     else:
    #         mode = 'Mode: ERROR'

    #     hike = 'Hike {n}'.format(n=self.picture.hike_id)

    #     hike_sz = self.sql_controller.get_size_of_hike(self.picture)
    #     index = '{x} / {n}'.format(x=self.picture.index_in_hike, n=hike_sz)

    #     altitude = '{a}m'.format(a=self.picture.altitude)

    #     value = datetime.datetime.fromtimestamp(self.picture.time)
    #     date_time = value.strftime('%-I:%M:%S%p on %d %b, %Y')
    #     date = '{d}'.format(d=date_time)

    #     self.label_mode.configure(text=mode)
    #     self.label_hike.configure(text=hike)
    #     self.label_index.configure(text=index)
    #     self.label_alt.configure(text=altitude)
    #     self.label_date.configure(text=date)

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
        if event.keycode == 114:  # Right / Next
            # print('right')
            self.picture = self.sql_controller.get_next_picture(
                    current_picture=self.picture, mode=self.MODE, is_across_hikes=self.IS_ACROSS_HIKES)
            self._build_next_raw_images(self.picture)
            self.alpha = .2                     # Resets amount of fade between pictures
            self.picture.print_obj()            # This is a print()
        elif event.keycode == 113:  # Left / Previous
            # print('left')
            self.picture = self.sql_controller.get_previous_picture(
                    current_picture=self.picture, mode=self.MODE, is_across_hikes=self.IS_ACROSS_HIKES)
            self._build_next_raw_images(self.picture)
            self.alpha = .2                     # Resets amount of fade between pictures
            self.picture.print_obj()            # This is a print()
        else:
            print(event)


# Create the root window
root = Tk()

root.attributes("-fullscreen", False)
root.bind("<Escape>", exit)
root.update()  # Needed to fix issue with dialog not going away
slide_show = Slideshow(root)
root.mainloop()
