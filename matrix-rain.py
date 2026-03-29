#!/usr/bin/env python3
"""
Animated terminal number grid with dynamic randomization.
"""

__author__ = "q1lra"
__version__ = "1.0.0"

import sys
import tty
import termios
import select
import random
import time
from rich.console import Console

console = Console()


def generate_grid(width: int, height: int):
    return [[random.randint(0, 9) for _ in range(width)] for _ in range(height)]


def random_color():
    x = random.random()
    if x < 0.02:
        return "1;97"   # bright white
    elif x < 0.1:
        return "1;92"   # bright green
    elif x < 0.3:
        return "2;32"   # dim green
    return "0;92"       # normal green


def draw(grid):
    sys.stdout.write("\033[H\n")  # move cursor to top

    for i, row in enumerate(grid):
        line = "  " + "".join(
            f"\033[{random_color()}m{n}\033[0m "
            for n in row
        )
        sys.stdout.write(line + ("\n" if i < len(grid) - 1 else ""))


def update_grid(grid, width, height):
    updates = (width * height) // 12
    for _ in range(updates):
        r = random.randrange(height)
        c = random.randrange(width)
        grid[r][c] = random.randint(0, 9)


def rain(speed: float = 0.08):
    width = max((console.size.width - 4) // 2, 1)
    height = max(console.size.height - 2, 1)

    grid = generate_grid(width, height)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        console.clear()
        sys.stdout.write("\033[?25l")  # hide cursor

        while True:
            # Exit on ENTER
            if select.select([sys.stdin], [], [], 0)[0]:
                if sys.stdin.read(1) == "\n":
                    break

            update_grid(grid, width, height)
            draw(grid)

            sys.stdout.flush()
            time.sleep(speed)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h")  # show cursor
        console.clear()


def main():
    speed = 0.08

    if len(sys.argv) > 1:
        try:
            speed = float(sys.argv[1])
        except ValueError:
            console.print("[red]Invalid speed value, using default.[/red]")

    rain(speed)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception:
        console.print_exception(max_frames=20)
        
