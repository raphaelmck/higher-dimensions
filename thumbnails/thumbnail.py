import numpy as np
from manim import *

BG  = "#08080F"
COL = "#58C4DD"


class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG

        xs    = [-4.8, -1.6, 1.6, 4.8]
        obj_y = 0.7
        lbl_y = -1.6

        # ── rotation helpers ──────────────────────────────────────────────────
        def ry(v, a):
            x, y, z = v
            return np.array([x*np.cos(a) + z*np.sin(a), y, -x*np.sin(a) + z*np.cos(a)])

        def rx(v, a):
            x, y, z = v
            return np.array([x, y*np.cos(a) - z*np.sin(a), y*np.sin(a) + z*np.cos(a)])

        # ── 1. point ──────────────────────────────────────────────────────────
        point = Dot(ORIGIN, radius=0.16, color=COL)
        point.move_to([xs[0], obj_y, 0])

        # ── 2. square ─────────────────────────────────────────────────────────
        square = Square(side_length=1.6, stroke_width=3.0, color=COL, fill_opacity=0)
        square.move_to([xs[1], obj_y, 0])

        # ── 3. cube ───────────────────────────────────────────────────────────
        ay, ax = 35 * DEGREES, 22 * DEGREES
        r = 0.82
        raw_verts = [
            (-r,-r,-r),(r,-r,-r),(r,r,-r),(-r,r,-r),
            (-r,-r, r),(r,-r, r),(r,r, r),(-r,r, r),
        ]
        rotated   = [rx(ry(np.array(v), ay), ax) for v in raw_verts]
        back_idx  = int(np.argmax([v[2] for v in rotated]))
        v2d       = [np.array([v[0], v[1], 0]) for v in rotated]

        edge_idx = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7),
        ]
        offset   = np.array([xs[2], obj_y, 0])
        cube_grp = VGroup()
        for i, j in edge_idx:
            hidden = (i == back_idx or j == back_idx)
            line   = Line(v2d[i] + offset, v2d[j] + offset,
                          color=COL, stroke_width=2.8)
            line.set_opacity(0.22 if hidden else 1.0)
            cube_grp.add(line)

        # ── 4. question mark ──────────────────────────────────────────────────
        qmark = MathTex(r"?", font_size=120, color=COL)
        qmark.move_to([xs[3], obj_y, 0])

        # ── labels ────────────────────────────────────────────────────────────
        label_tex = [
            r"\mathbb{R}",
            r"\mathbb{R}^2",
            r"\mathbb{R}^3",
            r"\mathbb{R}^n",
        ]
        lbls = VGroup(*[
            MathTex(s, font_size=60, color=WHITE).move_to([xs[i], lbl_y, 0])
            for i, s in enumerate(label_tex)
        ])

        self.add(point, square, cube_grp, qmark, lbls)
        self.wait(0.01)
