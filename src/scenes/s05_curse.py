from manim import *
import numpy as np

class HighDimensionalStrangeness(Scene):
    def construct(self):
        # -- STYLING --
        accent_color = TEAL_C
        secondary_color = YELLOW_D
        
        # --- PART 1: THE 2D CHAOS ---
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.2}
        ).scale(0.8)
        
        self.play(FadeIn(plane))
        
        # Generate random arrows to show wild variance in 2D
        arrows = VGroup()
        for _ in range(8):
            angle = np.random.uniform(0, 2 * PI)
            length = np.random.uniform(1.5, 2.5)
            arrow = Arrow(ORIGIN, [length * np.cos(angle), length * np.sin(angle), 0], buff=0, color=secondary_color)
            arrows.add(arrow)
            
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=1.5)
        self.wait(1)
        
        # Highlight two specific arrows and their angle
        v1 = arrows[0]
        v2 = arrows[3]
        angle_arc = Angle(v1, v2, radius=0.6, color=WHITE)
        
        self.play(
            *[FadeOut(a) for a in arrows if a not in [v1, v2]],
            Create(angle_arc)
        )
        self.wait(1)
        
        # --- PART 2: THE MATH FORMULA ---
        self.play(FadeOut(plane, v1, v2, angle_arc))
        
        formula = MathTex(
            r"\cos\theta = \frac{x \cdot y}{\|x\| \|y\|}"
        ).scale(1.5)
        
        self.play(Write(formula))
        self.wait(1)
        self.play(formula.animate.scale(0.6).to_corner(UR))
        
        # --- PART 3: THE DIMENSION SLIDER & HISTOGRAM ---
        # Setup the axes for the cosine distribution (-1 to 1)
        axes = Axes(
            x_range=[-1, 1, 0.5], 
            y_range=[0, 15, 5], 
            x_length=8, 
            y_length=5,
            axis_config={"include_numbers": True}
        ).shift(DOWN * 0.5)
        
        x_label = axes.get_x_axis_label(r"\cos\theta")
        self.play(Create(axes), FadeIn(x_label))
        
        # ValueTracker for dimension n (start at n=3 for a nice broad curve)
        n_tracker = ValueTracker(3)
        
        # Dynamic label for the slider
        n_label = always_redraw(lambda: Text(
            f"Dimension n = {int(n_tracker.get_value())}", 
            font_size=36, color=accent_color
        ).next_to(axes, UP, buff=0.5))
        self.add(n_label)
        
        # The mathematically exact probability curve morphing in real-time
        dist_curve = always_redraw(lambda: axes.plot(
            lambda x: np.sqrt(n_tracker.get_value() / (2 * PI)) * np.exp(-0.5 * n_tracker.get_value() * (x**2)),
            color=accent_color,
            use_smoothing=True
        ))
        
        # Shade the area under the curve
        area = always_redraw(lambda: axes.get_area(dist_curve, color=accent_color, opacity=0.3))
        
        self.play(Create(dist_curve), FadeIn(area))
        self.wait(1)
        
        # Animate the dimension exploding to 1000
        # rate_func=linear is usually best for exponential-feeling slider growth
        self.play(n_tracker.animate.set_value(1000), run_time=5, rate_func=smooth)
        self.wait(1)
        
        # The crucial implication
        implication = MathTex(
            r"\cos\theta \approx 0 \quad\Rightarrow\quad \theta \approx 90^\circ"
        ).scale(1.2).next_to(n_label, UP, buff=0.5)
        
        self.play(Write(implication))
        self.wait(2)
        
        # --- PART 4: APPLICATION (COSINE SIMILARITY) ---
        self.play(FadeOut(axes, x_label, dist_curve, area, n_label, implication, formula))
        
        # Central query vector
        query = Arrow(ORIGIN, UP*2, buff=0, color=WHITE, stroke_width=6)
        query_label = MathTex("q").next_to(query.get_end(), UP)
        
        # Candidate vectors (mostly orthogonal, one aligned)
        candidates = VGroup()
        for i in range(12):
            angle = np.random.uniform(0, 2*PI)
            # Force one candidate to be closely aligned with query
            if i == 5: angle = PI/2 + 0.1 
            
            c = Arrow(ORIGIN, [2*np.cos(angle), 2*np.sin(angle), 0], buff=0, color=GRAY)
            candidates.add(c)
            
        self.play(GrowArrow(query), Write(query_label))
        self.play(LaggedStart(*[GrowArrow(c) for c in candidates], lag_ratio=0.05))
        self.wait(1)
        
        # Highlight the aligned candidate
        best_match = candidates[5]
        highlight_arc = Angle(best_match, query, radius=1, color=accent_color)
        
        self.play(
            best_match.animate.set_color(accent_color).set_stroke(width=6),
            Create(highlight_arc),
            *[c.animate.set_opacity(0.2) for c in candidates if c != best_match]
        )
        
        # Final Thesis
        thesis = Text("Similarity by direction.", weight=BOLD, color=accent_color).to_corner(UL)
        self.play(Write(thesis))
        self.wait(2)
