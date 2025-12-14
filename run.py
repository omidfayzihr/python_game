#!/usr/bin/env python3
# Game launcher - starts the adventure game
import sys

if __name__ == "__main__":
    try:
        import game
    except ImportError as e:
        print(f"Error: Could not import game module: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
