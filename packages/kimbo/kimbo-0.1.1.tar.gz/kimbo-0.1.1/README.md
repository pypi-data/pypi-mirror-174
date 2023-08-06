# kimbo
A Python micro framework for AWS lambda inspired by mixin design pattern.

## Installation
**Python 3.6 or higher is required.**
```
python3 -m pip install -U kimbo
```

## Example
```python
import kimbo
import kimbo.mixins.api_gateway


class HelloWorld(
  kimbo.mixins.api_gateway.ProxyResponseMixin,
  kimbo.Handler,
):
  def init(self):
    self.message = "Hello, world!"

  def perform(self):
    return self.response(self.message)


lambda_handler = HelloWorld()
```

