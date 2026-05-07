from manim import *
import numpy as np

class FlatlandAnalogy(ThreeDScene):
    def construct(self):
        # -- SETUP & VARIABLES --
        plane_color = BLUE_E
        sphere_color = TEAL
        intersection_color = YELLOW
        sphere_radius = 2.0
        
        # A ValueTracker controls the Z-position of the sphere for the math to follow
        sphere_z = ValueTracker(3.0)

        # The 2D grid representing Flatland
        grid = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.2}
        )
        
        # --- PART 1: THE CREATURE'S PERSPECTIVE (2D ONLY) ---
        # Look straight down at the XY plane. We do NOT add the sphere yet.
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.play(FadeIn(grid))
        self.wait(1)

        # The intersection circle on the 2D plane
        # It natively lies flat on the XY plane, so no rotations are needed!
        intersection = Circle(radius=0.001, color=intersection_color, stroke_width=4)
        
        def update_circle(c):
            z = sphere_z.get_value()
            # If the sphere is intersecting the plane (z=0)
            if abs(z) < sphere_radius:
                # Math: r = sqrt(R^2 - z^2)
                r = np.sqrt(sphere_radius**2 - z**2)
                c.set_opacity(1)
                c.become(Circle(radius=max(r, 0.001), color=intersection_color, stroke_width=4))
            else:
                c.set_opacity(0) # Hide it if the sphere isn't touching the plane

        intersection.add_updater(update_circle)
        self.add(intersection)

        # "First a point appears. Then a circle grows. Then it shrinks."
        # Animate the unseen sphere moving from z=3 down to z=-3
        self.play(sphere_z.animate.set_value(-3.0), run_time=5, rate_func=linear)
        self.wait(1)


        # --- PART 2: THE 3D REVEAL ---
        # Reset the Z position to the top
        sphere_z.set_value(3.0)
        
        # Move camera to show the 3D reality
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)

        # Now we bring in the actual 3D objects
        plane = Rectangle(width=10, height=10, color=plane_color, fill_opacity=0.3)
        sphere = Sphere(radius=sphere_radius, color=sphere_color, fill_opacity=0.15)
        
        # Bind the sphere's actual position to the ValueTracker
        sphere.add_updater(lambda m: m.move_to(OUT * sphere_z.get_value()))
        
        self.play(FadeIn(plane), FadeIn(sphere))
        self.wait(1)

        # Re-run the exact same mathematical drop, but now we see the cause
        self.play(sphere_z.animate.set_value(-3.0), run_time=5, rate_func=linear)
        self.wait(1)


        # --- PART 3: THE TESSERACT PROJECTION ---
        # Clear the stage
        intersection.clear_updaters()
        sphere.clear_updaters()
        self.play(FadeOut(Group(grid, plane, sphere, intersection)))
        
        # Thesis Text
        thesis_text = Paragraph(
            "Higher-dimensional objects can be",
            "studied through lower-dimensional slices.",
            weight=BOLD, 
            alignment="left"
        ).scale(0.7)
        
        # Attach text to the camera so it ignores the 3D perspective
        self.add_fixed_in_frame_mobjects(thesis_text)
        thesis_text.to_edge(UP)
        self.play(Write(thesis_text))

        # Helper function to generate mathematically perfect 3D wireframe cubes
        def create_wireframe_cube(size, color=WHITE):
            vertices = []
            # Generate the 8 corners
            for x in [-1, 1]:
                for y in [-1, 1]:
                    for z in [-1, 1]:
                        vertices.append(np.array([x, y, z]) * size / 2)
            
            lines = VGroup()
            # Connect the edges where exactly 1 coordinate changes
            for i in range(8):
                for j in range(i + 1, 8):
                    diff = np.abs(vertices[i] - vertices[j])
                    if np.isclose(np.sum(diff), size):
                        lines.add(Line(vertices[i], vertices[j], color=color, stroke_width=2))
            return lines, vertices

        # Use ValueTrackers for the sizes so the connecting lines update flawlessly
        outer_size = ValueTracker(4)
        inner_size = ValueTracker(1.5)
        
        tesseract_group = VGroup()

        def update_tesseract(mob):
            mob.clear() # Redraw every frame for perfect connections
            out_lines, out_v = create_wireframe_cube(outer_size.get_value(), color=TEAL)
            in_lines, in_v = create_wireframe_cube(inner_size.get_value(), color=BLUE)
            
            # Connect corresponding vertices perfectly
            conn_lines = VGroup(*[
                Line(out_v[i], in_v[i], color=GRAY_B, stroke_opacity=0.5, stroke_width=2) 
                for i in range(8)
            ])
            mob.add(out_lines, in_lines, conn_lines)

        tesseract_group.add_updater(update_tesseract)
        
        # Move the tesseract down slightly to balance the text
        tesseract_group.move_to(DOWN * 0.5) 
        self.add(tesseract_group)
        
        # Fade in by animating from a size of 0
        outer_size.set_value(0.01)
        inner_size.set_value(0.01)
        self.play(
            outer_size.animate.set_value(4),
            inner_size.animate.set_value(1.5),
            run_time=1.5
        )
        self.wait(1)

        # "Rotate" the tesseract by inverting the sizes
        self.play(
            outer_size.animate.set_value(1.5),
            inner_size.animate.set_value(4),
            run_time=3,
            rate_func=there_and_back # Smoothly returns to original state
        )
        self.wait(2)
