# json-stream-to-standard-types

Utility function to convert `json-stream` objects to normal Python dicts/lists.

Parallel PR: https://github.com/daggaz/json-stream/pull/17

## Installation

```bash
pip install json-stream-to-standard-types
```

## Usage

To convert a json-stream `dict`-like or `list`-like object and all its
descendants to a standard `list` and `dict`, simply apply the library's
`to_standard_types` function:

```python
import json_stream
from json_stream_to_standard_types import to_standard_types

# JSON: {"round": 1, "results": [1, 2, 3]}
data = json_stream.load(f)
results = data["results"]
print(results)  # prints <TransientStreamingJSONList: TRANSIENT, STREAMING>
converted = to_standard_types(results)
print(converted)  # prints [1, 2, 3]
```

## License

Do whatever you want with it license or whatever it was called
