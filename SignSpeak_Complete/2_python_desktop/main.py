import cv2, time, os, sys, tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageDraw
from engine import Engine, SIGNS
import voice

BG, PANEL, AMB, TEAL, TX = "#0a1030", "#131b45", "#68ebff", "#c55fff", "#f1ecff"
TA = ("Nirmala UI", 17)
ctk.set_appearance_mode("dark")

def logo(n=80):
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = n / 100
    d.rounded_rectangle([0, 0, n, n], int(26 * k), fill=AMB)
    d.rounded_rectangle([30 * k, 48 * k, 70 * k, 84 * k], int(10 * k), fill=BG)
    for x, h in ((30, 26), (42, 34), (54, 30)):
        d.rounded_rectangle([x * k, (50 - h) * k, (x + 10) * k, 56 * k], int(5 * k), fill=BG)
    d.rounded_rectangle([17 * k, 52 * k, 31 * k, 72 * k], int(7 * k), fill=BG)
    return im

class App(ctk.CTk):
    def __init__(s):
        super().__init__()
        s.title("SignSpeak"); s.geometry("1220x740"); s.configure(fg_color=BG)
        s.eng = Engine(); s.lang = "en"; s.rec = None
        s.cand = s.last = None; s.since = s.lastt = 0; s.img = None
        s.build(); s.show("Live"); s.refresh_lib()
        s.cap = cv2.VideoCapture(0); s.loop()
        s.protocol("WM_DELETE_WINDOW", s.close)

    # ---------------- UI ----------------
    def build(s):
        side = ctk.CTkFrame(s, width=210, fg_color=PANEL, corner_radius=0); side.pack(side="left", fill="y")
        BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        s.lg = ctk.CTkImage(Image.open(os.path.join(BASE, "assets", "logo.png")), size=(80, 80))
        try: s.iconbitmap(os.path.join(BASE, "icon.ico"))
        except Exception: pass
        ctk.CTkLabel(side, image=s.lg, text="").pack(pady=(26, 4))
        ctk.CTkLabel(side, text="SignSpeak", font=("Segoe UI", 24, "bold"), text_color=AMB).pack()
        ctk.CTkLabel(side, text="சைகை  •  Sign", font=("Nirmala UI", 13), text_color=TEAL).pack(pady=(0, 22))
        for n in ("Live", "Teach", "Library"):
            ctk.CTkButton(side, text="  " + n, anchor="w", height=38, fg_color="transparent", hover_color="#1d2655",
                          text_color=TX, command=lambda n=n: s.show(n)).pack(fill="x", padx=14, pady=3)
        s.seg = ctk.CTkSegmentedButton(side, values=["English", "தமிழ்"], command=s.setlang,
                                       selected_color=TEAL, selected_hover_color=TEAL, font=("Nirmala UI", 13))
        s.seg.set("English"); s.seg.pack(padx=14, pady=(26, 10), fill="x")
        s.face = ctk.CTkSwitch(side, text="Face expressions", progress_color=TEAL); s.face.select(); s.face.pack(pady=6, padx=14, anchor="w")
        s.auto = ctk.CTkSwitch(side, text="Auto speak", progress_color=TEAL); s.auto.select(); s.auto.pack(pady=6, padx=14, anchor="w")

        main = ctk.CTkFrame(s, fg_color="transparent"); main.pack(side="left", fill="both", expand=True, padx=14, pady=14)
        camf = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=22); camf.pack(side="left", anchor="n")
        s.cam = ctk.CTkLabel(camf, text="", width=640, height=480); s.cam.pack(padx=10, pady=10)
        s.now = ctk.CTkLabel(camf, text="", font=("Nirmala UI", 26, "bold"), text_color=AMB); s.now.pack()
        s.bar = ctk.CTkProgressBar(camf, progress_color=AMB, height=8); s.bar.set(0); s.bar.pack(fill="x", padx=20, pady=(4, 16))

        s.box = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=22, width=430); s.box.pack(side="left", fill="both", expand=True, padx=(14, 0))
        s.pg = {n: ctk.CTkFrame(s.box, fg_color="transparent") for n in ("Live", "Teach", "Library")}
        # Live
        p = s.pg["Live"]
        ctk.CTkLabel(p, text="Notepad", font=("Segoe UI", 18, "bold"), text_color=TEAL).pack(anchor="w", padx=14, pady=(14, 4))
        s.note = ctk.CTkTextbox(p, font=TA, fg_color=BG, wrap="word"); s.note.pack(fill="both", expand=True, padx=14)
        r = ctk.CTkFrame(p, fg_color="transparent"); r.pack(fill="x", padx=10, pady=10)
        for t, c in (("Speak", s.say_note), ("Mic", s.mic), ("Undo", s.undo), ("Clear", lambda: s.note.delete("1.0", "end")), ("Save", s.save_note)):
            ctk.CTkButton(r, text=t, width=62, fg_color=AMB if t == "Speak" else "#232c63", text_color="#000" if t == "Speak" else TX, command=c).pack(side="left", padx=3)
        s.mst = ctk.CTkLabel(p, text="Hold a sign 1 second to type it.", text_color="#8f9bd6"); s.mst.pack(pady=(0, 10))
        # Teach
        p = s.pg["Teach"]
        ctk.CTkLabel(p, text="Teach a new sign", font=("Segoe UI", 18, "bold"), text_color=TEAL).pack(anchor="w", padx=14, pady=14)
        s.kind = ctk.CTkOptionMenu(p, values=["Hand sign", "Face expression"], fg_color="#232c63", button_color=AMB, button_hover_color=AMB); s.kind.pack(fill="x", padx=14, pady=4)
        s.en = ctk.CTkEntry(p, placeholder_text="English word", height=38); s.en.pack(fill="x", padx=14, pady=4)
        s.ta = ctk.CTkEntry(p, placeholder_text="தமிழ் சொல்", height=38, font=TA); s.ta.pack(fill="x", padx=14, pady=4)
        ctk.CTkButton(p, text="Record  (3s countdown + 2.5s)", height=42, fg_color=AMB, text_color="#000", command=s.start_rec).pack(fill="x", padx=14, pady=10)
        s.tst = ctk.CTkLabel(p, text="Record same word again from another angle to improve accuracy.", wraplength=380, text_color="#8f9bd6"); s.tst.pack(padx=14)
        # Library
        p = s.pg["Library"]
        ctk.CTkLabel(p, text="Sensitivity", text_color=TX).pack(anchor="w", padx=14, pady=(14, 0))
        sl = ctk.CTkSlider(p, from_=.6, to=2.4, progress_color=AMB, button_color=AMB, command=lambda v: setattr(s.eng, "sens", v)); sl.set(1.2); sl.pack(fill="x", padx=14)
        r = ctk.CTkFrame(p, fg_color="transparent"); r.pack(fill="x", padx=10, pady=6)
        ctk.CTkButton(r, text="Export", width=80, fg_color="#232c63", command=s.export).pack(side="left", padx=4)
        ctk.CTkButton(r, text="Import", width=80, fg_color="#232c63", command=s.imp).pack(side="left", padx=4)
        s.lib = ctk.CTkScrollableFrame(p, fg_color=BG); s.lib.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def show(s, n):
        for f in s.pg.values(): f.pack_forget()
        s.pg[n].pack(fill="both", expand=True)
    def setlang(s, v): s.lang = "ta" if v == "தமிழ்" else "en"; s.refresh_lib()
    def refresh_lib(s):
        for w in s.lib.winfo_children(): w.destroy()
        def row(en, ta, tag, c=None):
            f = ctk.CTkFrame(s.lib, fg_color=PANEL); f.pack(fill="x", pady=3)
            ctk.CTkLabel(f, text=f"{en}  /  {ta}", font=TA, anchor="w").pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(f, text=tag, text_color=TEAL).pack(side="right", padx=8)
            if c: ctk.CTkButton(f, text="✕", width=28, fg_color="#c1121f", command=lambda: (s.eng.delete(c), s.refresh_lib())).pack(side="right")
        for en, ta in SIGNS.values(): row(en, ta, "built-in")
        for c in s.eng.custom: row(c["en"], c["ta"], "my " + c["kind"], c)

    # ---------------- notepad / voice ----------------
    def add(s, t): s.note.insert("end", t + " ")
    def say_note(s): voice.speak(s.note.get("1.0", "end").strip(), s.lang)
    def undo(s):
        w = s.note.get("1.0", "end").strip().split(); s.note.delete("1.0", "end"); s.note.insert("1.0", " ".join(w[:-1]) + " ")
    def save_note(s):
        f = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="notes.txt")
        if f: open(f, "w", encoding="utf-8").write(s.note.get("1.0", "end"))
    def mic(s):
        s.mst.configure(text="Listening... speak now")
        voice.listen(s.lang, lambda t, e: s.after(0, lambda: (s.add(t) if t else None, s.mst.configure(text="Heard: " + t if t else "Mic error: " + e))))
    def export(s):
        f = filedialog.asksaveasfilename(defaultextension=".json", initialfile="my-signs.json")
        if f: s.eng.save(f)
    def imp(s):
        import json
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            for c in json.load(open(f, encoding="utf-8")): s.eng.add_custom(c["kind"], c["en"], c["ta"], c["samples"])
            s.refresh_lib()

    # ---------------- teach ----------------
    def start_rec(s):
        en = s.en.get().strip()
        if not en: return s.tst.configure(text="Enter an English word first.")
        s.rec = {"kind": "hand" if s.kind.get() == "Hand sign" else "face", "phase": "wait", "n": 3, "samples": [], "en": en, "ta": s.ta.get().strip() or en}
        s.countdown()
    def countdown(s):
        r = s.rec
        if r["n"] > 0: s.tst.configure(text=f"Get ready...  {r['n']}"); r["n"] -= 1; s.after(1000, s.countdown)
        else: r["phase"] = "go"; r["end"] = time.time() + 2.5; s.tst.configure(text="Recording... hold it steady")
    def rec_tick(s):
        r = s.rec
        if not r or r["phase"] != "go": return
        v = s.eng.hand_vec if r["kind"] == "hand" else s.eng.face_vec
        if v is not None: r["samples"].append([round(float(x), 3) for x in v])
        if time.time() > r["end"]:
            if len(r["samples"]) < 10: s.tst.configure(text="Not seen clearly. Try again with better light.")
            else:
                s.eng.add_custom(r["kind"], r["en"], r["ta"], r["samples"]); s.refresh_lib()
                s.tst.configure(text=f"Saved '{r['en']}' ({len(r['samples'])} samples)")
            s.rec = None

    # ---------------- main loop ----------------
    def feed(s, key):
        n = time.time()
        if key != s.cand: s.cand, s.since = key, n; s.bar.set(0)
        if not key: return
        p = min(1, n - s.since); s.bar.set(p)
        if p >= 1 and not (key == s.last and n - s.lastt < 3):
            w = s.eng.label(key)[1 if s.lang == "ta" else 0]
            s.add(w)
            if s.auto.get(): voice.speak(w, s.lang)
            s.last, s.lastt, s.since = key, n, n
    def loop(s):
        ok, f = s.cap.read()
        if ok:
            f = cv2.flip(f, 1)
            use_face = bool(s.face.get()) or bool(s.rec and s.rec["kind"] == "face")
            key, hr, fr = s.eng.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), use_face)
            s.eng.annotate(f, hr, fr); s.rec_tick(); s.feed(key)
            s.now.configure(text=s.eng.label(key)[1 if s.lang == "ta" else 0] if key else "")
            s.img = ctk.CTkImage(Image.fromarray(cv2.cvtColor(cv2.resize(f, (640, 480)), cv2.COLOR_BGR2RGB)), size=(640, 480))
            s.cam.configure(image=s.img)
        s.after(15, s.loop)
    def close(s): s.cap.release(); s.destroy()

if __name__ == "__main__":
    App().mainloop()
