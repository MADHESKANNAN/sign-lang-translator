import json, os, math
import numpy as np
import mediapipe as mp

SIGNS = {  # key: (English, Tamil)
 "hello": ("Hello", "வணக்கம்"), "yes": ("Yes", "ஆம்"), "good": ("Good", "நல்லது"),
 "bad": ("Bad", "மோசம்"), "peace": ("Peace", "அமைதி"), "love": ("I love you", "நான் உன்னை நேசிக்கிறேன்"),
 "wait": ("Wait", "காத்திரு"), "ok": ("OK", "சரி"), "call": ("Call me", "எனக்கு அழை"),
 "three": ("Three", "மூன்று"), "four": ("Four", "நான்கு"),
 "happy": ("Happy", "மகிழ்ச்சி"), "surprised": ("Surprised", "ஆச்சரியம்"), "sleepy": ("Sleepy", "தூக்கம்")}
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "custom_signs.json")

class Engine:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=.6, min_tracking_confidence=.5)
        self.face = mp.solutions.face_mesh.FaceMesh(max_num_faces=1)
        self.sens = 1.2
        self.hand_vec = self.face_vec = None
        self.custom = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else []

    # ---------- storage ----------
    def save(self, path=DATA):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump([{k: v for k, v in c.items() if k != "_np"} for c in self.custom],
                  open(path, "w", encoding="utf-8"), ensure_ascii=False)
    def add_custom(self, kind, en, ta, samples):
        for c in self.custom:
            if c["en"].lower() == en.lower() and c["kind"] == kind:
                c["samples"] += samples; c.pop("_np", None); break
        else:
            self.custom.append({"kind": kind, "en": en, "ta": ta, "samples": samples})
        self.save()
    def delete(self, c): self.custom.remove(c); self.save()
    def label(self, key):
        if key in SIGNS: return SIGNS[key]
        for c in self.custom:
            if "c:" + c["en"] == key: return c["en"], c["ta"]
        return key, key

    # ---------- features ----------
    def hvec(self, l):
        s = math.hypot(l[9].x - l[0].x, l[9].y - l[0].y) or 1
        return np.array([c for p in l for c in ((p.x - l[0].x) / s, (p.y - l[0].y) / s, (p.z - l[0].z) / s)], dtype=np.float32)
    def fvec(self, l):
        w = math.hypot(l[234].x - l[454].x, l[234].y - l[454].y) or 1
        return np.array([c for i in range(0, 468, 6) for c in ((l[i].x - l[1].x) / w, (l[i].y - l[1].y) / w)], dtype=np.float32)
    def match(self, vec, kind, th):
        best, bd = None, 1e9
        for c in self.custom:
            if c["kind"] != kind: continue
            a = c.get("_np")
            if a is None or len(a) != len(c["samples"]): a = c["_np"] = np.array(c["samples"], dtype=np.float32)
            d = np.linalg.norm(a - vec, axis=1).min()
            if d < bd: best, bd = c, d
        return "c:" + best["en"] if best and bd < th else None

    # ---------- built-in rules ----------
    def rule(self, l):
        d = lambda a, b: math.hypot(l[a].x - l[b].x, l[a].y - l[b].y)
        t = d(4, 17) > d(3, 17); i, m, r, p = (d(x, 0) > d(x - 2, 0) for x in (8, 12, 16, 20))
        if d(4, 8) < .05 and m and r and p: return "ok"
        if t and i and m and r and p: return "hello"
        if not (t or i or m or r or p): return "yes"
        if t and not (i or m or r or p):
            return "good" if l[4].y < l[0].y - .08 else "bad" if l[4].y > l[0].y + .08 else None
        if i and not (m or r or p or t): return "wait"
        if i and m and not (r or p or t): return "peace"
        if t and i and p and not (m or r): return "love"
        if t and p and not (i or m or r): return "call"
        if i and m and r and not (p or t): return "three"
        if i and m and r and p and not t: return "four"
    def expr(self, l):
        d = lambda a, b: math.hypot(l[a].x - l[b].x, l[a].y - l[b].y)
        if d(61, 291) / d(234, 454) > .44: return "happy"
        if d(13, 14) / d(10, 152) > .09: return "surprised"
        if (d(159, 145) + d(386, 374)) / (d(33, 133) + d(362, 263)) < .10: return "sleepy"

    # ---------- main ----------
    def process(self, rgb, use_face=True):
        key = None; self.hand_vec = self.face_vec = None
        hr = self.hands.process(rgb)
        if hr.multi_hand_landmarks:
            l = hr.multi_hand_landmarks[0].landmark
            self.hand_vec = self.hvec(l)
            key = self.match(self.hand_vec, "hand", self.sens) or self.rule(l)
        fr = self.face.process(rgb) if use_face else None
        if fr and fr.multi_face_landmarks:
            l = fr.multi_face_landmarks[0].landmark
            self.face_vec = self.fvec(l)
            if not key: key = self.match(self.face_vec, "face", self.sens * .25) or self.expr(l)
        return key, hr, fr
    def annotate(self, bgr, hr, fr):
        du, sp = mp.solutions.drawing_utils, mp.solutions.drawing_utils.DrawingSpec
        if hr.multi_hand_landmarks:
            du.draw_landmarks(bgr, hr.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS, sp((255, 235, 104), 3, 3), sp((255, 255, 255), 2))
        if fr and fr.multi_face_landmarks:
            du.draw_landmarks(bgr, fr.multi_face_landmarks[0], mp.solutions.face_mesh.FACEMESH_CONTOURS, None, sp((255, 95, 197), 1))
