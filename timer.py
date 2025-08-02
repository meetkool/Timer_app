import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import time
import os
from datetime import datetime
import json
from tkinter import font as tkfont
import webbrowser

from PIL import Image, ImageTk
import tkinter as tk

import os
import sys

# root = tk.Tk()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class CustomMessageBox(tk.Toplevel):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title(title)
        self.geometry("400x300")  # Larger size
        self.configure(bg='#1a1a1a')
        
        # Make dialog modal
        self.transient(self.master)
        self.grab_set()
        
        # Message
        msg_frame = tk.Frame(self, bg='#1a1a1a')
        msg_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        msg_label = tk.Label(
            msg_frame, 
            text=message,
            font=("Arial", 12),
            wraplength=360,  # Allow text wrapping
            justify=tk.CENTER,
            bg='#1a1a1a',
            fg='white'
        )
        msg_label.pack(expand=True, fill=tk.BOTH)
        
        # OK button
        button_frame = tk.Frame(self, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=self.destroy,
            font=("Arial", 12),
            bg='#ff6600',
            fg='white',
            width=10,
            height=1
        )
        ok_button.pack()
        
        # Center the dialog on screen
        self.center_window()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

class CPPracticeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CP Practice App")
        self.master.geometry("400x550")
        self.master.configure(bg='white')




        
        self.show_central_menu()
        # Input field for total problems
        # self.total_problems_label = tk.Label(self.master, text="Enter total problems:")
        # self.total_problems_label.pack(pady=10)
        # self.total_problems_entry = tk.Entry(self.master)
        # self.total_problems_entry.pack(pady=10)

        # # Start button to begin the program
        # self.start_program_button = tk.Button(self.master, text="Start", command=self.start_program)
        # self.start_program_button.pack(pady=10)
        self.links_frame = None
        self.current_section = None
        # self.current_section = None

        


        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.current_session_file = None


        # self.create_menu()
        # self.current_section = None


    def show_sample_links(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.configure(bg='#1a1a1a')
        
        # Create main frame
        main_frame = tk.Frame(self.master, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg='#1a1a1a')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create frame for links
        links_frame = tk.Frame(canvas, bg='#1a1a1a')
        canvas.create_window((0, 0), window=links_frame, anchor="nw")

        # Add mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        # Create a file named 'links.txt' in the same directory as timer.py
        # Add the following line to links.txt:
        # https://www.techinterviewhandbook.org/grind75

        with open('links.txt', 'r') as file:
            daily_link = file.read().strip()

        daily_button = tk.Button(links_frame, text="all the links ", command=lambda: self.open_link(daily_link),
                                 font=("Arial", 14, "bold"), fg='white', bg='#ff6600', padx=10, pady=5)
        
        daily_button.pack(pady=20)

        # To compile with PyInstaller, use the following command:
        # pyinstaller --add-data "links.txt:." timer.py        daily_button.pack(pady=20)
        # Sample links
        resource_links = {
            "OS Development": [
                ("OS Nice", "https://www.youtube.com/watch?v=V8VyvowFh88"),
                ("Dave Poo - C++ Hardware Programming", "https://www.youtube.com/c/DavePoo/videos"),
            ],
            "Digital Computer Electronics": [
                ("IIT Course", "https://www.youtube.com/watch?v=TH9nd-KdVHs&list=PL2DC54ABD5C0221FE"),
                ("Additional Course", "https://www.youtube.com/watch?v=oNh6V91zdPY&list=PLbRMhDVUMnge4gDT0vBWjCb3Lz0HnYKkX"),
                ("Neso Academy", "https://www.youtube.com/watch?v=M0mx8S05v60&list=PLBlnK6fEyqRjMH3mWf6kwqiTbT798eAOm"),
            ],
            "Electronics Courses": [
                ("Basic Electronics", "https://www.youtube.com/watch?v=r-X9coYTOV4&list=PLah6faXAgguOeMUIxS22ZU4w5nDvCl5gs"),
                ("Advanced Electronics", "https://www.youtube.com/watch?v=eFPTBATfX70&list=PLwjK_iyK4LLCAN5TddEZyliChEMpF0oOL"),
                ("Additional Course", "https://www.youtube.com/watch?v=AfQxyVuLeCs&list=PL9F74AFA03AA06A11"),
            ],
            "8-bit Computer": [
                ("Ben Eater", "https://eater.net/8bit/"),
                ("MadMaxx", "https://www.youtube.com/watch?v=bCVT1BtlZn0&list=PLNUL7DzXzp_J4TztZYOVtayTfp0DV1z5H"),
                ("AM Technology", "https://www.youtube.com/c/AMTechnology/playlists"),
                ("LiveOverflow", "https://www.youtube.com/user/LiveOverflowCTF"),
                ("Esperantanaso", "https://www.youtube.com/user/Esperantanaso/videos"),
                ("James Sharman", "https://www.youtube.com/channel/UCeRXQ_B5WZD3yjPly45myvg"),
                ("Slu4", "https://www.youtube.com/channel/UCXYQcMpUBT3aaQKfmAVJNow"),
                ("Stefan Noack", "https://www.youtube.com/c/StefanNoack/videos"),
            ],
            "Assembly Language": [
                ("Assembly Tutorial 1", "https://www.youtube.com/watch?v=mWeh3_ITG7M&list=PL25E6AC923586A2F6&index=1"),
                ("8051 Assembly", "https://www.youtube.com/watch?v=X8vAUlSTUcc&list=PLnF3iL9xWR2vPmEzIEGuoTeFPf-V7IeKx"),
                ("x86 Assembly Introduction", "https://www.youtube.com/watch?v=vWlAg-pwMsM&list=PLan2CeTAw3pFOq5qc9urw8w7R-kvAT8Yb"),
                ("Assembly Tutorial 2", "https://www.youtube.com/watch?v=rxsBghsrvpI&list=PLKK11Ligqitg9MOX3-0tFT1Rmh3uJp7kA"),
                ("Assembly Tutorial 3", "https://www.youtube.com/watch?v=mHC4-W3OUTQ&list=PLPedo-T7QiNsIji329HyTzbKBuCAHwNFC&index=2"),
            ],
            "Operating System Development": [
                ("Little OS Book", "https://littleosbook.github.io/"),
                ("OS Tutorial", "https://github.com/cfenollosa/os-tutorial"),
                ("OS Development Lectures", "https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf"),
                ("Assembly OS Easy", "https://github.com/leodenglovescode/Assembly_OS_EASY"),
                ("Cosmos OS", "https://www.gocosmos.org/"),
                ("Glad Code", "https://gladcode.dev/"),
            ],
            "OS Development Playlists": [
                ("Playlist 1", "https://www.youtube.com/watch?v=wz9CZBeXR6U&list=PLZQftyCk7_SeZRitx5MjBKzTtvk0pHMtp&index=2"),
                ("Playlist 2", "https://www.youtube.com/watch?v=rWFR4NC20UA&list=PLxN4E629pPnKKqYsNVXpmCza8l0Jb6l8-&index=2"),
                ("Playlist 3", "https://www.youtube.com/watch?v=Lke3QOytgcQ&list=PLmlvkUN3-1MNKwINqdCDtTdNDjfBmWcZA&index=1"),
                ("Playlist 4", "https://www.youtube.com/watch?v=rr-9w2gITDM&list=PLBK_0GOKgqn3hjBdrf5zQ0g7UkQP_KLC3"),
                ("Playlist 5", "https://www.youtube.com/watch?v=_xlO9MawAqY&list=PLKbvCgwMcH7BX6Z8Bk1EuFwDa0WGkMnrz"),
                ("Playlist 6", "https://www.youtube.com/watch?v=1rnA6wpF0o4&list=PLHh55M_Kq4OApWScZyPl5HhgsTJS9MZ6M"),
            ],
            "Linux Distribution Development": [
                ("Linux From Scratch", "https://www.linuxfromscratch.org/lfs/view/stable/"),
                ("Low Level Development", "https://www.youtube.com/channel/UCRWXAQsN5S3FPDHY4Ttq1Xg"),
                ("Custom Linux GUI", "https://www.youtube.com/watch?v=fxWRZuKqmk4&list=PLNgoty5-NgL4nL1YzbvwaPzbgJ4WXk9Tv"),
                ("Creating Debian Based Linux Distro", "https://www.youtube.com/watch?v=gibZpx9_dfU"),
            ],
        }


        # Create buttons for each link
        for category, links in resource_links.items():
            category_label = tk.Label(links_frame, text=category, font=("Arial", 16, "bold"), fg='#ff6600', bg='#1a1a1a')
            category_label.pack(pady=(20, 10), anchor='w')

            for text, url in links:
                button = tk.Button(links_frame, text=text, command=lambda u=url: self.open_link(u),
                                font=("Arial", 12), fg='white', bg='#333333',
                                activebackground='#ff6600', activeforeground='white',
                                width=40, height=1, bd=0)
                button.pack(pady=5)
                button.bind("<Enter>", lambda e, b=button: b.configure(bg='#444444'))
                button.bind("<Leave>", lambda e, b=button: b.configure(bg='#333333'))

        # Add back button
        back_button = tk.Button(links_frame, text="Back to Menu", command=self.show_central_menu,
                                font=("Arial", 14), fg='white', bg='#ff6600', padx=20, pady=10)
        back_button.pack(pady=20)

# Add this method to your Timer class


    def show_section(self, section):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.current_section = section


        if section == "links":
            # self.links_frame.pack(fill=tk.BOTH, expand=True)
            self.show_links()
            self.current_section = self.links_frame
        elif section == "timer":
            self.ask_total_problems()
        elif section == "OS_DEV":
            self.show_sample_links()

        # self.setup_section_content(section)
        self.current_section = section


    # def show_links(self):
    #     links_frame = tk.Frame(self.master)
    #     links_frame.pack(fill=tk.BOTH, expand=True)

    #     # Add link buttons
    #     tk.Button(links_frame, text="luv cp", command=lambda: self.open_link("https://www.youtube.com/playlist?list=PLauivoElc3ggagradg8MfOZreCMmXMmJ-")).pack(pady=5)
    #     tk.Button(links_frame, text="algoexpert", command=lambda: self.open_link("https://www.algoexpert.io/")).pack(pady=5)
    #     tk.Button(links_frame, text="sheets", command=lambda: self.open_link("https://sdesheets.bio.link/")).pack(pady=5)
    #     tk.Button(links_frame, text="grind 75", command=lambda: self.open_link("https://www.techinterviewhandbook.org/grind75")).pack(pady=5)


    #     # Add more link buttons as needed
    #     # add text in the gui like a heading
    #     tk.Label(links_frame, text="cs fundamentals ").pack(pady=10)
    #     tk.Button(links_frame, text="os", command=lambda: self.open_link("https://www.youtube.com/watch?v=3obEP8eLsCw")).pack(pady=5)
    #     tk.Button(links_frame, text="dbms", command=lambda: self.open_link("https://www.youtube.com/watch?v=dl00fOOYLOM&pp=ygUJYnViYmVyIGNu")).pack(pady=5)
    #     tk.Button(links_frame, text="OOPs", command=lambda: self.open_link("https://www.youtube.com/watch?v=dhksGkjtKqk&t=2038s")).pack(pady=5)
    #     tk.Button(links_frame, text="CN", command=lambda: self.open_link("https://tinyurl.com/28png6ca")).pack(pady=5)




    #      # Make the text read-only

    #     tk.Label(links_frame, text="Welcome to the Links section!\nClick on a link to open it in your browser.").pack(pady=10)

    #     # Add back button
    #     tk.Button(links_frame, text="Back to Menu", command=self.show_central_menu).pack(pady=10)
    def show_links(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.configure(bg='#1a1a1a')
        
        # Create a main frame
        main_frame = tk.Frame(self.master, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        canvas = tk.Canvas(main_frame, bg='#1a1a1a')


        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        # canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        def update_canvas_size(event):
            canvas.configure(height=event.height)
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.master.bind("<Configure>", update_canvas_size)

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Create another frame inside the canvas
        links_frame = tk.Frame(canvas, bg='#1a1a1a')

        # Add that new frame to a window in the canvas
        canvas.create_window((0, 0), window=links_frame, anchor="nw")
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Add main button for daily link
        daily_button = tk.Button(links_frame, text="Daily Grind", command=lambda: self.open_link("https://www.techinterviewhandbook.org/grind75"),
                                 font=("Arial", 14, "bold"), fg='white', bg='#ff6600', padx=20, pady=10)
        daily_button.pack(pady=20)




        # Links data structure
        # links = {
        #     "DSA Fundamentals": [
        #         ("Luv CP", "https://www.youtube.com/playlist?list=PLauivoElc3ggagradg8MfOZreCMmXMmJ-"),
        #         ("AlgoExpert", "https://www.algoexpert.io/"),
        #         ("SDE Sheets", "https://sdesheets.bio.link/"),
        #         ("Grind 75", "https://www.techinterviewhandbook.org/grind75"),
        #         ("Grokking-the-Coding-Interview-Patterns", "https://github.com/dipjul/Grokking-the-Coding-Interview-Patterns-for-Coding-Questions")
        #     ],
        #     "CS Fundamentals": [
        #         ("Operating Systems", "https://www.youtube.com/watch?v=3obEP8eLsCw"),
        #         ("DBMS", "https://www.youtube.com/watch?v=dl00fOOYLOM&pp=ygUJYnViYmVyIGNu"),
        #         ("OOPs", "https://www.youtube.com/watch?v=dhksGkjtKqk&t=2038s"),
        #         ("Computer Networks", "https://tinyurl.com/28png6ca")
        #     ],
        #     "sites": [
        #         ("Leetcode", "https://leetcode.com/"),
        #         ("GeeksforGeeks", "https://www.geeksforgeeks.org/"),
        #         ("HackerRank", "https://www.hackerrank.com/"),
        #         ("CodeChef", "https://www.codechef.com/"),
        #         ("CodeForces", "https://codeforces.com/"),
        #         ("AtCoder", "https://atcoder.jp/"),
        #         ("TopCoder", "https://www.topcoder.com/"),
        #         ("HackerEarth", "https://www.hackerearth.com/"),
        #         ("Codewars", "https://www.codewars.com/"),
        #         ("Project Euler", "https://projecteuler.net/"),
        #         ("Codeforces Gym", "https://codeforces.com/gyms"),
        #     ]
        # }

        links = {
    "DSA Fundamentals": [
        "Essential resources for Data Structures and Algorithms",
        ("Luv CP", "https://www.youtube.com/playlist?list=PLauivoElc3ggagradg8MfOZreCMmXMmJ-"),("blogs codeforces", "https://codeforces.com/blog/entry/91363"),
        {"Advanced DSA": [
            ("AlgoExpert", "https://www.algoexpert.io/"),
            ("SDE Sheets", "https://sdesheets.bio.link/"),
            {"CSES":[("video William Lincses","https://www.youtube.com/watch?v=dZ_6MS14Mg4"),("Editorials","https://codeforces.com/blog/entry/83343"),("cses", "https://cses.fi/problemset/"),]}
        ]},
        
        {"youtube":[
            "youtube links ",
            ("ThePrimeagen","https://frontendmasters.com/courses/algorithms/arrays-data-structure/"),
            ("CODEnCODE","https://www.youtube.com/@codencode"),
            ("DP","https://www.youtube.com/@TheAdityaVerma"),
        ]

        },
        {"Interview Prep": [
            ("Grind 75", "https://www.techinterviewhandbook.org/grind75"),
            ("Grokking-the-Coding-Interview-Patterns", "https://github.com/dipjul/Grokking-the-Coding-Interview-Patterns-for-Coding-Questions"),
        ]},
    ],
    "CS Fundamentals": [
        "Core computer science topics",
        {"Operating Systems": [
            ("OS Concepts", "https://www.youtube.com/watch?v=3obEP8eLsCw"),
        ]},
        {"Databases": [
            ("DBMS", "https://www.youtube.com/watch?v=dl00fOOYLOM&pp=ygUJYnViYmVyIGNu"),
        ]},
        {"Object-Oriented Programming": [
            ("OOPs", "https://www.youtube.com/watch?v=dhksGkjtKqk&t=2038s"),
        ]},
        {"Networking": [
            ("Computer Networks", "https://tinyurl.com/28png6ca"),
        ]},        {"BACKend": [
            ("Node.js - Top 100 Interview Questions and Answers", "https://www.youtube.com/watch?v=Nz-nPR5YJbw"),
            ("Top 100 React JS Interview Questions and Answers", "https://www.youtube.com/watch?v=yfD_mS7XM0k"),
        ]},
    ],
    "Coding Platforms": [
        "Popular websites for practicing coding problems",
        {"Competitive Programming": [
            ("CodeForces", "https://codeforces.com/"),
            ("CodeChef", "https://www.codechef.com/"),
            ("AtCoder", "https://atcoder.jp/"),
            ("TopCoder", "https://www.topcoder.com/"),
            ("Codeforces Gym", "https://codeforces.com/gyms"),
        ]},
        {"Interview Preparation": [
            ("Leetcode", "https://leetcode.com/"),
            ("HackerRank", "https://www.hackerrank.com/"),
            ("GeeksforGeeks", "https://www.geeksforgeeks.org/"),
        ]},
        {"Other Platforms": [
            ("HackerEarth", "https://www.hackerearth.com/"),
            ("Codewars", "https://www.codewars.com/"),
            ("Project Euler", "https://projecteuler.net/"),
        ]},
    ],
}

        # def toggle_category(category_frame, items_frame):
        #     if items_frame.winfo_viewable():
        #         items_frame.pack_forget()
        #     else:
        #         items_frame.pack(fill=tk.X)

        # for category, items in links.items():
        #     category_frame = tk.Frame(links_frame, bg='#1a1a1a')
        #     category_frame.pack(pady=10, fill=tk.X)

        #     items_frame = tk.Frame(category_frame, bg='#1a1a1a')

        #     category_button = tk.Button(category_frame, text=category, font=("Arial", 16, "bold"), 
        #                                 fg='#ff6600', bg='#1a1a1a', bd=0, anchor='w',
        #                                 command=lambda f=category_frame, i=items_frame: toggle_category(f, i))
        #     category_button.pack(fill=tk.X)

        #     for text, url in items:
        #         button = tk.Button(items_frame, text=text, command=lambda u=url: self.open_link(u),
        #                         font=("Arial", 12), fg='white', bg='#333333',
        #                         activebackground='#ff6600', activeforeground='white',
        #                         width=30, height=1, bd=0)
        #         button.pack(pady=5)
        #         button.bind("<Enter>", lambda e, b=button: b.configure(bg='#444444'))
        #         button.bind("<Leave>", lambda e, b=button: b.configure(bg='#333333'))

        #     items_frame.pack_forget()  # Initially hide the items
        def create_menu_item(parent, item, level=0):
            if isinstance(item, dict):
                for key, value in item.items():
                    frame = tk.Frame(parent, bg='#1a1a1a')
                    frame.pack(fill=tk.X, padx=(level*20, 0))
                    button = tk.Button(frame, text=key, font=("Arial", 14-level, "bold"),
                                    fg='#ff6600', bg='#1a1a1a', bd=0, anchor='w')
                    button.pack(fill=tk.X)
                    sub_frame = tk.Frame(frame, bg='#1a1a1a')
                    create_menu_item(sub_frame, value, level+1)
                    button.config(command=lambda f=sub_frame: toggle_frame(f))
            elif isinstance(item, list):
                for sub_item in item:
                    create_menu_item(parent, sub_item, level)
            elif isinstance(item, tuple):
                text, url = item
                button = tk.Button(parent, text=text, command=lambda u=url: self.open_link(u),
                                font=("Arial", 12-level), fg='white', bg='#333333',
                                activebackground='#ff6600', activeforeground='white',
                                width=30, height=1, bd=0)
                button.pack(pady=5, padx=(level*20, 0), anchor='w')
                button.bind("<Enter>", lambda e, b=button: b.configure(bg='#444444'))
                button.bind("<Leave>", lambda e, b=button: b.configure(bg='#333333'))
            else:
                label = tk.Label(parent, text=str(item), font=("Arial", 12-level), fg='white', bg='#1a1a1a')
                label.pack(pady=5, padx=(level*20, 0), anchor='w')


        def toggle_frame(frame):
            def animate(progress):
                if expanding:
                    height = int(progress * target_height)
                else:
                    height = int((1 - progress) * start_height)

                frame.configure(height=height)

                if progress >= 1:
                    if not expanding:
                        frame.pack_forget()
                else:
                    frame.after(10, lambda: animate(progress + 0.1))

            if frame.winfo_viewable():
                expanding = False
                start_height = frame.winfo_height()
                target_height = 0
            else:
                expanding = True
                frame.pack(fill=tk.X)
                frame.update()
                start_height = 0
                target_height = frame.winfo_reqheight()

            animate(0)

        # from animatecolor import AnimateColor

        # def toggle_frame(frame):
        #     def animate():
        #         if expanding:
        #             frame.configure(height=target_height)
        #             AnimateColor(frame, 'bg', start_color, end_color, duration=300)
        #         else:
        #             AnimateColor(frame, 'bg', start_color, end_color, duration=300, 
        #                         on_complete=lambda: frame.pack_forget())

        #     if frame.winfo_viewable():
        #         expanding = False
        #         start_color = frame['bg']
        #         end_color = '#1a1a1a'
        #     else:
        #         expanding = True
        #         frame.pack(fill=tk.X)
        #         frame.update()
        #         target_height = frame.winfo_reqheight()
        #         start_color = '#1a1a1a'
        #         end_color = frame['bg']

        #     animate()







        # Use the updated create_menu_item function
        create_menu_item(links_frame, links)



        # Add back button
        back_button = tk.Button(links_frame, text="BACK TO MENU", command=self.show_central_menu,
                                font=("Arial", 14, "bold"), fg='white', bg='#ff6600',
                                activebackground='#ff8800', activeforeground='white',
                                width=20, height=2, bd=0)
        back_button.pack(pady=20)
    
    def ask_total_problems(self):
        problem_window = tk.Toplevel(self.master)
        problem_window.title("Enter Total Problems")
        
        label = tk.Label(problem_window, text="Enter total problems:")
        label.pack(pady=10)
        
        entry = tk.Entry(problem_window)
        entry.pack(pady=10)
        
        start_button = tk.Button(problem_window, text="Start", command=lambda: self.start_new_timer_session(problem_window, entry.get()))
        start_button.pack(pady=10)

    def start_new_timer_session(self, problem_window, total_problems):
        problem_window.destroy()
        
        # Clear existing content
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Set up the timer in the main window
        self.master.configure(bg='white')
        self.total_problems = int(total_problems)
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.problems_solved = 0
        
        # Set up UI for the timer
        self.setup_ui()
        self.update_clock()



    def open_link(self, url):
        webbrowser.open(url, new=2)

    def show_message(self, title, message):
        CustomMessageBox(title, message, self.master)

    def show_error(self, title, message):
        dialog = CustomMessageBox(title, message, self.master)
        dialog.configure(bg='#ffebee')  # Light red background for errors

    def on_closing(self):
        if self.current_section == "timer":
            self.save_session()
        self.master.destroy()







    # def restore_session(self):
    #     if os.path.exists('session.json'):
    #         with open('session.json', 'r') as f:
    #             data = json.load(f)
            
    #         self.stopwatch_time = data['stopwatch_time']
    #         self.problems_solved = data['problems_solved']
    #         self.total_problems = data['total_problems']
            
    #         self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
            
    #         for log in data['logs']:
    #             self.steps_listbox.insert('', 'end', values=log)
            
    #         self.update_stopwatch()
    #         print("Previous session restored")
    #     else:
    #         print("No previous session found")




    def restore_session(self):
        session_folder = "sessions"
        if os.path.exists(session_folder):
            sessions = [f for f in os.listdir(session_folder) if f.endswith('.json')]
            if sessions:
                self.open_session_selection_window(sessions)
            else:
                print("No previous sessions found")
        else:
            print("No sessions folder found")

    def open_session_selection_window(self, sessions):
        selection_window = tk.Toplevel(self.master)
        selection_window.title("Select Session to Restore")
        selection_window.geometry("400x400")

        listbox = tk.Listbox(selection_window, width=50)
        listbox.pack(pady=10)

        for session in sessions:
            listbox.insert(tk.END, session)

        restore_button = tk.Button(selection_window, text="Restore Selected Session", 
                                command=lambda: self.restore_selected_session(listbox.get(tk.ACTIVE), selection_window))
        restore_button.pack(pady=5)

    def restore_selected_session(self, selected_session, selection_window):
        if selected_session:
            session_path = os.path.join("sessions", selected_session)
            with open(session_path, 'r') as f:
                data = json.load(f)
            
            self.stopwatch_time = data['stopwatch_time']
            self.problems_solved = data['problems_solved']
            self.total_problems = data['total_problems']
            
            self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
            
            self.steps_listbox.delete(*self.steps_listbox.get_children())
            for log in data['logs']:
                self.steps_listbox.insert('', 'end', values=log)
            
            self.update_stopwatch()
            self.current_session_file = session_path
            print(f"Session restored: {selected_session}")
            selection_window.destroy()
            self.current_session_file = session_path
            self.session_file_label.config(text=f"Current session: {selected_session}")
        else:
            print("No session selected")




    def start_program(self):
        # Get the total problems from the input field
        self.total_problems = int(self.total_problems_entry.get())

        # Hide the input field and start button
        self.total_problems_label.pack_forget()
        self.total_problems_entry.pack_forget()
        self.start_program_button.pack_forget()

        # Create the rest of the UI
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.problems_solved = 0

        # UI Setup
        self.setup_ui()

        # Start updating clock
        self.update_clock()



    def export_to_markdown(self):
        if not self.current_session_file:
            self.show_message("Error", "No active session to export")
            return
            
        try:
            base_filename = "cp_practice_log"
            extension = ".md"
            counter = 0
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            while True:
                if counter == 0:
                    filename = f"{base_filename}_{timestamp}{extension}"
                else:
                    filename = f"{base_filename}_{timestamp}_{counter}{extension}"

                if not os.path.exists(filename):
                    break
                counter += 1

            with open(filename, "w") as f:
                f.write("# CP Practice Log\n\n")
                f.write("| Time | Action |\n")
                f.write("|------|--------|\n")
                for item in self.steps_listbox.get_children():
                    values = self.steps_listbox.item(item)['values']
                    f.write(f"| {values[0]} | {values[1]} |\n")
            print(f"Exported to {filename}")
            self.show_message(
                "Export Complete", 
                f"Session has been exported to:\n{filename}\n\nTotal Problems: {self.total_problems}\nSolved: {self.problems_solved}"
            )
        except Exception as e:
            self.show_error("Export Error", f"Failed to export session:\n{str(e)}")
  
    # def setup_ui(self):
    #     # Stopwatch
    #     self.stopwatch_label = tk.Label(self.master, text="00:00", font=("Arial", 24))
    #     self.stopwatch_label.pack(pady=10)
        
    #     # Clock
    #     self.clock_label = tk.Label(self.master, text="", font=("Arial", 24))
    #     self.clock_label.pack(pady=10)

    #     # Start Button
    #     self.start_button = tk.Button(self.master, text="Start", command=self.start_stopwatch)
    #     self.start_button.pack(pady=5)

    #     # Stop Button
    #     self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED)
    #     self.stop_button.pack(pady=5)

    #     # Problem Solved Button
    #     # self.solve_button = tk.Button(self.master, text="Problem Solved", command=self.increment_problems)
    #     self.solve_button = tk.Button(self.master, text="Problem Solved", command=self.increment_problems, state=tk.DISABLED)

    #     self.solve_button.pack(pady=5)

    #     # Problem Counter
    #     self.problem_label = tk.Label(self.master, text=f"{self.problems_solved}/{self.total_problems}\nproblems count", font=("Arial", 16))
    #     self.problem_label.pack(pady=10)
    #     # self.export_button = tk.Button(self.master, text="Export to Markdown", command=self.export_to_markdown)
    #     # self.export_button.pack(pady=10)
    #     self.export_button = tk.Button(self.master, text="Export to Markdown", command=self.export_to_markdown, state=tk.DISABLED)
    #     self.export_button.pack(pady=10)

    #     # Steps List
    #     self.steps_label = tk.Label(self.master, text="Steps:", font=("Arial", 16))
    #     self.steps_label.pack(pady=5)
        
    #     self.steps_listbox = ttk.Treeview(self.master, columns=('Time', 'Action'), show='headings', height=10)
    #     self.steps_listbox.heading('Time', text='Time')
    #     self.steps_listbox.heading('Action', text='Action')
    #     self.steps_listbox.column('Time', width=150)
    #     self.steps_listbox.column('Action', width=150)
    #     self.steps_listbox.pack(pady=10)






    def setup_ui(self):
        # Stopwatch
        self.back_button = tk.Button(self.master, text="Back to Menu", command=self.back_to_menu)
        self.back_button.pack(pady=10)
        self.stopwatch_label = tk.Label(self.master, text="00:00", font=("Arial", 24))
        self.stopwatch_label.pack(pady=10)
        
        # Clock
        self.clock_label = tk.Label(self.master, text="", font=("Arial", 24))
        self.clock_label.pack(pady=10)

        start_stop_frame = tk.Frame(self.master)
        start_stop_frame.pack(pady=5)

        self.start_button = tk.Button(start_stop_frame, text="Start", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(start_stop_frame, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Problem Solved Button
        problem_frame = tk.Frame(self.master)
        problem_frame.pack(pady=5)

        self.solve_button = tk.Button(problem_frame, text="Problem Solved", command=self.increment_problems, state=tk.DISABLED)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.unsolve_button = tk.Button(problem_frame, text="Mark Unsolved", command=self.decrement_problems, state=tk.DISABLED)
        self.unsolve_button.pack(side=tk.LEFT, padx=5)

        # Problem Counter
        self.problem_label = tk.Label(self.master, text=f"{self.problems_solved}/{self.total_problems}\nproblems count", font=("Arial", 16))
        self.problem_label.pack(pady=10)

        self.export_button = tk.Button(self.master, text="Export to Markdown", command=self.export_to_markdown, state=tk.DISABLED)
        self.export_button.pack(pady=5)

        self.restore_button = tk.Button(self.master, text="Restore Previous Session", command=self.restore_session)
        self.restore_button.pack(pady=5)

        self.session_file_label = tk.Label(self.master, text="", font=("Arial", 10))
        self.session_file_label.pack(side=tk.BOTTOM, pady=5)

        # Steps List


        self.steps_label = tk.Label(self.master, text="Steps:", font=("Arial", 16))
        self.steps_label.pack(pady=5)
        
        self.steps_listbox = ttk.Treeview(self.master, columns=('Time', 'Action'), show='headings', height=10)
        self.steps_listbox.heading('Time', text='Time')
        self.steps_listbox.heading('Action', text='Action')
        self.steps_listbox.column('Time', width=150)
        self.steps_listbox.column('Action', width=150)
        self.steps_listbox.pack(pady=10)

        
    def decrement_problems(self):
        if self.problems_solved > 0:
            self.problems_solved -= 1
            self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
            self.add_step(f"Problem unmarked (total solved: {self.problems_solved})", 'orange')
            color = self.get_gradient_color()
            self.master.configure(bg=color)

    def show_central_menu(self):
        if self.master:
            for widget in self.master.winfo_children():
                widget.destroy()

        self.master.configure(bg='#1a1a1a')  # Dark background

        self.central_frame = tk.Frame(self.master, bg='#1a1a1a')
        self.central_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        button_font = tkfont.Font(family="Arial", size=16, weight="bold")

        title = tk.Label(self.central_frame, text="CP PRACTICE", font=title_font, fg='#ff6600', bg='#1a1a1a')
        title.pack(pady=20)

        buttons = [
            ("LINKS", lambda: self.show_section("links")),
            ("TIMER", lambda: self.show_section("timer")),
            ("OS_DEV", lambda: self.show_section("OS_DEV")),
        ]

        for text, command in buttons:
            button = tk.Button(self.central_frame, text=text, command=command, 
                            font=button_font, fg='white', bg='#333333', 
                            activebackground='#ff6600', activeforeground='white',
                            width=20, height=2, bd=0)
            button.pack(pady=10)
            button.bind("<Enter>", lambda e, b=button: b.configure(bg='#444444'))
            button.bind("<Leave>", lambda e, b=button: b.configure(bg='#333333'))

    def save_session(self):
        if hasattr(self, 'stopwatch_running') and self.stopwatch_running:
            session_folder = "sessions"
            if not os.path.exists(session_folder):
                os.makedirs(session_folder)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(session_folder, f"session_{timestamp}.json")

            data = {
                'stopwatch_time': getattr(self, 'stopwatch_time', 0),
                'problems_solved': getattr(self, 'problems_solved', 0),
                'total_problems': getattr(self, 'total_problems', 0),
                'logs': [self.steps_listbox.item(item)['values'] for item in self.steps_listbox.get_children()] if hasattr(self, 'steps_listbox') else []
            }

            with open(filename, 'w') as f:
                json.dump(data, f)

            print(f"Session saved successfully: {filename}")

    def save_session(self):
        if self.current_session_file:
            filename = self.current_session_file
        else:
            session_folder = "sessions"
            if not os.path.exists(session_folder):
                os.makedirs(session_folder)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(session_folder, f"session_{timestamp}.json")
            self.current_session_file = filename

        data = {
            'stopwatch_time': getattr(self, 'stopwatch_time', 0),
            'problems_solved': getattr(self, 'problems_solved', 0),
            'total_problems': getattr(self, 'total_problems', 0),
            'logs': [self.steps_listbox.item(item)['values'] for item in self.steps_listbox.get_children()] if hasattr(self, 'steps_listbox') else []
        }

        with open(filename, 'w') as f:
            json.dump(data, f)

        print(f"Session saved successfully: {filename}")
        self.session_file_label.config(text=f"Current session: {os.path.basename(filename)}")












    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.solve_button.config(state=tk.NORMAL)
            self.update_stopwatch()
            self.add_step("Started", 'green')
            self.master.configure(bg='light green')
 
            self.unsolve_button.config(state=tk.NORMAL)
            self.save_session()



    # def stop_stopwatch(self):
    #     if self.stopwatch_running:
    #         self.stopwatch_running = False
    #         self.start_button.config(state=tk.NORMAL)
    #         self.stop_button.config(state=tk.DISABLED)
    #         self.solve_button.config(state=tk.DISABLED)
    #         self.master.configure(bg='red')
    #         self.unsolve_button.config(state=tk.DISABLED)




    #         self.add_step("Stopped", 'red')
    #         self.save_session()



    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.solve_button.config(state=tk.DISABLED)
            self.unsolve_button.config(state=tk.DISABLED)
            self.master.configure(bg='red')
            self.add_step("Stopped", 'red')
            self.save_session() # Save session when stopping the timer





    def get_gradient_color(self):
        r = int(255 * (self.problems_solved / self.total_problems))
        g = int(255 * (1 - self.problems_solved / self.total_problems))
        b = int(150 * (self.problems_solved / self.total_problems))
        return f'#{r:02x}{g:02x}{b:02x}'


    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_time += 1
            days, remainder = divmod(self.stopwatch_time, 86400)  # 86400 seconds in a day
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if days > 0:
                time_str = f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
            elif hours > 0:
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:{seconds:02d}"
            
            self.stopwatch_label.config(text=time_str)
            self.master.after(1000, self.update_stopwatch)


    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M")
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_clock)


    def increment_problems(self):
        self.problems_solved += 1
        self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
        self.add_step(f"Problem {self.problems_solved} solved", 'black')
        color = self.get_gradient_color()
        self.master.configure(bg=color)
        if self.problems_solved == self.total_problems:
            self.add_step("All problems solved! Well done!", 'pink')


    def format_time_difference(self, seconds):
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}min"
            return f"{minutes}min {remaining_seconds}s"
        else:
            hours = seconds // 3600
            remaining = seconds % 3600
            minutes = remaining // 60
            seconds = remaining % 60
            if minutes == 0 and seconds == 0:
                return f"{hours}h"
            elif seconds == 0:
                return f"{hours}h {minutes}min"
            return f"{hours}h {minutes}min {seconds}s"

    def convert_time_to_seconds(self, time_str):
        # Handle different time formats (00:00, 00:00:00, 1d 00:00:00)
        parts = time_str.split()
        if len(parts) > 1:  # Format: "1d 00:00:00"
            days = int(parts[0].replace('d', ''))
            time_parts = parts[1].split(':')
        else:
            days = 0
            time_parts = parts[0].split(':')
        
        if len(time_parts) == 2:  # Format: "00:00"
            minutes, seconds = map(int, time_parts)
            hours = 0
        else:  # Format: "00:00:00"
            hours, minutes, seconds = map(int, time_parts)
        
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return total_seconds

    def add_step(self, action, color):
        current_time = datetime.now().strftime("%H:%M:%S")
        stopwatch_time = self.stopwatch_label.cget("text")
        
        # Get all existing items
        existing_items = self.steps_listbox.get_children()
        
        # Calculate time spent on problem
        time_spent_str = ""
        if "Problem" in action and "solved" in action and existing_items:
            last_item = self.steps_listbox.item(existing_items[-1])
            last_values = last_item['values']
            
            # Only calculate if the last action was also a solved problem
            if "Problem" in last_values[1] and "solved" in last_values[1]:
                last_stopwatch_time = last_values[0].split(' ; ')[0]
                current_seconds = self.convert_time_to_seconds(stopwatch_time)
                last_seconds = self.convert_time_to_seconds(last_stopwatch_time)
                diff_seconds = current_seconds - last_seconds
                
                if diff_seconds > 0:
                    time_spent_str = f" (Time spent: {self.format_time_difference(diff_seconds)})"

        step = f"{stopwatch_time} ; {current_time}"
        self.steps_listbox.insert('', 'end', values=(step, f"{action}{time_spent_str}"), tags=(color,))
        self.steps_listbox.tag_configure('green', foreground='green')
        self.steps_listbox.tag_configure('red', foreground='red')
        self.steps_listbox.tag_configure('black', foreground='black')
        self.export_button.config(state=tk.NORMAL) 
        self.steps_listbox.tag_configure('orange', foreground='orange')
    def back_to_menu(self):
        self.stopwatch_running = False
        for widget in self.master.winfo_children():
            widget.destroy()
        self.show_central_menu()

if __name__ == "__main__":
    root = tk.Tk()
        # root = tk.Tk()


    icon_path = resource_path('icon.ico')
    img = Image.open(icon_path)
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(True, icon)
    root.iconbitmap(icon_path)
    app = CPPracticeApp(root)
    root.mainloop()
