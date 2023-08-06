import types
import aiogram
import datetime
from dataclasses import dataclass
from nosql_storage_wrapper.mongo import Storage

callable_types: tuple = types.FunctionType, types.MethodType


class NotExists(Exception):
    """
    Exception for not exists user
    """
    pass


@dataclass
class UserExceptions:
    """
    User exceptions
    """
    NotExists = NotExists


class TelegramUser:
    chat_id: int = None
    username: str = None
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    phone: str = None
    type: str = None
    language_code: str = None
    is_premium: bool = False
    is_bot: bool = False

    email: str = None
    banned: bool = False

    __storage = Storage("users")

    def __init__(self, udata: aiogram.types.Message | dict):
        """
        User constructor
        @param udata:
        """
        if isinstance(udata, aiogram.types.Message):
            udata = getattr(udata, "from", udata)
            for k, v in dict(udata.chat).items():
                if k == "id":
                    self.chat_id = v
                    continue
                setattr(self, k, v)
        else:
            raise Exception("Invalid format data for constructor User()")

    async def find(self) -> bool:
        """
        Find user in storage
        @return: bool
        """
        user = await self.__storage.find_one({"chat_id": self.chat_id})
        if user is None:
            return False
        for k, v in user.items():
            setattr(self, k, v)
        return True

    async def get(self) -> "TelegramUser":
        """
        Find user in storage
        @return: bool
        """
        user = await self.__storage.find_one({"chat_id": self.chat_id})
        if user is None:
            raise UserExceptions.NotExists("User not exists")
        for k, v in user.items():
            setattr(self, k, v)
        return self

    async def create(self) -> object:
        """
        Create new user in storage
        @return:
        """
        props = self.get_props()
        props["create"] = datetime.datetime.now()
        return await self.__storage.insert_one(props)

    async def update(self) -> object:
        """
        Alias for save()
        """
        return await self.save()

    async def save(self) -> object:
        """
        Update user in storage
        TODO: save change log (username, names, etc)
            props.changelog.append({...})
        @return:
        """
        props = self.get_props()
        return await self.__storage.update_one(
            {"chat_id": self.chat_id},
            {"$set": props}
        )

    def get_props(self) -> dict:
        """
        Get user props
        @return: dict
        """
        props = {}
        for k, v in self.__dict__.items():
            if "_" == k[0] or isinstance(v, callable_types):
                continue
            props[k] = v
        return props

    async def __call__(self, *args, **kwargs):
        """
        Call user helper, syntax sugar
        @param args:
        @param kwargs:
        @return:
        """
        user_exists = await self.find()
        if user_exists:
            await self.update()
        else:
            await self.create()

    async def __aenter__(self):
        """
        Async context manager
        """
        return self

    async def __aexit__(self, tp, value, traceback):
        """
        Async context manager
        """
        return await self.update()

