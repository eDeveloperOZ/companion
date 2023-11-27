# main.py
import sys
from src.bot.bot import run_bot

def main():
    try:
        run_bot()
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
