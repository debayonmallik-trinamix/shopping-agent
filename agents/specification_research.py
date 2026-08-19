import sys
import asyncio

from browser_use import Agent, Browser, ChatGoogle
from dotenv import load_dotenv

load_dotenv()


async def main(url, product_name):

    browser = Browser(
        headless=False,
        keep_alive=False
    )

    task = f"""
Visit this product page:

{url}

Research the following product:

{product_name}

Collect the important product specifications.

The product can be ANY type of product.
Do not assume it is a laptop, phone, or any specific category.

Return useful specifications relevant to this particular product.
For example, depending on the product, these may include:
- dimensions
- weight
- material
- capacity
- processor
- RAM
- storage
- display
- battery
- connectivity
- compatibility
- warranty
- other important specifications

Do not invent information.
Only report information you can find on the website.
"""

    agent = Agent(
        task=task,
        browser=browser,
        llm=ChatGoogle(
            model="gemini-3.5-flash-lite"
        )
    )

    result = await agent.run()

    print(result)

    await browser.close()


if __name__ == "__main__":

    url = sys.argv[1]
    product_name = sys.argv[2]

    asyncio.run(main(url, product_name))