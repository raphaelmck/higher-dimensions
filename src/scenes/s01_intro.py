from manim import *
from PIL import Image
import numpy as np


class DimensionHook(Scene):
    GRID_SIZE = 56  # exact 2x NEAREST downscale of 112x112 → 3,136 px
    SQ = 0.1        # manim units per pixel square (grid = 5.6×5.6 units)

    def construct(self):
        G = self.GRID_SIZE
        arr, mask = self._load_sprite("charizard.png", G)
        grid = self._build_grid(arr, mask)

        # ── 1. Reveal the sprite ──────────────────────────────────────────
        sprite_label = Tex(rf"${G} \times {G}$ pixel sprite", font_size=36).next_to(grid, UP, buff=0.3)
        self.play(FadeIn(grid), FadeIn(sprite_label), run_time=0.8)
        self.wait(0.6)

        # ── 2. Shift left, introduce row structure ────────────────────────
        self.play(grid.animate.shift(LEFT * 2.8), FadeOut(sprite_label), run_time=0.6)

        row_defs = [
            (0,     YELLOW, rf"row 1: $x_1, \ldots, x_{{{G}}}$"),
            (1,     GREEN,  rf"row 2: $x_{{{G+1}}}, \ldots, x_{{{2*G}}}$"),
            (2,     BLUE,   rf"row 3: $x_{{{2*G+1}}}, \ldots, x_{{{3*G}}}$"),
            (G - 1, ORANGE, rf"row {G}: $x_{{{(G-1)*G+1}}}, \ldots, x_{{{G*G}}}$"),
        ]

        prev_rect = prev_label = dots = None
        for k, (row_idx, color, tex) in enumerate(row_defs):
            row_group = VGroup(*[grid[row_idx * G + j] for j in range(G)])
            rect = SurroundingRectangle(row_group, color=color, buff=0.01, stroke_width=2)
            y_off = UP * (0.9 - min(k, 2) * 0.75) if k < 3 else DOWN * 1.55
            lbl = Tex(tex, font_size=26, color=color).next_to(grid, RIGHT, buff=0.4).shift(y_off)

            if k == 3:
                dots = Tex(r"$\vdots$", font_size=34).next_to(grid, RIGHT, buff=0.4).shift(DOWN * 0.75)
                self.play(
                    ReplacementTransform(prev_rect, rect),
                    ReplacementTransform(prev_label, lbl),
                    FadeIn(dots),
                    run_time=0.5,
                )
            elif prev_rect is None:
                self.play(Create(rect), FadeIn(lbl, shift=LEFT * 0.15), run_time=0.5)
            else:
                self.play(
                    ReplacementTransform(prev_rect, rect),
                    ReplacementTransform(prev_label, lbl),
                    run_time=0.5,
                )
            prev_rect, prev_label = rect, lbl
            self.wait(0.45)

        self.play(FadeOut(prev_rect), FadeOut(prev_label), FadeOut(dots), run_time=0.4)

        # ── 3. Scan-line flatten → 1-D strip ──────────────────────────────
        # Move grid back to center and up to make room for the strip below
        self.play(grid.animate.move_to(UP * 1.0), run_time=0.5)

        STRIP_W, STRIP_H = 10.5, 0.45
        strip_cx = 0.0
        strip_cy = grid.get_bottom()[1] - 0.35 - STRIP_H / 2  # just below grid

        g_top   = grid.get_top()[1]
        g_h     = grid.get_height()
        g_left  = grid.get_left()[0]
        g_right = grid.get_right()[0]

        scan_line = Line([g_left, g_top, 0], [g_right, g_top, 0], color=YELLOW, stroke_width=2.5)
        strip_rect = Rectangle(
            width=0.001, height=STRIP_H,
            fill_color="#111111", fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to([strip_cx - STRIP_W / 2, strip_cy, 0])

        self.add(scan_line, strip_rect)

        def update_scan(mob, alpha):
            y = g_top - alpha * g_h
            mob.put_start_and_end_on([g_left, y, 0], [g_right, y, 0])

        def update_strip(mob, alpha):
            w = max(0.001, alpha * STRIP_W)
            mob.become(
                Rectangle(
                    width=w, height=STRIP_H,
                    fill_color="#111111", fill_opacity=1,
                    stroke_color=WHITE, stroke_width=1.5,
                ).move_to([strip_cx - STRIP_W / 2 + w / 2, strip_cy, 0])
            )

        self.play(
            UpdateFromAlphaFunc(scan_line, update_scan),
            UpdateFromAlphaFunc(strip_rect, update_strip),
            run_time=2.0,
            rate_func=linear,
        )
        self.play(FadeOut(scan_line), run_time=0.3)

        vec_label = MathTex(
            r"x = (x_1,\ x_2,\ \ldots,\ x_{3136})", font_size=38
        ).next_to(strip_rect, DOWN, buff=0.22)
        self.play(Write(vec_label), run_time=0.8)
        self.wait(0.8)

        # ── 4. Abstract to R^3136 ─────────────────────────────────────────
        r3136 = MathTex(r"x \in \mathbb{R}^{3136}", font_size=68).move_to(ORIGIN)
        self.play(
            FadeOut(grid),
            FadeOut(strip_rect),
            Transform(vec_label, r3136),
            run_time=0.7,
        )
        self.wait(1)

        # ── 5. Smash-cut to a real image ──────────────────────────────────
        # 4K: 3840 × 2160 × 3 = 24,883,200
        real = MathTex(r"x \in \mathbb{R}^{24{,}883{,}200}", font_size=68).move_to(ORIGIN)
        footnote = Tex(
            r"(4K photo: $3840 \times 2160 \times 3$ channels)",
            font_size=24, color=GRAY_C,
        ).next_to(real, DOWN, buff=0.35)
        self.play(Transform(vec_label, real), run_time=0.3)
        self.play(FadeIn(footnote), run_time=0.4)
        self.wait(1.5)

        # ── 6. Thesis ─────────────────────────────────────────────────────
        thesis = Text(
            "Dimension = number of independent values",
            weight=BOLD, font_size=38,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(thesis, shift=DOWN * 0.3), run_time=0.8)
        self.wait(2)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _load_sprite(self, path, size):
        img = Image.open(path).convert("RGBA")
        # Crop to content bounding box
        a = np.array(img)[:, :, 3]
        rmin, rmax = np.where(np.any(a > 0, axis=1))[0][[0, -1]]
        cmin, cmax = np.where(np.any(a > 0, axis=0))[0][[0, -1]]
        content = img.crop((cmin, rmin, cmax + 1, rmax + 1))
        # Re-center in original 112×112 canvas → 2x NEAREST downscale stays integer-perfect
        canvas = Image.new("RGBA", (112, 112), (0, 0, 0, 0))
        cw, ch = content.size
        canvas.paste(content, ((112 - cw) // 2, (112 - ch) // 2))
        small = np.array(canvas.resize((size, size), Image.NEAREST))  # (size, size, 4)
        is_content = small[:, :, 3] > 0
        gray = (0.299 * small[:, :, 0] + 0.587 * small[:, :, 1] + 0.114 * small[:, :, 2]) / 255.0
        return gray, is_content

    def _build_grid(self, arr, mask, seed=42):
        n, SQ = arr.shape[0], self.SQ
        rng = np.random.default_rng(seed)
        # Background shades: very dark gray noise for transparent pixels
        bg_vals = [0.04, 0.06, 0.05, 0.07, 0.05, 0.08, 0.06, 0.05]
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                v = arr[i, j] if mask[i, j] else bg_vals[rng.integers(len(bg_vals))]
                sq = Square(side_length=SQ)
                sq.set_fill(rgb_to_hex((v, v, v)), opacity=1)
                sq.set_stroke(color=GRAY, width=0.2)
                sq.move_to(RIGHT * (j - (n - 1) / 2) * SQ + DOWN * (i - (n - 1) / 2) * SQ)
                grid.add(sq)
        return grid
