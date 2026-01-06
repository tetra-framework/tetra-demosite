import io

from django.http import FileResponse

from tetra import Component, public


class DownloadButton(Component):

    filename: str = "foo.txt"

    def load(self, filename: str = "foo.txt", *args, **kwargs):
        self.filename = filename

    @public
    def download_file(self):
        return FileResponse(
            io.BytesIO(b"Hello, World!"),
            content_type="text/plain",
            filename=self.filename,
            as_attachment=True,
        )
