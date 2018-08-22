import time
import tkinter as tk
from PIL import Image, ImageTk


class Player(object):
    def __init__(self, width, height, fps, frames):
        self.width = width
        self.height = height
        self.frame_duration = int(1000.0/fps)

        self.frames = frames
        self.current_frame = len(frames)-1
        print('have {} frames'.format(len(frames)))

        self.root = tk.Tk()
        self.label = tk.Label(self.root)
        self.label.pack(side="bottom", fill="both", expand="yes")
        self.root.title('{} frames'.format(len(self.frames)))

    def play(self):
        self.last_pts = time.time()
        self.root.after(0, self.update_frame)
        self.root.mainloop()

    def update_frame(self):
        if len(self.frames) <= 1:
            return

        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        next_frame = self.frames[self.current_frame]

        frame_img = ImageTk.PhotoImage(Image.frombytes(
            'L', (self.width, self.height), next_frame.astype('b').tostring()))
        self.label.configure(image=frame_img)
        self.label.image = frame_img

        pts = time.time()
        # print('frame pts={} dur={}'.format(pts, pts - self.last_pts))
        self.last_pts = pts

        self.root.after(self.frame_duration, self.update_frame)

    def add_frame(self, frame):
        self.frames.append(frame)
        self.root.title('{} frames'.format(len(self.frames)))
