from faustapp.app import app as _faust

sent_messages_topic = _faust.topic("transactions")


@_faust.agent(sent_messages_topic, concurrency=16)
async def sent_messages(messages):
    async for message in messages:
        return f"RECEIVED Sent Message {message}"
