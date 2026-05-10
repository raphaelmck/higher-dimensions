from manim import *
import numpy as np

class ClosingSynthesis(ThreeDScene):
    def construct(self):
        # -- STYLING --
        primary_color = BLUE_D
        accent_color = TEAL_C
        highlight_color = YELLOW_D
        formula_color = WHITE
        space_color = BLUE_D 
        
        # --- INTRODUCTION: THE SUMMARY POINTS ---
        self.camera.background_color = BLACK # Classic YouTube style

        summary_title = Text("Higher Dimensions Matter for Three Reasons:", weight=BOLD).scale(0.7).to_edge(UP)
        
        reasons = VGroup(
            Tex(r"\textbf{1. Spatially:} reasoning about shapes, slices, and projections."),
            Tex(r"\textbf{2. Mathematically:} a language for many degrees of freedom."),
            Tex(r"\textbf{3. Computationally:} turning data into geometry.")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6).next_to(summary_title, DOWN, buff=0.8)
        
        # Sequentially reveal the three reasons
        self.play(Write(summary_title), run_time=1.5)
        self.play(FadeIn(reasons[0], shift=RIGHT), run_time=1)
        self.play(FadeIn(reasons[1], shift=RIGHT), run_time=1)
        self.play(FadeIn(reasons[2], shift=RIGHT), run_time=1)
        self.wait(2)
        
        # --- THE MONTAGE BEATS ---
        self.play(FadeOut(summary_title), FadeOut(reasons))
        
        # 1. Pixel image → vector
        pixels = VGroup(*[Square(side_length=0.4, fill_opacity=1, fill_color=interpolate_color(BLUE_E, TEAL_E, i/9), stroke_width=0.5) for i in range(9)])
        pixels.arrange_in_grid(3, 3, buff=0)
        
        vector_label = MathTex(r"\in \mathbb{R}^{n}", color=formula_color, font_size=36)
        
        # Center them separately
        pixels.move_to(ORIGIN)
        vector_label.move_to(ORIGIN)

        self.play(FadeIn(pixels, scale=0.5), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(pixels, vector_label), run_time=1)
        self.wait(1)
        self.play(FadeOut(vector_label), run_time=0.5)

        # 2. Sphere slicing plane (Creature's Perspective → 3D Reveal)
        # Re-using logic from Scene 2
        # Setup the plane and sphere (invisible initially)
        plane = Rectangle(width=10, height=8, color=GRAY_B, fill_opacity=0.3)
        grid = NumberPlane(x_range=[-5, 5, 1], y_range=[-4, 4, 1], background_line_style={"stroke_opacity": 0.2})
        plane_group = VGroup(plane, grid)

        sphere_radius = 2.0
        sphere_z = ValueTracker(3.0) # ValueTracker is best for smooth animation
        
        # Define the dynamic intersection circle with an updater
        # This is a key technique for geometric physics sims in Manim
        intersection = Circle(radius=0.001, color=highlight_color, stroke_width=4)
        def update_circle(c):
            z = sphere_z.get_value()
            if abs(z) < sphere_radius:
                r = np.sqrt(sphere_radius**2 - z**2)
                c.set_opacity(1)
                c.become(Circle(radius=max(r, 0.001), color=highlight_color, stroke_width=4))
            else:
                c.set_opacity(0)
        intersection.add_updater(update_circle)
        self.add(intersection)

        # 2D view first (Mystery Reveal)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.play(FadeIn(plane_group), run_time=1)
        
        # Drop unseen sphere through the floor. rate_func=linear is essential for smooth geometric transitions.
        self.play(sphere_z.animate.set_value(-3.0), run_time=4, rate_func=linear)
        self.wait(1)
        
        # Clean the stage
        intersection.clear_updaters()
        self.play(FadeOut(intersection, plane_group), run_time=0.5)


        # 3. Swiss roll manifold
        self.move_camera(phi=65 * DEGREES, theta=-30 * DEGREES, run_time=1)
        
        def create_swiss_roll_mesh(color=BLUE_E, stroke_opacity=0.3):
            mesh = VGroup()
            num_lines = 15
            for i in range(num_lines):
                t = i / (num_lines-1) * 2 * PI
                # Equation: r(t,v) = (t*cos(t), t*sin(t), v)
                line = ParametricFunction(
                    lambda v, t_val=t: np.array([t_val*np.cos(t_val), t_val*np.sin(t_val), v]),
                    t_range=[-2, 2],
                    color=color,
                    stroke_opacity=stroke_opacity,
                    stroke_width=1
                )
                mesh.add(line)
            return mesh

        # Animate the creation of the roll structure
        # LaggedStart gives a beautiful procedural reveal feel
        roll_lines = create_swiss_roll_mesh()
        self.play(LaggedStart(*[Create(l) for l in roll_lines], lag_ratio=0.05), run_time=2)
        self.wait(1)
        
        # Clear stage
        self.play(FadeOut(roll_lines), run_time=0.5)


        # 4. Spacetime Grid (Warping for visual finale)
        # Using tightly packed parametric lines (Scene 7 approach) is best for smoothness
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=1)
        
        dense_grid = VGroup()
        for x in np.arange(-8, 9, 0.5):
            line = ParametricFunction(
                lambda t: np.array([x, t, 0]), 
                t_range=[-8, 8], 
                color=space_color, 
                stroke_opacity=0.5,
                stroke_width=1.5
            )
            dense_grid.add(line)
        for y in np.arange(-8, 9, 0.5):
            line = ParametricFunction(
                lambda t: np.array([t, y, 0]), 
                t_range=[-8, 8], 
                color=space_color, 
                stroke_opacity=0.5,
                stroke_width=1.5
            )
            dense_grid.add(line)
            
        self.play(Create(dense_grid, lag_ratio=0.01), run_time=1.5)
        self.wait(0.5)
        
        # Define the gravity well bending function (Scene 7)
        depth = 2.5
        spread = 0.4
        def gravity_well(p):
            r_sq = p[0]**2 + p[1]**2
            z = -depth * np.exp(-spread * r_sq)
            return np.array([p[0], p[1], z])
            
        self.play(
            dense_grid.animate.apply_function(gravity_well),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(1)
        
        # Clear stage
        self.play(FadeOut(dense_grid), run_time=0.5)
        
        # --- THE CONCLUDING THESIS STATEMENT ---
        # Flatten camera for the final message
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1)
        
        # Dimensions turn information into geometry.
        # Tex allows for bolding (\textbf{}) directly, which is cleaner than multiple Text objects.
        thesis = Tex(r"\textbf{Dimensions turn information into geometry.}").scale(1.2)
        self.play(Write(thesis), run_time=2)
        self.wait(3)
        self.play(FadeOut(thesis), run_time=1)
        
        # --- END CARD ---
        end_card_title = Text("Up Next in the Series:", weight=BOLD, color=highlight_color).scale(0.8).to_edge(UP, buff=1.5)
        
        next_scenes = VGroup(
            Text("The Geometry of Data", weight=BOLD),
            Text("or"),
            Text("Dot Products, Angles, and Similarity", weight=BOLD)
        ).arrange(DOWN, buff=0.5).scale(0.6).next_to(end_card_title, DOWN, buff=1)
        
        self.play(Write(end_card_title))
        self.play(FadeIn(next_scenes[0], shift=RIGHT), run_time=1)
        self.play(FadeIn(next_scenes[1], scale=0.5), run_time=0.5) # Fast reveal for 'or'
        self.play(FadeIn(next_scenes[2], shift=LEFT), run_time=1)
        
        self.wait(4) # Allow YouTube viewers to click end screens
