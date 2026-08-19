import asyncio
import sys
import json

from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatGoogle
from pydantic import BaseModel
from typing import List, Optional


load_dotenv(override=True)


# -------------------------
# 1. Product schema
# -------------------------

class Product(BaseModel):
    name: str
    price: Optional[float] = None
    rating: Optional[float] = None
    specifications: str
    url: Optional[str] = None
    source: str


class ProductDiscoveryResult(BaseModel):
    products: List[Product]


# -------------------------
# 2. Browser agent
# -------------------------

async def main(url,task):

    browser = Browser(
        headless=False
    )
    
    browser_task = f"""
    Visit this website:

    {url}

    {task}

    Find candidate products that match the user's requirement.
    Return the requested product information in the required structured format.
    """
    try:

        agent = Agent(
            task=browser_task,
            llm=ChatGoogle(
                model="gemini-3.5-flash-lite"
            ),
            browser=browser,
            output_model_schema=ProductDiscoveryResult,
        )

        history = await agent.run()

        # Structured Pydantic result(object)
        structured_result = history.structured_output

        

        if structured_result:
            # Convert the structured result to a dictionary and then 
            dic=structured_result.model_dump()
            # to JSON
            json_data=json.dumps(dic, indent=2, ensure_ascii=False)
            print(json_data)
                
        else:
            print(
                json.dumps(
                    {
                        "products": []
                    }
                )
            )

    

    finally:

        await browser.close()


# -------------------------
# 3. Entry point
# -------------------------

if __name__ == "__main__":

    url = sys.argv[1]
    task=sys.argv[2]

    asyncio.run(main(url,task))
    