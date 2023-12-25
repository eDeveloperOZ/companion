import sys
import asyncio
from src.app import App

async def main():
    try:
        app = App()
        await app.run()
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
