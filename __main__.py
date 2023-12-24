# main.py
import sys
from src.app import App

def main():
    try:
        app = App()
        app.run()
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
