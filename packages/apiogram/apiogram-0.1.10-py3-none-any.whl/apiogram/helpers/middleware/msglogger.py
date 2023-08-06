import ast
import json
from aiogram import types
from datetime import datetime
from nosql_storage_wrapper.mongo import Storage
from aiogram.dispatcher.middlewares import BaseMiddleware


class MessageLoggerMiddleware(BaseMiddleware):
    """
    Aiogram messages logger middleware
    """

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """
        Log inbound messages
        """
        data = str(dict(message))
        try:
            data = json.loads(data)
        except:
            data = ast.literal_eval(data)

        await Storage("chat_msg_id").insert_one({
            "chat_id": message.chat.id,
            "msg_id": message.message_id,
            # BotDirection.Inbound,
            "dir": 1,
            "datetime": datetime.now(),
        })

        await Storage("chat_log").insert_one({
            "chat_id": message.chat.id,
            "datetime": datetime.now(),
            # BotDirection.Inbound,
            "dir": 1,
            "client": "aiogram",
            "data": data
        })


__all__ = ["MessageLoggerMiddleware"]
