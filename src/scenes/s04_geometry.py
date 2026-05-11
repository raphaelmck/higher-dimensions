from manim import *
import numpy as np

class DataGeometry(Scene):
    def construct(self):
        # -- STYLING --
        accent_color = TEAL_C
        secondary_color = YELLOW_D
        text_color = WHITE
        
        # --- PART 1: THE MONTAGE (REAL WORLD TO VECTORS) ---
        
        # 1. Image to Vector
        # Build a stylized 3x3 pixel grid
        colors = [BLUE_E, BLUE_D, BLUE_C, BLUE_E, TEAL_E, BLUE_D, TEAL_D, BLUE_C, BLUE_E]
        pixels = VGroup(*[Square(side_length=0.4, fill_opacity=1, fill_color=c, stroke_width=0.5) for c in colors])
        pixels.arrange_in_grid(3, 3, buff=0)
        
        image_label = Text("Photo", font_size=24).next_to(pixels, DOWN)
        image_group = VGroup(pixels, image_label).move_to(LEFT * 4)
        
        image_vector = MathTex(r"x \in \mathbb{R}^n", font_size=36).move_to(image_group)
        image_dot = Dot(color=accent_color).move_to(image_group)

        # 2. Sound to Vector
        # Build a clean sine wave with sample sticks
        axes = Axes(x_range=[0, 2*PI, PI/2], y_range=[-1.5, 1.5, 1], x_length=2.5, y_length=1.5)
        wave = axes.plot(lambda x: np.sin(2*x), color=secondary_color)
        samples = VGroup(*[
            DashedLine(axes.c2p(x, 0), axes.c2p(x, np.sin(2*x)), stroke_width=2, color=WHITE) 
            for x in np.arange(0.2, 2*PI, 0.4)
        ])
        
        sound_label = Text("Sound", font_size=24).next_to(axes, DOWN)
        sound_group = VGroup(axes, wave, samples, sound_label).move_to(ORIGIN)
        
        sound_vector = MathTex(r"(s_1, s_2, \dots, s_n)", font_size=36).move_to(sound_group)
        sound_dot = Dot(color=accent_color).move_to(sound_group)

        # 3. Data to Vector
        # Build a minimalist data table
        table = Table(
            [["Age", "Height", "Score"], ["24", "1.75", "88"], ["31", "1.82", "92"]],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY_B}
        ).scale(0.3)
        
        # Highlight a specific row to show extraction
        row_highlight = BackgroundRectangle(table.get_rows()[1], color=accent_color, fill_opacity=0.3, buff=0.05)
        
        data_label = Text("User Profile", font_size=24).next_to(table, DOWN, buff=0.4)
        data_group = VGroup(table, row_highlight, data_label).move_to(RIGHT * 4)
        
        data_vector = MathTex(r"(v_1, v_2, \dots, v_n)", font_size=36).move_to(data_group)
        data_dot = Dot(color=accent_color).move_to(data_group)

        # -- Animate Montage --
        self.play(FadeIn(image_group, shift=UP*0.2), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(sound_group, shift=UP*0.2), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(data_group, shift=UP*0.2), run_time=0.8)
        self.wait(0.8)
        
        # "Smash" them into math vectors
        self.play(
            Transform(image_group, image_vector),
            Transform(sound_group, sound_vector),
            Transform(data_group, data_vector),
            run_time=1
        )
        self.wait(0.5)
        
        # Collapse the math into abstract points (the core thesis)
        self.play(
            Transform(image_group, image_dot),
            Transform(sound_group, sound_dot),
            Transform(data_group, data_dot),
            run_time=1
        )
        self.wait(0.5)

        # Move the points to the center to form a "dataset"
        dataset = VGroup(image_group, sound_group, data_group)
        self.play(dataset.animate.arrange(RIGHT, buff=0.5).move_to(ORIGIN))
        
        # Fade out to clear the canvas for the toolkit
        self.play(FadeOut(dataset, scale=0.5))
        self.wait(0.5)


        # --- PART 2: THE 2x2 GEOMETRY TOOLKIT ---
        
        # Helper to create uniform boxes for the 2x2 grid
        def create_tool_panel(title_str, math_str, visual_vgroup):
            box = RoundedRectangle(width=5.5, height=3, corner_radius=0.2, color=GRAY_D, fill_opacity=0.1)
            title = Text(title_str, font_size=20, color=GRAY_B).next_to(box.get_top(), DOWN, buff=0.2)
            math_text = MathTex(math_str, font_size=32).next_to(box.get_bottom(), UP, buff=0.2)
            visual_vgroup.move_to(box.get_center())
            return VGroup(box, title, visual_vgroup, math_text)

        # 1. Distance (Similarity)
        d_dot1 = Dot(LEFT*1 + DOWN*0.2, color=accent_color)
        d_dot2 = Dot(RIGHT*1 + UP*0.5, color=secondary_color)
        d_line = DashedLine(d_dot1.get_center(), d_dot2.get_center(), color=WHITE)
        distance_visual = VGroup(d_dot1, d_dot2, d_line)
        panel_distance = create_tool_panel("Similarity", r"\|x - y\|", distance_visual)

        # 2. Angle (Alignment)
        v1 = Arrow(ORIGIN, RIGHT*1.5 + UP*0.5, buff=0, color=accent_color)
        v2 = Arrow(ORIGIN, RIGHT*1.2 + DOWN*0.8, buff=0, color=secondary_color)
        angle = Angle(v1, v2, radius=0.5, color=WHITE)
        angle_visual = VGroup(v1, v2, angle)
        panel_angle = create_tool_panel("Alignment", r"x \cdot y", angle_visual)

        # 3. Hyperplane (Decision Boundary)
        h_line = Line(DOWN*1.2 + LEFT*1.5, UP*1.2 + RIGHT*1.5, color=WHITE, stroke_width=2)
        # Fixed positions verified to lie on the correct side of y = 0.8x
        pts_left = VGroup(*[Dot(p, color=accent_color) for p in [
            LEFT*1.4 + UP*0.6, LEFT*1.0 + UP*0.9, LEFT*0.7 + UP*0.3,
            LEFT*1.2 + DOWN*0.1, LEFT*0.5 + UP*0.7,
        ]])
        pts_right = VGroup(*[Dot(p, color=secondary_color) for p in [
            RIGHT*1.4 + DOWN*0.6, RIGHT*1.0 + DOWN*0.9, RIGHT*0.7 + DOWN*0.3,
            RIGHT*1.2 + UP*0.1, RIGHT*0.5 + DOWN*0.7,
        ]])
        boundary_visual = VGroup(h_line, pts_left, pts_right)
        panel_boundary = create_tool_panel("Decision Boundary", r"w^\top x + b = 0", boundary_visual)

        # 4. Projection (Compression)
        p_line = Line(LEFT*2, RIGHT*2, color=GRAY_C, stroke_width=2)
        p_dot = Dot(UP*1 + LEFT*0.5, color=accent_color)
        p_proj_dot = Dot(LEFT*0.5, color=secondary_color)
        p_drop = DashedLine(p_dot.get_center(), p_proj_dot.get_center(), color=WHITE)
        right_angle = RightAngle(p_line, p_drop, length=0.2, quadrant=(1,-1))
        proj_visual = VGroup(p_line, p_dot, p_drop, p_proj_dot, right_angle)
        panel_projection = create_tool_panel("Compression", r"x \mapsto Px", proj_visual)

        # Arrange the 4 panels into a grid
        toolkit = VGroup(panel_distance, panel_angle, panel_boundary, panel_projection)
        toolkit.arrange_in_grid(2, 2, buff=0.5)

        # Animate the tools appearing synchronously with the narration
        self.play(FadeIn(panel_distance, shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeIn(panel_angle, shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeIn(panel_boundary, shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeIn(panel_projection, shift=UP*0.2))
        self.wait(1.5)

        self.play(FadeOut(toolkit), run_time=1.0)


class PanelGlow(Scene):
    def construct(self):
        accent_color = TEAL_C
        secondary_color = YELLOW_D

        def create_tool_panel(title_str, math_str, visual_vgroup):
            box = RoundedRectangle(width=5.5, height=3, corner_radius=0.2, color=GRAY_D, fill_opacity=0.1)
            title = Text(title_str, font_size=20, color=GRAY_B).next_to(box.get_top(), DOWN, buff=0.2)
            math_text = MathTex(math_str, font_size=32).next_to(box.get_bottom(), UP, buff=0.2)
            visual_vgroup.move_to(box.get_center())
            return VGroup(box, title, visual_vgroup, math_text)

        d_dot1 = Dot(LEFT*1 + DOWN*0.2, color=accent_color)
        d_dot2 = Dot(RIGHT*1 + UP*0.5, color=secondary_color)
        d_line = DashedLine(d_dot1.get_center(), d_dot2.get_center(), color=WHITE)
        panel_distance = create_tool_panel("Similarity", r"\|x - y\|", VGroup(d_dot1, d_dot2, d_line))

        v1 = Arrow(ORIGIN, RIGHT*1.5 + UP*0.5, buff=0, color=accent_color)
        v2 = Arrow(ORIGIN, RIGHT*1.2 + DOWN*0.8, buff=0, color=secondary_color)
        panel_angle = create_tool_panel("Alignment", r"x \cdot y", VGroup(v1, v2, Angle(v1, v2, radius=0.5, color=WHITE)))

        h_line = Line(DOWN*1.2 + LEFT*1.5, UP*1.2 + RIGHT*1.5, color=WHITE, stroke_width=2)
        pts_left = VGroup(*[Dot(p, color=accent_color) for p in [LEFT*1.4+UP*0.6, LEFT*1.0+UP*0.9, LEFT*0.7+UP*0.3, LEFT*1.2+DOWN*0.1, LEFT*0.5+UP*0.7]])
        pts_right = VGroup(*[Dot(p, color=secondary_color) for p in [RIGHT*1.4+DOWN*0.6, RIGHT*1.0+DOWN*0.9, RIGHT*0.7+DOWN*0.3, RIGHT*1.2+UP*0.1, RIGHT*0.5+DOWN*0.7]])
        panel_boundary = create_tool_panel("Decision Boundary", r"w^\top x + b = 0", VGroup(h_line, pts_left, pts_right))

        p_line = Line(LEFT*2, RIGHT*2, color=GRAY_C, stroke_width=2)
        p_dot = Dot(UP*1 + LEFT*0.5, color=accent_color)
        p_proj_dot = Dot(LEFT*0.5, color=secondary_color)
        p_drop = DashedLine(p_dot.get_center(), p_proj_dot.get_center(), color=WHITE)
        panel_projection = create_tool_panel("Compression", r"x \mapsto Px", VGroup(p_line, p_dot, p_drop, p_proj_dot, RightAngle(p_line, p_drop, length=0.2, quadrant=(1,-1))))

        toolkit = VGroup(panel_distance, panel_angle, panel_boundary, panel_projection)
        toolkit.arrange_in_grid(2, 2, buff=0.5)
        self.add(toolkit)
        self.wait(0.3)

        # Sequential rectangle pulse — outer halo + crisp edge, smooth in/out
        boxes = [panel[0] for panel in [panel_distance, panel_angle, panel_boundary, panel_projection]]
        for box in boxes:
            halo = box.copy().set_fill(opacity=0).set_stroke(WHITE, width=10, opacity=0)
            edge = box.copy().set_fill(opacity=0).set_stroke(WHITE, width=1.5, opacity=0)
            self.add(halo, edge)
            self.play(
                halo.animate.set_stroke(opacity=0.12),
                edge.animate.set_stroke(opacity=0.75),
                rate_func=there_and_back_with_pause,
                run_time=1.4,
            )
            self.remove(halo, edge)
        self.wait(1.0)
