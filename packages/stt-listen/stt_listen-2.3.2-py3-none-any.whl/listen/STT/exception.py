
class NotAllowedToListenError(Exception):
    def __init__(self, config_path, message=None):
        self.config_path = config_path
        self.message = message or f"System is not allowed to listen. Open `{self.config_path}` and set `stt.is_allowed` to `True`."
        super().__init__(self.message)