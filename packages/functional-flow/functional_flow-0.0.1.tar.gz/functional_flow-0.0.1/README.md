# Functional Flow

This is a small library providing the compose and flow functions as inspired by James Sinclair's blog [post](https://jrsinclair.com/articles/2022/javascript-function-composition-whats-the-big-deal).

## Installation
***
```bash
pip install functional-flow
```

## Usage
***

```python
from functional_flow import compose, flow

f = lambda x: x + 1
g = lambda x: x * 3

dynamic_compose = compose(
    f,
    g
)
compose_result = dynamic_compose(3)

dynamic_flow = flow(
    f,
    g
)
flow_result = dynamic_flow(3)

print(compose_result)
print(flow_result)
```