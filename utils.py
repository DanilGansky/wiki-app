from io import BytesIO

import markdown
from django.core.files.images import ImageFile
from django.db.models.fields.files import ImageFieldFile
from PIL import Image


def compress_image(image: ImageFieldFile,
                   size=None, quality=70) -> ImageFile:
    """
    Compress the image to the specified quality.
    Resize the image to the specified size.
    """

    img = Image.open(image)
    img = img.convert('RGB')

    if size:
        img = img.resize(size)

    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=quality)
    return ImageFile(img_io, name=image.name)


def get_upload_path(instance, filename):
    return instance.get_upload_path(filename)


def get_html_from_markdown(source):
    return markdown.markdown(source,
                             extensions=['pymdownx.tasklist',
                                         'pymdownx.emoji',
                                         'pymdownx.mark',
                                         'pymdownx.smartsymbols',
                                         'pymdownx.superfences',
                                         'tables', 'footnotes'])
