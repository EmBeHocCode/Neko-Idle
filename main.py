"""Entry point for Neko Idle Quest."""

from src.core.game import Game


def main() -> None:
    """Start the game application."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
