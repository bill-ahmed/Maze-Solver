# Maze Solver
An implementation of Dijkstra's algorithm to solve a given maze.

## Pre-conditions
1. The maze must use the PPM file format (and contain only black/white colour values)
2. The start of the maze must be at pixel (0,0) and end at (X, Y), where X & Y are the dimensions of the image


## Running the Program
This script requires Python 3. To install dependencies: `pip install requirements.txt` in the root directory.

To execute: `python MazeSolver.py`. When prompted, enter the path to the PPM file (for example: `images/maze.ppm`). 

Results will be saved in the "output" folder, and there are two sample images in the "images" folder included.

Note: Some images can take several seconds to process.


## Info
This was created as part of the second-year "Design and Analysis of Data Structures" course at the University of Toronto.