from manim import *
import numpy as np

class DimensionEscalation(ThreeDScene):
    def construct(self):
        # -- STYLING --
        # Using a distinct, vibrant color against a minimalist background
        accent_color = TEAL_C 
        
        # Initialize the full 3D axes from the start to prevent transition jumps
        axes = ThreeDAxes(
            x_range=[-4, 4, 1], 
            y_range=[-3, 3, 1], 
            z_range=[-3, 3, 1],
            x_length=8, y_length=6, z_length=6
        )
        
        # --- 1D SPACE ---
        # Only draw the x-axis initially
        x_axis = axes.get_x_axis()
        dot_1d = Dot(axes.c2p(2, 0, 0), color=accent_color, radius=0.1)
        label_1d = MathTex(r"x \in \mathbb{R}").next_to(dot_1d, UP, buff=0.4)
        
        self.play(Create(x_axis), run_time=1.5)
        self.play(FadeIn(dot_1d, scale=0.5), Write(label_1d))
        self.wait(1)
        
        # --- 2D SPACE ---
        y_axis = axes.get_y_axis()
        dot_2d = Dot(axes.c2p(2, 2, 0), color=accent_color, radius=0.1)
        label_2d = MathTex(r"(x, y) \in \mathbb{R}^2").next_to(dot_2d, UR, buff=0.2)
        
        self.play(Create(y_axis), run_time=1)
        self.play(
            dot_1d.animate.move_to(dot_2d.get_center()),
            TransformMatchingTex(label_1d, label_2d),
            run_time=1.5
        )
        self.wait(1)
        
        # --- 3D SPACE ---
        z_axis = axes.get_z_axis()
        # Transform the flat dot into a true 3D sphere so it has volume when the camera moves
        dot_3d = Sphere(radius=0.1, resolution=(16, 16)).set_color(accent_color)
        dot_3d.move_to(axes.c2p(2, 2, 2))
        
        # Fix the 3D label to the camera frame so it doesn't skew during rotation
        label_3d = MathTex(r"(x, y, z) \in \mathbb{R}^3")
        label_3d.to_corner(UR, buff=1)
        self.add_fixed_in_frame_mobjects(label_3d)
        
        # Move camera and draw Z simultaneously
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(Create(z_axis), run_time=1)
        
        self.play(
            ReplacementTransform(dot_1d, dot_3d),
            TransformMatchingTex(label_2d, label_3d),
            run_time=1.5
        )
        self.wait(1.5)
        
        # --- n-DIMENSIONAL SPACE (UI Overlay) ---
        # Reset camera back to a flat front view
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        
        label_nd = MathTex(r"(x_1, x_2, \dots, x_n) \in \mathbb{R}^n").scale(1.3)
        label_nd.move_to(UP * 2)
        self.add_fixed_in_frame_mobjects(label_nd)
        
        # Fade out the physical representation, leaving only the abstract math
        self.play(
            FadeOut(axes, dot_3d),
            ReplacementTransform(label_3d, label_nd),
            run_time=1.5
        )
        
        # Build the minimalist slider UI
        sliders = VGroup()
        slider_labels = ["x_1", "x_2", "x_3", r"\vdots", "x_n"]
        
        for i, text in enumerate(slider_labels):
            slider_group = VGroup()
            
            if text == r"\vdots":
                label = MathTex(text).scale(0.8)
                slider_group.add(label)
                slider_group.move_to(RIGHT * 0.5) # Alignment adjustment
            else:
                label = MathTex(text).scale(0.8)
                # Thin, clean stroke for the track
                track = Line(LEFT * 2, RIGHT * 2, color=GRAY_D, stroke_width=2) 
                
                # Start knobs at random positions
                start_prop = np.random.uniform(0.1, 0.9)
                knob = Dot(track.point_from_proportion(start_prop), color=accent_color, radius=0.08)
                
                label.next_to(track, LEFT, buff=0.5)
                slider_group.add(label, track, knob)
                
            sliders.add(slider_group)
            
        sliders.arrange(DOWN, buff=0.4).next_to(label_nd, DOWN, buff=1)
        self.add_fixed_in_frame_mobjects(sliders)
        
        # Cascade the sliders in
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=UP * 0.2) for s in sliders], 
                lag_ratio=0.15
            ),
            run_time=2
        )
        
        # Animate the values shifting independently to drive the "independent change" thesis
        animations = []
        for slider in sliders:
            if len(slider) > 1: # Skip the \vdots group
                track, knob = slider[1], slider[2]
                new_prop = np.random.uniform(0.1, 0.9)
                animations.append(knob.animate.move_to(track.point_from_proportion(new_prop)))
                
        self.play(*animations, run_time=2.5, rate_func=there_and_back)
        self.wait(2)
