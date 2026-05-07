from manim import *
from PIL import Image
import numpy as np
import os, tempfile


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

        # ── 3. Scan-line flatten → 1-D strip ──────────────────────────────
        self.play(grid.animate.move_to(UP * 1.0), run_time=0.5)

        STRIP_W, STRIP_H = 10.5, 0.45
        strip_cx = 0.0
        strip_cy = grid.get_bottom()[1] - 0.35 - STRIP_H / 2
        seg_w    = STRIP_W / G   # one row's slice of the strip

        g_top   = grid.get_top()[1]
        g_h     = grid.get_height()
        g_left  = grid.get_left()[0]
        g_right = grid.get_right()[0]

        # ── 3a. Pixel-by-pixel intro (first 3 pixels) ────────────────────
        pix_lbl_pos = grid.get_right() + RIGHT * 0.5 + UP * 0.85
        prev_phl  = None
        coord_lbl = None
        for pi, pj, cs in [(0, 0, r"x_1"), (0, 1, r"x_2"), (0, 2, r"x_3")]:
            sq  = grid[pi * G + pj]
            phl = SurroundingRectangle(sq, color=WHITE, buff=0.0, stroke_width=3.5)
            new_lbl = MathTex(cs, font_size=30, color=WHITE).move_to(pix_lbl_pos)
            if prev_phl is None:
                self.play(Create(phl), FadeIn(new_lbl), run_time=0.25)
                coord_lbl = new_lbl
            else:
                self.play(
                    ReplacementTransform(prev_phl, phl),
                    Transform(coord_lbl, new_lbl),
                    run_time=0.2,
                )
            self.wait(0.2)
            prev_phl = phl
        cdots = MathTex(r"\cdots", font_size=30, color=WHITE).move_to(pix_lbl_pos)
        self.play(FadeOut(prev_phl), Transform(coord_lbl, cdots), run_time=0.2)
        self.wait(0.3)
        self.play(FadeOut(coord_lbl), run_time=0.2)

        # ── 3b. Tracked pixel: pixel(3,7) → x_119 ────────────────────────
        # 0-indexed (i=2,j=6) → 1-indexed row 3, col 7 → x_{56·2+7} = x_119
        track_i, track_j = 2, 6
        track_sq  = grid[track_i * G + track_j]
        track_hl  = SurroundingRectangle(track_sq, color=ORANGE, buff=0.0, stroke_width=3.5)
        track_lbl = MathTex(
            r"\text{pixel}(3,\,7) \;\longrightarrow\; x_{119}",
            font_size=27, color=ORANGE,
        ).next_to(grid, RIGHT, buff=0.45).shift(UP * 0.55)
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

        # Strip border appears before the row animations begin
        strip_border = Rectangle(
            width=STRIP_W, height=STRIP_H,
            fill_opacity=0, stroke_color=WHITE, stroke_width=1.5,
        ).move_to([strip_cx, strip_cy, 0])
        self.play(Create(strip_border), run_time=0.35)

        # ── 3c. Row 1: highlight → collapses into strip ───────────────────
        row0_group = VGroup(*[grid[j] for j in range(G)])
        row0_hl    = SurroundingRectangle(row0_group, color=YELLOW, buff=0.01, stroke_width=2)
        self.play(Create(row0_hl), run_time=0.4)
        self.wait(0.2)

        avg0     = float(arr[0].mean())
        seg0_tgt = Rectangle(
            width=seg_w * 0.95, height=STRIP_H * 0.88,
            fill_color=rgb_to_hex((avg0, avg0, avg0)),
            fill_opacity=1, stroke_width=0,
        ).move_to([strip_cx - STRIP_W / 2 + 0.5 * seg_w, strip_cy, 0])

        row_lbl_pos = grid.get_right() + RIGHT * 0.45
        row0_side_lbl = Tex(
            rf"row 1 $\to x_1, \ldots, x_{{{G}}}$",
            font_size=24, color=YELLOW,
        ).move_to(row_lbl_pos + UP * 0.4)

        self.play(
            Transform(row0_hl, seg0_tgt),
            FadeIn(row0_side_lbl, shift=LEFT * 0.1),
            run_time=0.6,
        )
        self.wait(0.35)

        # ── 3d. Row 2: highlight → collapses into strip ───────────────────
        row1_group = VGroup(*[grid[G + j] for j in range(G)])
        row1_hl    = SurroundingRectangle(row1_group, color=GREEN, buff=0.01, stroke_width=2)
        self.play(Create(row1_hl), run_time=0.4)
        self.wait(0.2)

        avg1     = float(arr[1].mean())
        seg1_tgt = Rectangle(
            width=seg_w * 0.95, height=STRIP_H * 0.88,
            fill_color=rgb_to_hex((avg1, avg1, avg1)),
            fill_opacity=1, stroke_width=0,
        ).move_to([strip_cx - STRIP_W / 2 + 1.5 * seg_w, strip_cy, 0])

        row1_side_lbl = Tex(
            rf"row 2 $\to x_{{{G+1}}}, \ldots, x_{{{2*G}}}$",
            font_size=24, color=GREEN,
        ).move_to(row_lbl_pos + DOWN * 0.1)

        self.play(
            Transform(row1_hl, seg1_tgt),
            FadeOut(row0_side_lbl),
            FadeIn(row1_side_lbl, shift=LEFT * 0.1),
            run_time=0.6,
        )
        self.wait(0.35)

        # ── 3e. Rows 3–56: rapid scan reveals tail image ──────────────────
        # Build an image only for rows 3-56 so the first two segments stay clean
        h_px     = 80
        flat_tail = arr[2:].flatten()                              # (54·G,)
        tail_px   = np.repeat(
            (flat_tail[np.newaxis, :] * 255).astype(np.uint8), h_px, axis=0,
        )
        tail_px = np.stack([tail_px] * 3, axis=-1)
        tmp_tail = os.path.join(tempfile.gettempdir(), "hd_strip_tail.png")
        Image.fromarray(tail_px).save(tmp_tail)

        tail_w  = STRIP_W * (G - 2) / G
        tail_cx = strip_cx - STRIP_W / 2 + 2 * seg_w + tail_w / 2
        strip_img = (
            ImageMobject(tmp_tail)
            .set_width(tail_w)
            .set_height(STRIP_H * 0.88)
            .move_to([tail_cx, strip_cy, 0])
        )
        strip_img.z_index = -1   # behind the two row-segment rectangles

        cover_left  = strip_cx - STRIP_W / 2 + 2 * seg_w
        cover_right = strip_cx + STRIP_W / 2
        cover_w0    = tail_w
        cover = Rectangle(
            width=cover_w0, height=STRIP_H + 0.06,
            fill_color=BLACK, fill_opacity=1, stroke_width=0,
        ).move_to([cover_left + cover_w0 / 2, strip_cy, 0])

        scan_y0   = g_top - (2.0 / G) * g_h
        scan_line = Line([g_left, scan_y0, 0], [g_right, scan_y0, 0],
                         color=YELLOW, stroke_width=2.5)

        self.add(strip_img, cover, scan_line)

        remaining_frac = (G - 2) / G

        def update_scan_rapid(mob, alpha):
            frac = 2.0 / G + alpha * remaining_frac
            mob.put_start_and_end_on([g_left, g_top - frac * g_h, 0],
                                     [g_right, g_top - frac * g_h, 0])

        def update_cover_rapid(mob, alpha):
            w = max(0.001, cover_w0 * (1 - alpha))
            mob.become(
                Rectangle(
                    width=w, height=STRIP_H + 0.06,
                    fill_color=BLACK, fill_opacity=1, stroke_width=0,
                ).move_to([cover_right - w / 2, strip_cy, 0])
            )

        self.play(
            UpdateFromAlphaFunc(scan_line, update_scan_rapid),
            UpdateFromAlphaFunc(cover, update_cover_rapid),
            FadeOut(row1_side_lbl),
            run_time=1.8,
            rate_func=linear,
        )
        self.play(FadeOut(scan_line), run_time=0.3)

        # ── 3f. Endpoint labels + vector formula ──────────────────────────
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

        # ── 4. Abstract to R^3136 ─────────────────────────────────────────
        r3136 = MathTex(r"x \in \mathbb{R}^{3136}", font_size=68).move_to(ORIGIN)
        self.play(
            FadeOut(grid),
            FadeOut(strip_img),
            FadeOut(strip_border),
            FadeOut(row0_hl),
            FadeOut(row1_hl),
            FadeOut(x1_lbl),
            FadeOut(xn_lbl),
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
        ).move_to(UP * 2.3)
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
