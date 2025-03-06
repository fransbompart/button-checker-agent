import asyncio
from agent.button_checker_agent import ButtonCheckerAgent

async def main():
    agent = ButtonCheckerAgent()
    await agent.check()

if __name__ == '__main__':
    asyncio.run(main())