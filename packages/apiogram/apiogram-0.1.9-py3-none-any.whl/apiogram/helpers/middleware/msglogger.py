from aiogram import types
import ast
import json
from datetime import datetime
from nosql_storage_wrapper.mongo import Storage
from aiogram.dispatcher.middlewares import BaseMiddleware
from apiogram import log_sending_message_id, BotDirection


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

        await log_sending_message_id(message, BotDirection.Inbound)

        await Storage("chat_log").insert_one({
            "chat_id": message.chat.id,
            "datetime": datetime.now(),
            "dir": BotDirection.Inbound,
            "client": "aiogram",
            "data": data
        })


__all__ = ["MessageLoggerMiddleware"]
