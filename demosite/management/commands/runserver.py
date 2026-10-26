"""ASGI ``runserver`` that serves the project via uvicorn (replaces daphne's)."""

import os
import sys

import uvicorn
from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand,
)
from django.db import connections
from django.utils import autoreload
from django.utils.module_loading import import_string

# Same limit daphne enforced (1 MiB per incoming WebSocket message).
WS_MAX_SIZE = 1024 * 1024


class Command(StaticfilesRunserverCommand):
    """Development server running ``ASGI_APPLICATION`` under uvicorn.

    Keeps Django's ``runserver`` interface (``addrport``, ``--noreload``,
    ``--ipv6``, ``--nostatic``, ``--insecure``) and Django's autoreloader.
    Under ``DEBUG`` (or ``--insecure``) static files are served through
    ``ASGIStaticFilesHandler``. Tetra's ``runserver`` (listed before this app
    in ``INSTALLED_APPS``) runs the Tetra build and then chains to this one.
    """

    help = "Starts the ASGI development server (uvicorn), serving static files."

    def get_handler(self, *args, **options):
        """Return ``ASGI_APPLICATION``, wrapped in the static files handler if needed."""
        app = import_string(settings.ASGI_APPLICATION)
        if options["use_static_handler"] and (
            settings.DEBUG or options["insecure_serving"]
        ):
            return ASGIStaticFilesHandler(app)
        return app

    def inner_run(self, *args, **options):
        """Run checks, then serve the ASGI app with uvicorn (no uvicorn reloader)."""
        autoreload.raise_last_exception()
        if not options["skip_checks"]:
            self.stdout.write("Performing system checks...\n\n")
            self.check(display_num_errors=True)
        self.check_migrations()
        for conn in connections.all(initialized_only=True):
            conn.close()

        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"
        host = "0.0.0.0" if self.addr == "0" else self.addr
        addr = f"[{host}]" if self._raw_ipv6 else host
        self.stdout.write(
            f"Django version {self.get_version()}, using settings "
            f"{settings.SETTINGS_MODULE!r}\n"
            f"Starting ASGI/uvicorn development server at "
            f"{self.protocol}://{addr}:{self.port}/\n"
            f"Quit the server with {quit_command}."
        )
        config = uvicorn.Config(
            self.get_handler(*args, **options),
            host=host,
            port=int(self.port),
            lifespan="off",
            ws_max_size=WS_MAX_SIZE,
        )
        try:
            uvicorn.Server(config).run()
        except SystemExit as e:
            # uvicorn exits on bind errors; sys.exit doesn't work in the reloader thread.
            os._exit(e.code or 1)
        except KeyboardInterrupt:
            sys.exit(0)
