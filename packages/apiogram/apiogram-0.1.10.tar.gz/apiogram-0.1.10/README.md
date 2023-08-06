# Apiogram
Simple wrapper for aiogram - little framework for comfortable develop telegram bots

[![PyPi Package Version](https://img.shields.io/pypi/v/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/apiogram)
[![PyPi status](https://img.shields.io/pypi/status/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/apiogram)
[![Supported python versions](https://img.shields.io/badge/Python-3.10.8,3.11-blue)](https://pypi.python.org/pypi/apiogram)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-6.2-blue.svg?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api)
[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)

```py
import logging
from magic_config import Config
from apiogram import start_polling


def main():
    """Main function"""
    # Logging module configuration
    logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)
    # Dafult configuration get from Config object
    start_polling()


if __name__ == "__main__":
    """Run main function"""
    main()
```