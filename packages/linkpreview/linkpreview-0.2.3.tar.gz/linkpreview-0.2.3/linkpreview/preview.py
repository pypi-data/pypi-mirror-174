from os.path import dirname

from bs4 import BeautifulSoup

from .link import Link
from .helpers import LazyAttribute, titleize


class PreviewBase(object):  # pragma: nocover
    """
    Base for all web preview.
    """

    def __init__(self, link: Link, parser: str):
        self.link = link
        self._soup = BeautifulSoup(self.link.content, parser)

    @property
    def title(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError

    @property
    def image(self):
        raise NotImplementedError


class Generic(PreviewBase):
    """
    Extracts title, description, image from a webpage's body
    """

    @property
    def title(self):
        """
        Extract title from the given web page.
        """
        soup = self._soup
        if soup.title and soup.title.text:
            return soup.title.text

        if soup.h1 and soup.h1.text:
            return soup.h1.text

    @property
    def description(self):
        """
        Extract description from the given web page.
        """
        soup = self._soup
        # meta[name='description']
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.has_attr("content"):
            return meta["content"]

        # else extract preview from the first <p> sibling to the first <h1>
        first_h1 = soup.find("h1")
        if first_h1:
            first_p = first_h1.find_next("p")
            if first_p and first_p.string:
                return first_p.text

        # else extract preview from the first <p>
        first_p = soup.find("p")
        if first_p and first_p.string:
            return first_p.string

    @property
    def image(self):
        """
        Extract preview image from the given web page.
        """
        soup = self._soup
        h1 = soup.find("h1")
        if h1:
            # extract the first image which is sibling to the first h1
            img = h1.find_next_sibling("img") or h1.find_next("img")

        else:
            # just find something
            img = soup.find("img")

        if img and img["src"]:
            return img["src"]


class SocialPreviewBase(PreviewBase):
    """
    Abstract class for OpenGraph, TwitterCard and Google+.
    """

    __target_attr__ = None

    def _get_property(self, name):
        meta = self._soup.find("meta", attrs={self.__target_attr__: name})
        if meta and meta["content"]:
            return meta["content"]


class OpenGraph(SocialPreviewBase):
    """
    Gets OpenGraph meta properties of a webpage.
    sample: <meta property="og:title" content="blabla">
    """

    __target_attr__ = "property"

    @property
    def title(self):
        return self._get_property("og:title")

    @property
    def description(self):
        return self._get_property("og:description")

    @property
    def image(self):
        return self._get_property("og:image")


class TwitterCard(SocialPreviewBase):
    """
    Gets TwitterCard meta properties of a webpage.
    sample: <meta name="twitter:title" content="blabla">
    """

    __target_attr__ = "name"

    @property
    def title(self):
        return self._get_property("twitter:title")

    @property
    def description(self):
        return self._get_property("twitter:description")

    @property
    def image(self):
        return self._get_property("twitter:image")


class Schema(SocialPreviewBase):
    """
    Schema.org meta properties
    sample: <meta itemprop="name" content="blabla">
    """

    __target_attr__ = "itemprop"

    @property
    def title(self):
        return self._get_property("name")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def image(self):
        return self._get_property("image")


class LinkPreview:
    def __init__(self, link: Link, parser: str = "html.parser"):
        self.link = link
        self.generic = Generic(link, parser)
        self.opengraph = OpenGraph(link, parser)
        self.twitter = TwitterCard(link, parser)
        self.schema = Schema(link, parser)

    def _find_attribute(self, name):
        for obj in (self.opengraph, self.twitter, self.schema, self.generic):
            value = getattr(obj, name)
            if value:
                return value

    @LazyAttribute
    def title(self):
        return self._find_attribute("title")

    @LazyAttribute
    def description(self):
        return self._find_attribute("description")

    @LazyAttribute
    def image(self):
        return self._find_attribute("image")

    @LazyAttribute
    def absolute_image(self):
        if not self.image:
            return self.image

        # is starts with url scheme
        parts = self.image.split("://")
        if len(parts) > 1 and self.image.startswith(parts[0]):
            return self.image

        link = self.link.copy()

        if self.image.startswith("/"):
            # image is located from root
            link.path = self.image

        elif link.path.endswith("/"):
            # the link is a directory
            link.path = "%s%s" % (link.path, self.image)

        else:
            # the link is a file
            link.path = "%s/%s" % (dirname(link.path), self.image)

        return link.url

    @LazyAttribute
    def force_title(self):
        if self.title:
            return self.title

        if self.link.may_file:
            exploded = self.link.path.split("/")[-1].split(".")
            if len(exploded) > 1:
                return titleize(".".join(exploded[:-1]))

        link = self.link.copy()
        link.netloc = link.netloc.split("@")[-1]
        return link.url[len(self.link.scheme) + 3 :]
