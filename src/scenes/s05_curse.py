from manim import *
import numpy as np

class The90DegreeMachine(Scene):
    def construct(self):
        # -- STYLING --
        accent_color = TEAL_C
        reference_color = BLUE_D
        highlight_color = YELLOW_D
        dot_color = WHITE
        
        # --- BEAT 1: 2D INTUITION ---
        # "If I pick two random directions, what angle should I expect?"
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.2}
        ).scale(0.8)
        
        # Fixed Reference Vector (pointing straight right)
        ref_arrow = Arrow(ORIGIN, RIGHT * 2.5, buff=0, color=reference_color, stroke_width=6)
        ref_label = MathTex("v_{ref}").next_to(ref_arrow.get_end(), DOWN)
        
        self.play(FadeIn(plane), GrowArrow(ref_arrow), FadeIn(ref_label))
        self.wait(0.5)
        
        # Generate random arrows and angle arcs
        random_arrows = VGroup()
        angle_arcs = VGroup()
        angle_labels = VGroup()
        
        # 4 distinct 2D examples
        angles = [PI/6, 2*PI/3, -PI/4, 5*PI/6] 
        for angle in angles:
            arrow = Arrow(ORIGIN, [2.5*np.cos(angle), 2.5*np.sin(angle), 0], buff=0, color=accent_color)
            arc = Angle(ref_arrow, arrow, radius=0.8, color=highlight_color)
            deg_val = int(abs(angle * 180 / PI))
            label = Text(f"{deg_val}°", font_size=20, color=highlight_color).next_to(arc, direction=UP if angle>0 else DOWN, buff=0.1)
            
            random_arrows.add(arrow)
            angle_arcs.add(arc)
            angle_labels.add(label)
            
        # Flash them one by one to show the "wild variance"
        for i in range(4):
            self.play(GrowArrow(random_arrows[i]), Create(angle_arcs[i]), FadeIn(angle_labels[i]), run_time=0.8)
            self.wait(0.2)
            if i < 3: # Keep the last one for the transition
                self.play(FadeOut(random_arrows[i], angle_arcs[i], angle_labels[i]), run_time=0.3)
                
        self.wait(1)
        
        # --- BEAT 2: THE ANGLE GAUGE ---
        self.play(FadeOut(plane, random_arrows[-1], angle_arcs[-1], angle_labels[-1], ref_arrow, ref_label))
        
        # Build the semicircular gauge
        gauge_radius = 3.5
        gauge_arc = Arc(radius=gauge_radius, start_angle=0, angle=PI, color=GRAY_B, stroke_width=4)
        gauge_center = DOWN * 1.5
        gauge_arc.move_to(gauge_center + UP * gauge_radius/2) # align properly
        
        ticks = VGroup()
        tick_labels = VGroup()
        for deg in [0, 45, 90, 135, 180]:
            rad = deg * PI / 180
            # Calculate tick positions
            start = gauge_center + np.array([np.cos(rad), np.sin(rad), 0]) * (gauge_radius - 0.2)
            end = gauge_center + np.array([np.cos(rad), np.sin(rad), 0]) * (gauge_radius + 0.2)
            ticks.add(Line(start, end, color=WHITE))
            
            # Add text labels
            label = Text(f"{deg}°", font_size=24)
            label_pos = gauge_center + np.array([np.cos(rad), np.sin(rad), 0]) * (gauge_radius + 0.6)
            label.move_to(label_pos)
            tick_labels.add(label)
            
        # Highlight the 90 degree mark to subconsciously prime the viewer
        ticks[2].set_color(highlight_color).set_stroke(width=6)
        tick_labels[2].set_color(highlight_color).set_weight(BOLD)
        
        gauge = VGroup(gauge_arc, ticks, tick_labels)
        self.play(Create(gauge), run_time=1.5)
        
        # --- BEAT 3: THE DIMENSION SLIDER & COLLAPSE ---
        n_tracker = ValueTracker(2)
        
        slider_label = always_redraw(lambda: Text(
            f"Dimension n = {int(n_tracker.get_value())}", 
            font_size=36, color=accent_color
        ).to_corner(UL))
        
        self.play(FadeIn(slider_label))
        
        # Generate 40 samples using statistical Z-scores for smooth animation
        num_samples = 40
        # Z-scores from a standard normal distribution
        z_scores = np.random.normal(0, 1.2, num_samples) 
        
        dots = VGroup()
        for z in z_scores:
            dot = Dot(color=dot_color, radius=0.06)
            # Clip z-scores so they don't break the arccos math at n=2
            safe_z = np.clip(z, -1.3, 1.3)
            
            # Updater: cos(theta) approaches 0 with std dev 1/sqrt(n)
            dot.add_updater(lambda d, z_val=safe_z: d.move_to(
                gauge_center + np.array([
                    np.cos(np.arccos(np.clip(z_val / np.sqrt(n_tracker.get_value()), -1, 1))),
                    np.sin(np.arccos(np.clip(z_val / np.sqrt(n_tracker.get_value()), -1, 1))),
                    0
                ]) * gauge_radius
            ))
            dots.add(dot)
            
        # Cascade the dots in at n=2 (broad spread)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), run_time=2)
        self.wait(1)
        
        # THE REVEAL: Slide n to 1000. 
        # The updaters will pull all dots smoothly toward 90 degrees.
        self.play(n_tracker.animate.set_value(1000), run_time=4.5, rate_func=smooth)
        self.wait(1)
        
        # --- BEAT 4: FORMALIZE ---
        dots.clear_updaters() # Lock them in place
        
        formula = MathTex(r"\cos\theta = \frac{x \cdot y}{\|x\| \|y\|} \approx 0").scale(1.2)
        formula.next_to(gauge, DOWN, buff=1)
        
        self.play(Write(formula))
        self.wait(2)
        
        # --- BEAT 5: SIGNAL VS NOISE PAYOFF ---
        self.play(FadeOut(gauge, dots, formula, slider_label))
        
        # Bring back the reference vector
        self.play(GrowArrow(ref_arrow), FadeIn(ref_label))
        
        # Draw the "Noise" (almost perpendicular)
        noise_arrows = VGroup()
        for _ in range(15):
            # Angles very close to 90 or 270 degrees
            angle = np.random.choice([PI/2, -PI/2]) + np.random.uniform(-0.1, 0.1)
            arrow = Arrow(ORIGIN, [2*np.cos(angle), 2*np.sin(angle), 0], buff=0, color=GRAY_C, stroke_width=2)
            noise_arrows.add(arrow)
            
        self.play(LaggedStart(*[GrowArrow(a) for a in noise_arrows], lag_ratio=0.05), run_time=1.5)
        
        # Draw the "Signal" (meaningful alignment)
        signal_arrows = VGroup()
        for angle in [0.2, -0.15]:
            arrow = Arrow(ORIGIN, [2.5*np.cos(angle), 2.5*np.sin(angle), 0], buff=0, color=highlight_color, stroke_width=6)
            signal_arrows.add(arrow)
            
        self.play(LaggedStart(*[GrowArrow(a) for a in signal_arrows], lag_ratio=0.2))
        
        # Add the thesis text
        thesis = Text("Genuine alignment stands out.", weight=BOLD, color=highlight_color).to_corner(UL)
        self.play(Write(thesis))
        
        self.wait(3)
