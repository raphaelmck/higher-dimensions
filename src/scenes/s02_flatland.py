from manim import *
import numpy as np

class FlatlandAnalogy(ThreeDScene):
    def construct(self):
        # -- STYLING & SETUP --
        plane_color = BLUE_E
        sphere_color = TEAL
        intersection_color = YELLOW
        
        # Angle the camera to see both the 3D space and the flat surface
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # --- PART 1: THE FLATLAND PLANE ---
        # A semi-transparent plane representing the 2D world
        plane = Rectangle(width=10, height=10, color=plane_color, fill_opacity=0.3)
        grid = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.2}
        )
        plane_group = VGroup(plane, grid)
        
        self.play(FadeIn(plane_group), run_time=1.5)
        self.wait(1)

        # --- PART 2: THE SPHERE PASSING THROUGH ---
        sphere_radius = 2.0
        sphere = Sphere(radius=sphere_radius, color=sphere_color, fill_opacity=0.15)
        
        # Start the sphere completely above the plane
        start_z = 3.0
        sphere.move_to(OUT * start_z)

        self.play(FadeIn(sphere), run_time=1)

        # The intersection circle on the 2D plane
        intersection = Circle(radius=0.001, color=intersection_color, stroke_width=4)
        intersection.set_opacity(0) # Hide it initially
        intersection.rotate(PI/2, axis=RIGHT) # Align flat with the 3D plane
        
        # Dynamically calculate the cross-section radius
        def update_intersection(circle):
            z_pos = sphere.get_center()[2]
            # r = sqrt(R^2 - z^2)
            if abs(z_pos) < sphere_radius:
                r = np.sqrt(sphere_radius**2 - z_pos**2)
                circle.set_opacity(1)
                # Re-draw the circle at the new radius
                new_circle = Circle(radius=max(r, 0.001), color=intersection_color, stroke_width=4)
                new_circle.rotate(PI/2, axis=RIGHT)
                circle.become(new_circle)
            else:
                circle.set_opacity(0)

        intersection.add_updater(update_intersection)
        self.add(intersection)

        # Animate the sphere moving straight down through the plane
        self.play(
            sphere.animate.move_to(IN * start_z),
            run_time=6,
            rate_func=linear # Linear speed makes the geometric growth/shrink naturally accurate
        )
        
        intersection.clear_updaters()
        self.wait(1)

        # --- PART 3: THESIS TEXT ---
        # Smoothly flatten the camera back to a 2D top-down view
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        self.play(FadeOut(sphere, plane_group, intersection))

        thesis_text = Text(
            "Higher-dimensional objects can be\nstudied through lower-dimensional slices.",
            weight=BOLD
        ).scale(0.8)
        
        self.play(Write(thesis_text), run_time=2)
        self.wait(2)

        # Move text up to make room for the projection
        self.play(thesis_text.animate.to_edge(UP).scale(0.7))

        # --- PART 4: THE TESSERACT PROJECTION ---
        # A clean, minimalist wireframe of a hypercube projection
        outer_cube = Square(side_length=4, color=TEAL, stroke_width=2)
        inner_cube = Square(side_length=2, color=BLUE, stroke_width=2)
        
        # Connect the corresponding vertices
        connecting_lines = VGroup()
        for v1, v2 in zip(outer_cube.get_vertices(), inner_cube.get_vertices()):
            connecting_lines.add(Line(v1, v2, color=GRAY_B, stroke_opacity=0.5))
            
        tesseract = VGroup(outer_cube, inner_cube, connecting_lines)
        tesseract.move_to(DOWN * 0.5)

        label = Text("Projection of a 4D cube into 2D", color=GRAY).scale(0.5).next_to(tesseract, DOWN, buff=0.5)

        self.play(FadeIn(tesseract), Write(label))
        
        # Animate a simple perspective shift to imply 4D rotation without overcomplicating the scene
        self.play(
            inner_cube.animate.scale(1.5),
            outer_cube.animate.scale(0.7),
            run_time=3,
            rate_func=there_and_back
        )
        self.wait(1.5)
