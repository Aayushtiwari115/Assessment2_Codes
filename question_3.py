#question_3_Solution
from turtle import Screen, Turtle
from math import cos, sin, radians
from typing import Tuple

# Draw one edge of the polygon recursively using the Koch-like triangle rule
def draw_edge(t: Turtle, length: float, depth: int) -> None:
    if depth == 0:
        # Base case: at depth 0, draw a straight line
        t.forward(length)
        return

    # Recursive step: divide the edge into 4 segments with triangle indentation
    L = length / 3.0
    d = depth - 1
    # Sequence represents forward and turn operations for the edge
    seq = [("F", L), ("L", 60), ("F", L), ("R", 120), ("F", L), ("L", 60), ("F", L)]

    for op, val in seq:
        if op == "F":
            # Recursively draw the forward segment
            draw_edge(t, val, d)
        elif op == "L":
            # Turn left by specified angle
            t.left(val)
        elif op == "R":
            # Turn right by specified angle
            t.right(val)

# Draw the full polygon by connecting multiple recursive edges
def draw_polygon_fractal(t: Turtle, sides: int, side_length: float, depth: int) -> None:
    if sides < 3:
        raise ValueError("Number of sides must be ≥ 3.")  # Ensure polygon validity
    exterior_angle = 360.0 / sides  # Calculate exterior angle of polygon
    for _ in range(sides):
        draw_edge(t, side_length, depth)  # Draw one recursive edge
        t.left(exterior_angle)            # Turn to next edge

# Simulate the turtle's path to estimate bounding box for centering
def simulate_path_bbox(sides: int, side_length: float, depth: int) -> Tuple[float, float, float, float]:
    x = y = heading = 0.0
    min_x = max_x = x
    min_y = max_y = y

    # Move forward in simulation without drawing
    def forward_sim(len_):
        nonlocal x, y, min_x, max_x, min_y, max_y
        rad = radians(heading)
        x += len_ * cos(rad)
        y += len_ * sin(rad)
        # Update bounding box coordinates
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

    # Simulate turning left or right
    def turn_sim(kind: str, angle: float):
        nonlocal heading
        heading += angle if kind == "left" else -angle

    # Simulate recursive edge drawing
    def draw_edge_sim(length: float, d: int):
        if d == 0:
            forward_sim(length)
            return
        L = length / 3.0
        seq = [("F", L), ("L", 60), ("F", L), ("R", 120), ("F", L), ("L", 60), ("F", L)]
        for op, val in seq:
            if op == "F":
                draw_edge_sim(val, d - 1)
            elif op == "L":
                turn_sim("left", val)
            elif op == "R":
                turn_sim("right", val)

    # Simulate drawing entire polygon
    exterior = 360.0 / sides
    for _ in range(sides):
        draw_edge_sim(side_length, depth)
        turn_sim("left", exterior)

    return min_x, min_y, max_x, max_y  # Return bounding box

# Helper function to safely ask for integer input
def ask_int(prompt: str, min_value: int = 1) -> int:
    while True:
        try:
            v = int(input(f"{prompt}: ").strip())
            if v < min_value:
                print(f"Enter integer ≥ {min_value}.")
                continue
            return v
        except ValueError:
            print("Enter a valid integer.")

# Helper function to safely ask for float input
def ask_float(prompt: str, min_value: float = 0.1) -> float:
    while True:
        try:
            v = float(input(f"{prompt}: ").strip())
            if v < min_value:
                print(f"Enter number ≥ {min_value}.")
                continue
            return v
        except ValueError:
            print("Enter a valid number.")

# Main execution function
def main() -> None:
    print("=== Recursive Polygon with Triangle Indentation ===")
    sides = ask_int("Enter number of sides", 3)
    length = ask_float("Enter side length (pixels)", 1.0)
    depth = ask_int("Enter recursion depth", 0)

    if depth > 6:
        print("Note: Depth > 6 may render slowly.")  # Warn about performance

    screen = Screen()
    screen.title("Recursive Triangle Indentation")
    screen.setup(width=1100, height=800)
    screen.bgcolor("white")
    screen.tracer(False)  # Disable animation for faster drawing

    t = Turtle(visible=True)
    t.hideturtle()
    t.speed(0)
    t.pensize(2)
    t.color("#333333")

    # Center the drawing based on simulated bounding box
    min_x, min_y, max_x, max_y = simulate_path_bbox(sides, length, depth)
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    t.penup()
    t.goto(-cx, -cy)
    t.setheading(0.0)
    t.pendown()

    draw_polygon_fractal(t, sides, length, depth)  # Draw the fractal polygon
    screen.update()
    print("Drawing complete. Close the window to exit.")
    screen.mainloop()

if __name__ == "__main__":
    main()
