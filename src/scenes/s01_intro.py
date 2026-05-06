from manim import *
from PIL import Image
import numpy as np

class DimensionHook(Scene):
    def construct(self):
        # 1. Load and process the data using the function from above
        # (Assuming you saved the image as 'charizard.png' in the same folder)
        pixel_array = self.process_image_to_array("charizard.png", target_size=(20, 20))
        
        # 2. Build the pixel grid
        pixel_grid = VGroup()
        square_size = 0.2
        
        for i in range(20):
            for j in range(20):
                val = pixel_array[i, j]
                # Convert the grayscale value (0 to 1) to a hex color
                color = rgb_to_hex((val, val, val))
                
                sq = Square(side_length=square_size)
                # Set stroke width to 0.5 or 1 to give that distinct "grid" look
                sq.set_fill(color, opacity=1).set_stroke(color=GRAY, width=0.5)
                
                # Center the grid based on index
                sq.move_to(RIGHT * (j - 9.5) * square_size + DOWN * (i - 9.5) * square_size)
                pixel_grid.add(sq)

        # -- ANIMATION SEQUENCE --

        # Start with the 20x20 image
        self.play(FadeIn(pixel_grid))
        self.wait(1)

        # "Zoom into pixels"
        self.play(pixel_grid.animate.scale(2.5))
        self.wait(1)

        # "Each pixel value floats out into a long vector"
        # Since 400 squares won't fit horizontally on screen, a great visual trick 
        # is to collapse the grid into a dense line, while fading in the math notation.
        vector_tex = MathTex(r"x = (x_1, x_2, x_3, \dots, x_{400})").scale(1.2).to_edge(DOWN)
        
        self.play(
            # Arrange the squares into a single row, shrink them, and move them up
            pixel_grid.animate.arrange(RIGHT, buff=0.02).scale(0.15).next_to(vector_tex, UP, buff=0.5),
            Write(vector_tex),
            run_time=2
        )
        self.wait(1)

        # "Then replace with x in R^400"
        r400_tex = MathTex(r"x \in \mathbb{R}^{400}").scale(1.5).move_to(vector_tex)
        
        self.play(
            Transform(vector_tex, r400_tex),
            FadeOut(pixel_grid, shift=UP) # The visual pixels vanish into the abstract math
        )
        self.wait(1.5)

        # "Smash-cut to a real image"
        real_image_tex = MathTex(r"x \in \mathbb{R}^{12{,}000{,}000}").scale(1.5).move_to(vector_tex)
        self.play(
            Transform(vector_tex, real_image_tex),
            run_time=0.5 # Fast transition for the smash-cut feel
        )
        self.wait(1.5)

        # On-screen thesis
        thesis = Text("Dimension = number of independent values", weight=BOLD).scale(0.9).to_edge(UP)
        self.play(FadeIn(thesis, shift=DOWN))
        self.wait(2)


    def process_image_to_array(self, image_path, target_size=(20, 20)):
        img = Image.open(image_path).convert("RGBA")
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        solid_img = Image.alpha_composite(background, img)
        gray_img = solid_img.convert("L")
        small_img = gray_img.resize(target_size, Image.NEAREST)
        return np.array(small_img) / 255.0
