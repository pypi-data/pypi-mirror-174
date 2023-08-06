__all__ = (
    "SQSMixin",
)


class SQSMixin:
    successful = True
    success = True
    failed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__factory = self.handler_kwargs.get("sqs__record_factory", lambda x: x)

    def perform_record(self, message):
        pass

    def prepare_message(self, record):
        return self.__factory(record)

    def perform(self):
        self.records = self.raw_event["Records"]

        failures = []
        for record in self.records:
            message = self.prepare_message(record)
 
            successful = self.perform_record(message)
            if not successful:
                failures.append({"itemIdentifier": record["messageId"]})

        return {
            "batchItemFailures": failures,
        }

