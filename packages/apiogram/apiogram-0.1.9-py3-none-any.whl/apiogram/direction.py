from dataclasses import dataclass

@dataclass
class BotDirection:
    """
    Bot direction
    """
    Inbound: int = 1
    Outgoing: int = 0
