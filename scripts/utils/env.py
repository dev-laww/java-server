import dotenv

dotenv.load_dotenv()


class Environment:
    __values = dotenv.dotenv_values()

    @staticmethod
    def get(key: str, default=None):
        """Get an environment variable."""
        return Environment.__values.get(key, default)

    @staticmethod
    def set(key: str, value: str):
        """Set an environment variable."""
        dotenv.set_key(dotenv.find_dotenv(), key, value)
