# PiStatsServer
This tool is a lightweight HTTP server that wraps Broadcom's `vcgencmd` and its respective Python bindings that expose various readout endpoints that can be used to remotely measure temperature, clock speed and throttling state of a Raspberry PI.

## Endpoints
| Endpoint | Description | Call |
|----------|-------------|------|
| `/temp` | Measures CPU temperature | `vcgm.measure_temp()` |
| `/voltage` | Measures core voltage | `vcgm.measure_volts("core")` |
| `/throttled` | Checks throttling status | `vcgm.get_throttled()` |

Any other endpoint emits a 404.

## Running
Pull the repo and install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already, then sync dependencies.
```
uv sync
```
Start the server by invoking python:
```
uv run server.py
```
The script supports `--host` and `--port` for setting the host address and port to serve on respectively. Set host to `0.0.0.0` to serve externally. Example usage:
```
uv run server.py --host 0.0.0.0 --port 8912
```
Tested on Raspberry Pi5
