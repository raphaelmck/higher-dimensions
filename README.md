# Higher Dimensions

[![YouTube Video](https://img.shields.io/badge/Watch%20on-YouTube-red?logo=youtube)](https://www.youtube.com/watch?v=Qf3NN38oFxs)

A Manim animation explaining what dimensions actually are — not as places to move, but as independent degrees of freedom needed to describe something.

The video covers:
- Why a photo with 400 pixels is a point in 400-dimensional space
- How "dimension" generalises from physical space to any coordinate system
- Flatland and building intuition for spaces we can't visualise
- Manifolds and lower-dimensional structure embedded in high dimensions
- The geometry of high-dimensional space (dot products, angles, norms)
- The curse of dimensionality
- The manifold hypothesis in machine learning

## Watch

> Click on the link above to watch on YouTube

## Run the animations

```bash
manim -pql src/scenes/s00_intro.py
```

## Project structure

```
src/scenes/   # Manim scene files (one per section)
src/style.py  # Shared style and helpers
media/        # Rendered output (auto-generated, not committed)
```
