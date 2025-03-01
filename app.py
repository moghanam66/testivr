from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

import asyncio

# Define the bot settings
settings = BotFrameworkAdapterSettings(app_id="b0a29017-ea3f-4697-aef7-0cb05979d16c", app_password="2fc8Q~YUZMbD8E7hEb4.vQoDFortq3Tvt~CLCcEQ")  # Add your credentials if needed
adapter = BotFrameworkAdapter(settings)


class SimpleBot:
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == "message":
            await turn_context.send_activity(f"You said: {turn_context.activity.text}")

# Bot logic handler
async def bot_logic(turn_context: TurnContext):
    bot = SimpleBot()
    await bot.on_turn(turn_context)

@app.post("/api/messages")
async def messages(request: Request):
    body = await request.json()
    activity = Activity().deserialize(body)

    async def turn_call(turn_context):
        await bot_logic(turn_context)

    response = await adapter.process_activity(activity, "", turn_call)
    if response:
        return response
    else:
        raise HTTPException(status_code=500, detail="Bot processing error")
