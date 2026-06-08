from urllib.parse import urlencode
from urllib.request import urlopen


class TelegramNotifier:
    def __init__(self, bot_token: str | None, chat_id: str | None):
        self.bot_token = bot_token
        self.chat_id = chat_id

    @property
    def enabled(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    async def send_message(self, message: str) -> bool:
        if not self.enabled:
            return False

        query = urlencode({"chat_id": self.chat_id, "text": message})
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?{query}"
        with urlopen(url, timeout=10):
            pass
        return True
