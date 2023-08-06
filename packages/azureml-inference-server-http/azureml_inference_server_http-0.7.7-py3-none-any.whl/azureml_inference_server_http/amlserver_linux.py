import os
import sys

import gunicorn.app.wsgiapp

from .constants import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_WORKER_COUNT,
    DEFAULT_WORKER_PRELOAD,
    DEFAULT_WORKER_TIMEOUT_SECONDS,
    ENV_WORKER_PRELOAD,
    ENV_WORKER_TIMEOUT,
)


def run(host, port, worker_count):
    #
    # Manipulate the sys.argv to apply settings to gunicorn.app.wsgiapp.
    #
    # Not all gunicorn settings can be applied using environment variables and
    # command arguments have higher authoritative than other settings.
    #
    # Configuration authoritative:
    #   https://docs.gunicorn.org/en/stable/configure.html#configuration-overview
    #
    sys.argv = [
        sys.argv[0],
        "-b",
        f"{host}:{port}",
        "-w",
        str(worker_count),
        "--log-config",
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "logging.conf"),
        "--timeout",
        os.environ.get(ENV_WORKER_TIMEOUT, DEFAULT_WORKER_TIMEOUT_SECONDS),
    ]

    if os.environ.get(ENV_WORKER_PRELOAD, DEFAULT_WORKER_PRELOAD).lower() == "true":
        sys.argv.append("--preload")

    sys.argv.append("azureml_inference_server_http.server.entry:app")

    gunicorn.app.wsgiapp.WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()


if __name__ == "__main__":
    run(DEFAULT_HOST, DEFAULT_PORT, DEFAULT_WORKER_COUNT)
