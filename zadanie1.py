import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

tryb = None
pole_param = None
canvas = None
punkty = []
zaznaczony = None
uchwyty = []
uchwyt_drag = None

def odznacz():
    global zaznaczony, uchwyty
    for h in uchwyty:
        canvas.delete(h)
    uchwyty.clear()
    zaznaczony = None

def klik(e):
    global punkty, zaznaczony, uchwyty, uchwyt_drag
    t = tryb.get()
    if t in ["linia", "prostokat", "okrag"]:
        punkty.append((e.x, e.y))
        if t == "linia" and len(punkty) == 2:
            x1, y1 = punkty[0]
            x2, y2 = punkty[1]
            zaznaczony = canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
            punkty.clear()
        elif t == "prostokat" and len(punkty) == 2:
            x1, y1 = punkty[0]
            x2, y2 = punkty[1]
            zaznaczony = canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=2)
            punkty.clear()
        elif t == "okrag" and len(punkty) == 2:
            cx, cy = punkty[0]
            x2, y2 = punkty[1]
            r = abs(x2 - cx)
            zaznaczony = canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="red", width=2)
            punkty.clear()
    elif t == "edycja":
        nearby = canvas.find_overlapping(e.x - 2, e.y - 2, e.x + 2, e.y + 2)
        if not nearby:
            odznacz()
            return

        clicked = None
        for item in nearby:
            if "uchwyt" in canvas.gettags(item):
                clicked = item
                break
        if clicked:
            uchwyt_drag = clicked
            return

        closest = canvas.find_closest(e.x, e.y)
        if closest:
            zaznaczony = closest[0]
            stworz_uchwyty()


def stworz_uchwyty():
    global uchwyty
    for h in uchwyty:
        canvas.delete(h)
    uchwyty.clear()
    if not zaznaczony:
        return
    typ = canvas.type(zaznaczony)
    coords = canvas.coords(zaznaczony)
    if typ == "line":
        punkty_loc = [(coords[0], coords[1]), (coords[2], coords[3])]
    elif typ == "rectangle":
        x1, y1, x2, y2 = coords
        punkty_loc = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
    elif typ == "oval":
        x1, y1, x2, y2 = coords
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        punkty_loc = [(cx, cy), (x2, cy)]
    else:
        return

    for (x, y) in punkty_loc:
        h = canvas.create_rectangle(x - 4, y - 4, x + 4, y + 4, fill="red", tags="uchwyt")
        uchwyty.append(h)

def przeciaganie(e):
    global uchwyt_drag
    if uchwyt_drag:
        canvas.coords(uchwyt_drag, e.x - 4, e.y - 4, e.x + 4, e.y + 4)
        aktualizuj_ksztalt()
    elif zaznaczony and tryb.get() == "edycja":
        bbox = canvas.bbox(zaznaczony)
        if bbox:
            dx = e.x - (bbox[0] + bbox[2]) // 2
            dy = e.y - (bbox[1] + bbox[3]) // 2
            canvas.move(zaznaczony, dx, dy)
            for h in uchwyty:
                canvas.move(h, dx, dy)


def stop_drag(e):
    global uchwyt_drag
    uchwyt_drag = None


def aktualizuj_ksztalt():
    if not zaznaczony:
        return
    typ = canvas.type(zaznaczony)
    try:
        if typ == "line":
            p = []
            for h in uchwyty:
                x1, y1, x2, y2 = canvas.coords(h)
                p.append(((x1 + x2) / 2, (y1 + y2) / 2))
            canvas.coords(zaznaczony, p[0][0], p[0][1], p[1][0], p[1][1])
        elif typ == "rectangle":
            xs, ys = [], []
            for h in uchwyty:
                x1, y1, x2, y2 = canvas.coords(h)
                xs.append((x1 + x2) / 2)
                ys.append((y1 + y2) / 2)
            canvas.coords(zaznaczony, min(xs), min(ys), max(xs), max(ys))
        elif typ == "oval":
            x1, y1, x2, y2 = canvas.coords(uchwyty[0])
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            x1, y1, x2, y2 = canvas.coords(uchwyty[1])
            rx = abs((x1 + x2) / 2 - cx)
            r = max(rx, 1)
            canvas.coords(zaznaczony, cx - r, cy - r, cx + r, cy + r)
    except Exception:
        pass

def zastosuj_parametry():
    global zaznaczony
    dane = pole_param.get().strip()
    if not dane:
        messagebox.showerror("Blad", "brak parametrow.")
        return
    dane_split = dane.split(",")
    try:
        liczby = list(map(float, [s.strip() for s in dane_split]))
    except Exception:
        messagebox.showerror("Blad", "podaj liczby poprawnie")
        return

    wybrany_tryb = tryb.get()

    if not zaznaczony:
        if wybrany_tryb == "linia" and len(liczby) == 4:
            canvas.create_line(*liczby, fill="blue", width=2)
            odznacz()
        elif wybrany_tryb == "prostokat" and len(liczby) == 4:
            canvas.create_rectangle(*liczby, outline="green", width=2)
            odznacz()
        elif wybrany_tryb == "okrag" and len(liczby) == 3:
            cx, cy, r = liczby
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="red", width=2)
            odznacz()
        return

    typ = canvas.type(zaznaczony)
    if typ == "line" and len(liczby) == 4:
        canvas.coords(zaznaczony, *liczby)
    elif typ == "rectangle" and len(liczby) == 4:
        canvas.coords(zaznaczony, *liczby)
    elif typ == "oval" and len(liczby) == 3:
        cx, cy, r = liczby
        canvas.coords(zaznaczony, cx - r, cy - r, cx + r, cy + r)
    stworz_uchwyty()


def zapisz():
    plik = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
    if not plik:
        return
    dane = []
    for obj in canvas.find_all():
        if obj in uchwyty:
            continue
        coords = canvas.coords(obj)
        typ = canvas.type(obj)
        dane.append({"typ": typ, "coords": coords})
    with open(plik, "w") as f:
        json.dump(dane, f, indent=2)


def wczytaj():
    plik = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if not plik:
        return
    with open(plik) as f:
        dane = json.load(f)
    canvas.delete("all")
    odznacz()
    for obj in dane:
        if obj["typ"] == "line":
            canvas.create_line(*obj["coords"], fill="blue", width=2)
        elif obj["typ"] == "rectangle":
            canvas.create_rectangle(*obj["coords"], outline="green", width=2)
        elif obj["typ"] == "oval":
            canvas.create_oval(*obj["coords"], outline="red", width=2)


def klawisz(event):
    if event.keysym == "Escape":
        odznacz()

root = tk.Tk()
root.title("Zadanie1 PawełBrzozowski")

panel = tk.Frame(root)
panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

tryb = tk.StringVar(value="linia")

ttk.Label(panel, text="tryb rysowania:").pack()
ttk.Combobox(panel, textvariable=tryb, values=["edycja", "linia", "prostokat", "okrag"]).pack(pady=2)

ttk.Label(panel, text="parametry (x1,y1,x2,y2 / cx,cy,r):").pack()
pole_param = tk.Entry(panel)
pole_param.pack(pady=2)

tk.Button(panel, text="zastosuj parametry", command=zastosuj_parametry).pack(pady=5)
tk.Button(panel, text="zapisz", command=zapisz).pack(pady=5)
tk.Button(panel, text="wczytaj", command=wczytaj).pack(pady=5)

canvas = tk.Canvas(root, bg="white", width=800, height=600)
canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", klik)
canvas.bind("<B1-Motion>", przeciaganie)
canvas.bind("<ButtonRelease-1>", stop_drag)
root.bind_all("<Key>", klawisz)

root.mainloop()
