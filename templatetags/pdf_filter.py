from django import template
import urllib
import io
import base64

register = template.Library()


@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    """
    if url.startswith("http"):
        image = io.BytesIO(urllib.urlopen(url).read())
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url
