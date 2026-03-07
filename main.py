#!/usr/bin/env python3
"""
Portfolio Website Generator
Create beautiful portfolio websites from the command line.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.generator import PortfolioGenerator


def main():
    """Application entry point."""
    try:
        generator = PortfolioGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Portfolio Generator.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue on GitHub.")
        sys.exit(1)


if __name__ == "__main__":
    main()