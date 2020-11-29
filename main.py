#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser, Menu, Spinbox, scrolledtext, messagebox as mb, filedialog as fd

import os
import glob
from PIL import Image, ImageTk

#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""
    #===========================================
    def __init__(self, title, icon, theme):
        super().__init__()
        self.init_config()
        self.style.theme_use(theme)
        self.title(title)
        self.iconbitmap(icon)
        self.init_UI()
        self.init_events()

    # INITIALIZER ==============================
    @classmethod
    def create_app(cls, app):
        return cls(app['title'], app['icon'], app['theme'])

    #===========================================
    def init_config(self):
        self.resizable(True, True)
        self.geometry('800x600+300+50')
        self.style = ttk.Style(self)

    #===========================================
    def init_events(self):
        self.listbox.bind('<<ListboxSelect>>', self.evt__show_img)
        self.listbox.bind('<Control-d>', self.evt__delete_item)

    def init_UI(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor=tk.W)

        self.list_of_png = glob.glob(r'*.png')
        self.listbox = tk.Listbox(self.frame)

        for img in self.list_of_png:
            self.listbox.insert(0, img)

        self.listbox.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)

    # EVENTS ------------------------------------
    def im__get_screen_size(self):
        """Returns the width and height of the screen to set images
        and canvas alike it: called by root.bind <Configure>"""
        if self.winfo_width() > 200 and self.winfo_height() > 30:
            screen_w = self.winfo_width() - 200
            screen_h = self.winfo_height() - 30
        else:
            screen_w = 200
            screen_h = 30
        return screen_w, screen_h

    # EVENTS ------------------------------------
    def evt__show_img(self, event):
        n = self.listbox.curselection()
        filename = self.listbox.get(n)

        im = Image.open(filename)
        im = im.resize(tuple(self.im__get_screen_size()), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(im)
        image_w, image_h = image.width(), image.height()

        self.canvas.image = image
        self.canvas.config(width=image_w, height=image_h)
        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
        self.bind('<Configure>', self.evt__show_img)

    def evt__delete_item(self, event):
        n = self.listbox.curselection()
        os.remove(self.listbox.get(n))
        self.listbox.delete(n)


#===========================
# Start GUI
#===========================

def main(config):
    app = App.create_app(config)
    app.mainloop()

if __name__ == '__main__':
    main({
        'title' : 'Image Browser Version 1.0',
        'icon' : 'python.ico',
        'theme' : 'clam'
        })