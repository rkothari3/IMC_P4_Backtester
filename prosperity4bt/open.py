import socket
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

_LOCAL_VIS_PORT = 5173
_DEPLOYED_VIS_URL = "https://jmerle.github.io/imc-prosperity-4-visualizer"


def _get_visualizer_base_url() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        try:
            s.connect(("localhost", _LOCAL_VIS_PORT))
            return f"http://localhost:{_LOCAL_VIS_PORT}"
        except OSError:
            return _DEPLOYED_VIS_URL


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.server.shutdown_flag = True
        return super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        return super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        return


class CustomHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shutdown_flag = False


def open_visualizer(output_file: Path) -> None:
    http_handler = partial(HTTPRequestHandler, directory=str(output_file.parent))
    http_server = CustomHTTPServer(("localhost", 0), http_handler)

    vis_base = _get_visualizer_base_url()
    webbrowser.open(
        f"{vis_base}/?open=http://localhost:{http_server.server_port}/{output_file.name}"
    )

    while not http_server.shutdown_flag:
        http_server.handle_request()
