__all__ = (
    "Handler",

    "mixins",
)

from . import mixins


class Handler:
    def __init__(self):
        self.init()

    def __init_subclass__(cls, **kwargs):
        cls.handler_kwargs = kwargs

    def init(self) -> None:
        pass

    def __call__(self, event, context):
        self.raw_event = event
        self.raw_context = context

        result = None
        try:
            result = self.run()
        except Exception as error:
            result = self.error(error)
        finally:
            del self.raw_event, self.raw_context
        return result

    def run(self):
        self.setup()

        result = None
        try:
            result = self.perform()
        finally:
            self.teardown(result)
        return result

    def error(self, exception: Exception):
        raise exception from None

    def setup(self):
        pass

    def perform(self):
        pass

    def teardown(self, result):
        pass
