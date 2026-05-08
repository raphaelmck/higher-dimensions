import numpy as np
import os
import tempfile
from PIL import Image
from manim import *


class DimensionHook(Scene):
    GRID_SIZE = 56  # exact 2x NEAREST downscale of 112x112 → 3,136 px
    SQ = 0.1  # manim units per pixel square (grid = 5.6×5.6 units)

    def construct(self):
        G = self.GRID_SIZE
        arr, mask = self._load_sprite("charizard.png", G)
        grid = self._build_grid(arr, mask)

        # ── 1. Reveal the greyscale pixel grid ───────────────────────────────
        self.play(FadeIn(grid), run_time=0.8)
        self.wait(0.5)

        # ── 2. Dimension arrows directly on the grid ──────────────────────────
        left_val  = grid.get_left()[0]
        right_val = grid.get_right()[0]
        top_val   = grid.get_top()[1]
        bot_val   = grid.get_bottom()[1]

        top_arrow = DoubleArrow(
            start=[left_val, top_val + 0.3, 0],
            end=[right_val, top_val + 0.3, 0],
            tip_length=0.15, buff=0.05, color=YELLOW_A,
        )
        width_label = MathTex(rf"{G}", font_size=26, color=YELLOW_A).next_to(top_arrow, UP, buff=0.1)

        left_arrow = DoubleArrow(
            start=[left_val - 0.3, top_val, 0],
            end=[left_val - 0.3, bot_val, 0],
            tip_length=0.15, buff=0.05, color=YELLOW_A,
        )
        height_label = MathTex(rf"{G}", font_size=26, color=YELLOW_A).next_to(left_arrow, LEFT, buff=0.1)

        self.play(
            Create(VGroup(top_arrow, left_arrow)),
            FadeIn(VGroup(width_label, height_label)),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(VGroup(top_arrow, width_label, left_arrow, height_label)), run_time=0.5)
        self.wait(0.3)

        # ── 3. White shimmer wave on the gridlines (strokes only) ────────────
        # Pulse brightens stroke color GRAY→WHITE and thickens it temporarily;
        # pixel fill colors are never touched.
        def white_wave(_, alpha):
            pulse_width = 0.07
            pulse_center = alpha * (1 + 2 * pulse_width) - pulse_width
            for i in range(G):
                for j in range(G):
                    idx = i * G + j
                    norm_dist = (i + j) / (2 * (G - 1))
                    effect = np.exp(-((norm_dist - pulse_center) ** 2) / (2 * pulse_width ** 2))
                    grid[idx].set_stroke(
                        color=interpolate_color(GRAY, WHITE, effect),
                        width=0.2 + effect * 1.5,
                    )

        self.play(UpdateFromAlphaFunc(grid, white_wave), run_time=2.0, rate_func=linear)
        for k in range(G * G):
            grid[k].set_stroke(color=GRAY, width=0.2)
        self.wait(1.0)

        # ── 4. Shift left and introduce row structure ──────────────────────────
        self.play(grid.animate.shift(LEFT * 2.8), run_time=0.6)

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
            y_off = UP * (1.2 - min(k, 2) * 0.75) if k < 3 else DOWN * 1.25
            lbl = Tex(tex, font_size=26, color=color).next_to(grid, RIGHT, buff=0.4).shift(y_off)

            if k == 3:
                dots = Tex(r"$\vdots$", font_size=34).next_to(grid, RIGHT, buff=0.4).shift(DOWN * 0.45)
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

        # ── 7. Pixel annotation then scan ─────────────────────────────────────
        # First move to centre so we can capture scan geometry, then shift left
        # so the labels have room on the right, then slide back for the scan.
        self.play(grid.animate.move_to(UP * 1.0), run_time=0.5)

        STRIP_W, STRIP_H = 10.5, 0.45
        strip_cx = 0.0
        # Capture scan geometry while grid is centred (x-coords matter for scan line)
        strip_cy = grid.get_bottom()[1] - 0.35 - STRIP_H / 2
        g_top   = grid.get_top()[1]
        g_h     = grid.get_height()
        g_left  = grid.get_left()[0]
        g_right = grid.get_right()[0]

        # Shift left so labels on the right are clear of the grid
        self.play(grid.animate.shift(LEFT * 1.8), run_time=0.4)
        lbl_anchor = RIGHT * 4.0 + UP * 1.0

        # Off-center tracked pixel: upper-body of charizard
        # 0-indexed (22,28) → 1-indexed row 23, col 29 → x_{56·22+29} = x_{1261}
        track_i, track_j = 22, 28
        track_sq  = grid[track_i * G + track_j]
        track_hl  = SurroundingRectangle(track_sq, color=ORANGE, buff=0.0, stroke_width=3.5)
        track_lbl = MathTex(
            r"\text{pixel}(23,\,29) \;\longrightarrow\; x_{1261}",
            font_size=27, color=ORANGE,
        ).move_to(lbl_anchor)
        formula_lbl = MathTex(
            r"x_{i,j} \;\mapsto\; x_{\,56(i-1)+j}",
            font_size=22, color=GRAY_B,
        ).next_to(track_lbl, DOWN, buff=0.2)

        self.play(Create(track_hl), FadeIn(track_lbl), run_time=0.5)
        self.play(FadeIn(formula_lbl, shift=UP * 0.05), run_time=0.35)
        self.wait(1.0)
        self.play(
            FadeOut(track_hl), FadeOut(track_lbl), FadeOut(formula_lbl),
            run_time=0.4,
        )

        neighbor_seq = [
            (22, 29, BLUE_C,    r"\text{pixel}(23,\,30) \;\longrightarrow\; x_{1262}"),
            (22, 30, TEAL_C,    r"\text{pixel}(23,\,31) \;\longrightarrow\; x_{1263}"),
            (22, 31, GREEN_C,   r"\text{pixel}(23,\,32) \;\longrightarrow\; x_{1264}"),
            (22, 32, PURPLE_C,  r"\text{pixel}(23,\,33) \;\longrightarrow\; x_{1265}"),
        ]
        prev_phl  = None
        coord_lbl = None
        for pi, pj, color, tex in neighbor_seq:
            sq  = grid[pi * G + pj]
            phl = SurroundingRectangle(sq, color=color, buff=0.0, stroke_width=3.5)
            new_lbl = MathTex(tex, font_size=27, color=color).move_to(lbl_anchor)
            if prev_phl is None:
                self.play(Create(phl), FadeIn(new_lbl), run_time=0.3)
                coord_lbl = new_lbl
            else:
                self.play(
                    ReplacementTransform(prev_phl, phl),
                    Transform(coord_lbl, new_lbl),
                    run_time=0.25,
                )
            self.wait(0.25)
            prev_phl = phl
        self.play(FadeOut(prev_phl), FadeOut(coord_lbl), run_time=0.25)

        # Slide grid back to centre before the scan
        self.play(grid.animate.move_to(UP * 1.0), run_time=0.4)

        strip_border = Rectangle(
            width=STRIP_W, height=STRIP_H,
            fill_opacity=0, stroke_color=WHITE, stroke_width=1.5,
        ).move_to([strip_cx, strip_cy, 0])

        h_px = 80
        flat_gray = arr.flatten()
        strip_px  = np.repeat(
            (flat_gray[np.newaxis, :] * 255).astype(np.uint8), h_px, axis=0,
        )
        strip_px  = np.stack([strip_px] * 3, axis=-1)
        tmp_path  = os.path.join(tempfile.gettempdir(), "hd_strip.png")
        Image.fromarray(strip_px).save(tmp_path)
        strip_img = (
            ImageMobject(tmp_path)
            .set_width(STRIP_W)
            .set_height(STRIP_H * 0.88)
            .move_to([strip_cx, strip_cy, 0])
        )
        strip_img.z_index = -1

        right_x = strip_cx + STRIP_W / 2
        cover = Rectangle(
            width=STRIP_W, height=STRIP_H + 0.06,
            fill_color=BLACK, fill_opacity=1, stroke_width=0,
        ).move_to([strip_cx, strip_cy, 0])

        scan_line = Line([g_left, g_top, 0], [g_right, g_top, 0],
                         color=YELLOW, stroke_width=2.5)

        self.add(strip_img, cover, scan_line)

        def update_scan(mob, alpha):
            y = g_top - alpha * g_h
            mob.put_start_and_end_on([g_left, y, 0], [g_right, y, 0])

        def update_cover(mob, alpha):
            w = max(0.001, STRIP_W * (1 - alpha))
            mob.become(
                Rectangle(
                    width=w, height=STRIP_H + 0.06,
                    fill_color=BLACK, fill_opacity=1, stroke_width=0,
                ).move_to([right_x - w / 2, strip_cy, 0])
            )

        self.play(
            UpdateFromAlphaFunc(scan_line, update_scan),
            UpdateFromAlphaFunc(cover, update_cover),
            run_time=2.2,
            rate_func=linear,
        )
        self.play(FadeOut(scan_line), FadeIn(strip_border), run_time=0.35)

        # Endpoint labels + vector formula
        x1_lbl = MathTex(r"x_1", font_size=20, color=YELLOW)
        xn_lbl = MathTex(rf"x_{{{G * G}}}", font_size=20, color=YELLOW)
        x1_lbl.next_to(strip_border, UP, buff=0.07).align_to(strip_border, LEFT).shift(RIGHT * 0.08)
        xn_lbl.next_to(strip_border, UP, buff=0.07).align_to(strip_border, RIGHT).shift(LEFT * 0.08)
        self.play(FadeIn(x1_lbl), FadeIn(xn_lbl), run_time=0.4)
        self.wait(0.2)

        vec_label = MathTex(
            r"x = (x_1,\ x_2,\ \ldots,\ x_{3136})", font_size=38
        ).next_to(strip_border, DOWN, buff=0.22)
        self.play(Write(vec_label), run_time=0.8)
        self.wait(0.8)

        # ── 8. Abstract to R^3136 (unchanged) ────────────────────────────────────
        r3136 = MathTex(r"x \in \mathbb{R}^{3136}", font_size=68).move_to(ORIGIN)
        self.play(
            FadeOut(grid),
            FadeOut(strip_img),
            FadeOut(strip_border),
            FadeOut(x1_lbl),
            FadeOut(xn_lbl),
            Transform(vec_label, r3136),
            run_time=0.7,
        )
        self.wait(1.0)

        # ── 9. Smash-cut to a real image (unchanged) ────────────────────────────
        real = MathTex(r"x \in \mathbb{R}^{24{,}883{,}200}", font_size=68).move_to(ORIGIN)
        footnote = Tex(
            r"(4K photo: $3840 \times 2160 \times 3$ channels)",
            font_size=24, color=GRAY_C,
        ).next_to(real, DOWN, buff=0.35)
        self.play(Transform(vec_label, real), run_time=0.3)
        self.play(FadeIn(footnote), run_time=0.4)
        self.wait(1.5)

        # ── 10. Thesis (unchanged) ──────────────────────────────────────────────────
        thesis = Text(
            "Dimension = number of independent values",
            weight=BOLD, font_size=38,
        ).move_to(UP * 2.3)
        self.play(FadeIn(thesis, shift=DOWN * 0.3), run_time=0.8)
        self.wait(2.0)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _load_sprite(self, path, size):
        img = Image.open(path).convert("RGBA")
        a = np.array(img)[:, :, 3]
        rmin, rmax = np.where(np.any(a > 0, axis=1))[0][[0, -1]]
        cmin, cmax = np.where(np.any(a > 0, axis=0))[0][[0, -1]]
        content = img.crop((cmin, rmin, cmax + 1, rmax + 1))
        canvas = Image.new("RGBA", (112, 112), (0, 0, 0, 0))
        cw, ch = content.size
        canvas.paste(content, ((112 - cw) // 2, (112 - ch) // 2))
        small = np.array(canvas.resize((size, size), Image.NEAREST))
        is_content = small[:, :, 3] > 0
        gray = (0.299 * small[:, :, 0] + 0.587 * small[:, :, 1] + 0.114 * small[:, :, 2]) / 255.0
        return gray, is_content

    def _build_grid(self, arr, mask, seed=42):
        n, SQ = arr.shape[0], self.SQ
        rng = np.random.default_rng(seed)
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
