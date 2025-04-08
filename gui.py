import tkinter as tk
import math
import datetime
import pygame
import pytz
from clock_logic import ClockCircularList

pygame.mixer.init()
clock_sound = pygame.mixer.Sound("tic.mp3")

def to_roman(num):
    roman_symbols = [
        ('XII', 12), ('XI', 11), ('X', 10), ('IX', 9),
        ('VIII', 8), ('VII', 7), ('VI', 6), ('V', 5),
        ('IV', 4), ('III', 3), ('II', 2), ('I', 1)
    ]
    for symbol, value in roman_symbols:
        if num == value:
            return symbol
    return str(num)

def run_clock():
    root = tk.Tk()
    root.title("Minimal Analog Clock")
    root.geometry("420x480")
    root.minsize(300, 400)

    dark_mode = True
    bg_dark, fg_dark = "black", "white"
    bg_light, fg_light = "white", "black"

    canvas = tk.Canvas(root, highlightthickness=0, bg=bg_dark if dark_mode else bg_light)
    canvas.pack(fill="both", expand=True)

    timezones = ["UTC", "America/Bogota", "America/New_York", "Europe/London", "Europe/Madrid",
                 "Asia/Tokyo", "Asia/Kolkata", "Australia/Sydney"]
    selected_timezone = tk.StringVar(value="UTC")

    label_tz = tk.Label(root, text="Zona horaria:", font=("Helvetica", 10),
                        bg=bg_dark, fg=fg_dark)
    label_tz.place(x=10, y=10)

    tz_menu = tk.OptionMenu(root, selected_timezone, *timezones)
    tz_menu.config(bg="gray20", fg="white", highlightbackground="black", activebackground="gray")
    tz_menu.place(x=100, y=5)

    bottom_frame = tk.Frame(root, bg=bg_dark if dark_mode else bg_light, height=40)
    bottom_frame.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)
    
    digital_clock_label = tk.Label(bottom_frame, text="", font=("Consolas", 10),
                                   bg=bg_dark if dark_mode else bg_light,
                                   fg=fg_dark if dark_mode else fg_light)
    digital_clock_label.pack(side="right", padx=10, pady=5)
    
    date_label = tk.Label(bottom_frame, text="", font=("Helvetica", 10),
                          bg=bg_dark if dark_mode else bg_light,
                          fg=fg_dark if dark_mode else fg_light)
    date_label.pack(side="left", padx=10, pady=5)

    show_numbers = tk.BooleanVar(value=True)
    modern_style = tk.BooleanVar(value=False)
    use_roman = tk.BooleanVar(value=False)

    chk_numbers = tk.Checkbutton(root, text="Mostrar Números", variable=show_numbers,
                                 bg=bg_dark, fg=fg_dark,
                                 selectcolor=bg_dark if dark_mode else bg_light,
                                 command=lambda: draw_clock_face())
    chk_numbers.place(x=10, y=35)

    chk_style = tk.Checkbutton(root, text="Manecillas modernas", variable=modern_style,
                               bg=bg_dark, fg=fg_dark,
                               selectcolor=bg_dark if dark_mode else bg_light)
    chk_style.place(x=10, y=60)

    chk_roman = tk.Checkbutton(root, text="Números Romanos", variable=use_roman,
                               bg=bg_dark, fg=fg_dark,
                               selectcolor=bg_dark if dark_mode else bg_light,
                               command=lambda: draw_clock_face())
    chk_roman.place(x=10, y=85)

    def toggle_mode():
        nonlocal dark_mode
        dark_mode = not dark_mode
        root.configure(bg=bg_dark if dark_mode else bg_light)
        canvas.configure(bg=bg_dark if dark_mode else bg_light)
        label_tz.configure(bg=bg_dark if dark_mode else bg_light, fg=fg_dark if dark_mode else fg_light)
        tz_menu.configure(bg="gray20" if dark_mode else "lightgray", fg="white" if dark_mode else "black")

        bottom_frame.configure(bg=bg_dark if dark_mode else bg_light)
        digital_clock_label.configure(bg=bg_dark if dark_mode else bg_light,
                                      fg=fg_dark if dark_mode else fg_light)
        date_label.configure(bg=bg_dark if dark_mode else bg_light,
                             fg=fg_dark if dark_mode else fg_light)
        chk_numbers.configure(bg=bg_dark if dark_mode else bg_light,
                              fg=fg_dark if dark_mode else fg_light,
                              selectcolor=bg_dark if dark_mode else bg_light)
        chk_style.configure(bg=bg_dark if dark_mode else bg_light,
                            fg=fg_dark if dark_mode else fg_light,
                            selectcolor=bg_dark if dark_mode else bg_light)
        chk_roman.configure(bg=bg_dark if dark_mode else bg_light,
                            fg=fg_dark if dark_mode else fg_light,
                            selectcolor=bg_dark if dark_mode else bg_light)
        draw_clock_face()

    btn_mode = tk.Button(root, text="☀ / 🌙", command=toggle_mode)
    btn_mode.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    clock_segments = ClockCircularList()
    for i in range(1, 13):
        clock_segments.insert_segment_at_end(i)

    hour_hand = canvas.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
    minute_hand = canvas.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
    second_hand = canvas.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
    center_dot = canvas.create_oval(0, 0, 0, 0,  tags="center")

    last_second = [-1]
    updating = [False]

    def draw_clock_face():
        canvas.delete("face")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 20

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            x = cx + math.cos(angle) * (radius - 12)
            y = cy + math.sin(angle) * (radius - 12)
            r = 2 if i % 5 != 0 else 4
            color = "#333" if dark_mode else "#aaa" if i % 5 != 0 else "#555"
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color, tags="face")

        if show_numbers.get():
            for i in range(1, 13):
                angle = math.radians(i * 30 - 90)
                x = cx + math.cos(angle) * (radius - 30)
                y = cy + math.sin(angle) * (radius - 30)
                color = fg_dark if dark_mode else fg_light
                number = to_roman(i) if use_roman.get() else str(i)
                canvas.create_text(x, y, text=number, font=("Helvetica", 12, "bold"), 
                                   fill=color, tags="face")

        canvas.coords(center_dot, cx - 4, cy - 4, cx + 4, cy + 4)

    def update_clock():
        if updating[0]:
            return
        updating[0] = True

        try:
            tz = pytz.timezone(selected_timezone.get())
            now = datetime.datetime.now(tz)
        except Exception:
            now = datetime.datetime.utcnow()

        hour = now.hour % 12 + now.minute / 60
        minute = now.minute + now.second / 60
        second = now.second

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 20

        if modern_style.get():
            hour_len = 0.4
            min_len = 0.65
            sec_len = 0.75
            canvas.itemconfig(hour_hand, width=5, fill="#666")
            canvas.itemconfig(minute_hand, width=3, fill="#888")
            canvas.itemconfig(second_hand, width=1, fill="red")
            canvas.itemconfig(center_dot, fill="red", outline="red")
        else:
            hour_len = 0.5
            min_len = 0.72
            sec_len = 0.75
            canvas.itemconfig(hour_hand, width=5, fill="#666")
            canvas.itemconfig(minute_hand, width=3, fill="#888")
            canvas.itemconfig(second_hand, width=1, fill="#777")
            canvas.itemconfig(center_dot, fill="white", outline="black")

        angle_hour = math.radians(hour * 30 - 90)
        angle_minute = math.radians(minute * 6 - 90)
        angle_second = math.radians(second * 6 - 90)

        canvas.coords(hour_hand, cx, cy,
                      cx + math.cos(angle_hour) * radius * hour_len,
                      cy + math.sin(angle_hour) * radius * hour_len)
        canvas.coords(minute_hand, cx, cy,
                      cx + math.cos(angle_minute) * radius * min_len,
                      cy + math.sin(angle_minute) * radius * min_len)
        canvas.coords(second_hand, cx, cy,
                      cx + math.cos(angle_second) * radius * sec_len,
                      cy + math.sin(angle_second) * radius * sec_len)

        if int(second) != last_second[0]:
            clock_sound.play()
            last_second[0] = int(second)

        digital_clock_label.config(text=now.strftime("%H:%M:%S"))
        date_label.config(text=now.strftime("%d %B %Y"))

        updating[0] = False
        root.after(1000, update_clock)

    canvas.bind("<Configure>", lambda e: [draw_clock_face(), update_clock()])
    draw_clock_face()
    update_clock()
    root.mainloop()

if __name__ == "__main__":
    run_clock()
