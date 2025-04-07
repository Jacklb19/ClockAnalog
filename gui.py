import tkinter as tk
import math
import datetime
import pygame
import pytz
from clock_logic import ClockCircularList

pygame.mixer.init()
clock_sound = pygame.mixer.Sound("tic.mp3")

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

    digital_clock_label = tk.Label(root, text="", font=("Consolas", 10),
                                   bg=bg_dark if dark_mode else bg_light,
                                   fg=fg_dark if dark_mode else fg_light)
    digital_clock_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def toggle_mode():
        nonlocal dark_mode
        dark_mode = not dark_mode
        root.configure(bg=bg_dark if dark_mode else bg_light)
        canvas.configure(bg=bg_dark if dark_mode else bg_light)
        label_tz.configure(bg=bg_dark if dark_mode else bg_light, fg=fg_dark if dark_mode else fg_light)
        tz_menu.configure(bg="gray20" if dark_mode else "lightgray", fg="white" if dark_mode else "black")
        digital_clock_label.configure(bg=bg_dark if dark_mode else bg_light,
                                      fg=fg_dark if dark_mode else fg_light)
        draw_clock_face()

    btn_mode = tk.Button(root, text="☀ / 🌙", command=toggle_mode)
    btn_mode.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    clock_segments = ClockCircularList()
    for i in range(1, 13):
        clock_segments.insert_segment_at_end(i)

    hour_hand = canvas.create_line(0, 0, 0, 0, width=5, fill="#666", capstyle=tk.ROUND)
    minute_hand = canvas.create_line(0, 0, 0, 0, width=3, fill="#888", capstyle=tk.ROUND)
    second_hand = canvas.create_line(0, 0, 0, 0, width=1, fill="red", capstyle=tk.ROUND)
    center_dot = canvas.create_oval(0, 0, 0, 0, fill="red", outline="red", tags="center")

    last_second = -1
    updating = False  # Variable de control para evitar duplicados

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

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = cx + math.cos(angle) * (radius - 30)
            y = cy + math.sin(angle) * (radius - 30)
            color = fg_dark if dark_mode else fg_light
            canvas.create_text(x, y, text=str(i), font=("Helvetica", 12, "bold"), fill=color, tags="face")

        canvas.coords(center_dot, cx - 4, cy - 4, cx + 4, cy + 4)

    def update_clock():
        nonlocal last_second, updating

        if updating:  # Si ya se está ejecutando, no hacer nada
            return
        updating = True  # Marcar que la función está en ejecución

        try:
            tz = pytz.timezone(selected_timezone.get())
            now = datetime.datetime.now(tz)
        except Exception as e:
            now = datetime.datetime.utcnow()

        hour = now.hour % 12 + now.minute / 60
        minute = now.minute + now.second / 60
        second = now.second 

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 20

        angle_hour = math.radians(hour * 30 - 90)
        angle_minute = math.radians(minute * 6 - 90)
        angle_second = math.radians(second * 6 - 90)

        x_hour = cx + math.cos(angle_hour) * radius * 0.5
        y_hour = cy + math.sin(angle_hour) * radius * 0.5
        x_minute = cx + math.cos(angle_minute) * radius * 0.72
        y_minute = cy + math.sin(angle_minute) * radius * 0.72
        x_second = cx + math.cos(angle_second) * radius * 0.88
        y_second = cy + math.sin(angle_second) * radius * 0.88

        canvas.coords(hour_hand, cx, cy, x_hour, y_hour)
        canvas.coords(minute_hand, cx, cy, x_minute, y_minute)
        canvas.coords(second_hand, cx, cy, x_second, y_second)

        if int(second) != last_second:
            clock_sound.play()
            last_second = int(second)

        digital_clock_label.config(text=now.strftime("%H:%M:%S"))

        updating = False  # Liberar la variable de control
        root.after(1000, update_clock)

    canvas.bind("<Configure>", lambda e: [draw_clock_face(), update_clock()])
    draw_clock_face()
    update_clock()
    root.mainloop()
