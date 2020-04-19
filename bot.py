import os
import logging
from zoidberg.client import Client
from sanic import Sanic
from sanic.response import json

app = Sanic(configure_logging=False)


@app.route("/events", methods=["POST"])
async def events(request):
    # For the initial events payload
    if request.json.get("type") == "url_verification":
        challenge = request.json.get("challenge")
        return json({"challenge": challenge})

    try:
        await bot.handle_event(request.json)
        return json({"message": "Done!"})
    except SlackApiError as e:
        return json({"message": f"Failed due to {e.response['error']}"})


if __name__ == "__main__":
    bot = Client(os.environ.get("BOT_OAUTH_TOKEN"))
    bot.load_plugins(
        ["wttr", "brain", "status", "dadjoke", "utilities", "yourmom", "ping"]
    )

    app.run(host="0.0.0.0", port=3000)
