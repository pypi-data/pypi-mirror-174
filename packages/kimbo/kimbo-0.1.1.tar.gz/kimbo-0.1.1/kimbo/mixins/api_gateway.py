__all__ = (
    "ProxyResponseMixin",

    "Request",
    "ProxyEventMixin",
)

from collections import namedtuple


class ProxyResponseMixin:
    def response(
        self,
        body,
        status=None,
        headers=None,
        cookies=None,
        is_base64=None,
    ):
        response = {"body": body}
        if status is not None:
            response["statusCode"] = status
        if headers is not None:
            response["headers"] = headers
        if cookies is not None:
            response["cookies"] = cookies
        if is_base64 is not None:
            response["isBase64Encoded"] = is_base64
        return response


_Request = namedtuple("_Request", (
    "version",
    "headers",
    "body",
    "query",
    "path_parameters",
    "stage_variables",
    "is_base64_encoded",
    "context",
    "http"
))


class Request(_Request):
    __slots__ = ()

    @property
    def parameters(self):
        return self.path_parameters

    @property
    def variables(self):
        return self.stage_variables

    @property
    def is_base64(self):
        return self.is_base64_encoded


_Context = namedtuple("_Context", (

))


class Context(_Context):
    pass


def _build_context(event):
    return Context()


_HTTP = namedtuple("_HTTP", (
    "method",
))


class HTTP(_HTTP):
    pass


def _v1_build_http(event):
    return HTTP(
        method=event["httpMethod"],
    )


def _v2_build_http(event):
    context = event["requestContext"]
    return HTTP(
        method=context["httpMethod"],
    )


def _build_http(event):
    version = event.get("version", "1.0")
    if version == "2.0":
        return _v2_build_http(event)
    if version == "1.0":
        return _v1_build_http(event)
    raise ValueError("coundn't build http")


class ProxyEventMixin:
    @property
    def request(self):
        event = self.raw_event
        return Request(
            event.get("version", "1.0"),
            event["headers"],
            event["body"],
            event["queryStringParameters"],
            event["pathParameters"],
            event["stageVariables"],
            event["isBase64Encoded"],
            _build_context(event),
            _build_http(event),
        )

