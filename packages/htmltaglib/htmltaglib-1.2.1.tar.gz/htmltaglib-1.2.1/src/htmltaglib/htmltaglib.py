"""
HTMLTagLib by Micah Hanevich / Swordsman300

This Module / Library is designed to be an easy-to-implement HTML Element source for Bottle (and other) projects.
HTML Element Definitions and Documentation pulled from W3Schools' HTML Reference.
Intended for use with HTML5 and a Python Bottle Framework.
"""

from enum import Enum
from datetime import datetime


# CUSTOM ENUM SETUP
class CustomEnum(Enum):
    def __str__(self):
        return '{0}'.format(self.value)


# ELEMENTS

class Element:
    """ Represents an HTML element. Used to make dynamic page
    generation in-code easily applicable to a ``bottle`` webpage.
    Used as the base class for more advanced objects of this type.

    :param tag: Type of HTML Element.
    :param attr: Dictionary of attribute choices for the Element. (default: None)
    :param html: Overrides generated html str (default: None)
    :param end_tag: Whether to generate a terminating tag. Ex: </div> (default: True) """

    _attributes: dict

    # Initialize Class
    def __init__(self, tag: str, attr: dict = None, html: str = None, end_tag: bool = True):

        # HTML Element Type
        self.tag = tag

        # Raw HTML Text
        self._html = html

        # HTML Child Elements (accessible
        #  through indexing the object)
        self._items = []

        # List of HTML Attributes (accessible
        #  through python as attributes)
        self._attributes = attr

        # Determines if the closing tag (</tag>)
        #  is included or not
        self.end_tag = end_tag

        # If initialized as not bool, set to False
        if type(end_tag) is not bool:
            self.end_tag = False

        # If initialized blank, set to empty dict
        if attr is None:
            self._attributes = {}

        # If initialized blank, generate html based
        #  on _attributes and tag
        if html is None:
            self._gen_html()

    def _gen_html(self):
        """Loops through the object's
        attributes and children, formats them
        into html, and sets self._html equal
        to the calculated string."""

        # The character to insert for newlines
        # Unless the child is an Element, gets set to empty
        inserted_char = '\n'

        # The str version of the attributes; this var is
        #  used to store the data between loops
        attr_list = ''

        # The str version of the attributes; this var is
        #  used to store the data between loops
        children_list = ''

        # If there are no attributes, we still need a
        #  space for it to be valid HTML
        if len(self._attributes) > 0:
            attr_list += ' '

        # For every attribute entered:
        for attr_name, attr_val in self._attributes.items():

            # If neither the name or value are None (implying
            #  it is a valid attribute):
            if attr_name is not None and attr_val is not None:

                # Special case handling for the 'Class' attribute:
                #  all objects have a .class method; therefore we
                #  have to call our class attribute something
                #  slightly different to avoid errors.

                # If it is not a specialized attribute:
                if attr_name[0:4] != 'HTML':

                    if type(attr_val) == type(''):
                        # Add the attribute normally. 'attribute=value'
                        attr_list += f'{attr_name}=\"{attr_val}\"'
                    else:
                        # Add the attribute normally. 'attribute=value'
                        attr_list += f'{attr_name}={attr_val}'

                else:

                    if type(attr_val) == type(''):
                        # Add the specialized attribute.
                        attr_list += f'{attr_name[4:]}=\"{attr_val}\"'
                    else:
                        # Add the specialized attribute.
                        attr_list += f'{attr_name[4:]}={attr_val}'

            # If the attribute has a name but no value, it means
            #  we want a special type of attribute. If this type
            #  is used, it's name is entered with no '='.
            #  For ex. <button disabled> created by Element('button', {'disabled': None})

            # else if the attribute has a value of None:
            elif attr_val is None:

                # Add only the attribute name.
                attr_list += f'{attr_name}'

            # If we're not on the last attribute:
            if attr_name != list(self._attributes.keys())[-1]:
                # Add a space between this attribute and the next.
                attr_list += ' '

        # For every child object:
        try:
            for child in self._items:

                # If the child is an Element object:
                if issubclass(type(child), Element):

                    # Update it and it's childrens' HTML.
                    child.reload()

                # Else if the child is a String or None object:
                elif type(child) is str or child is None:

                    # Set the inserted char to empty.
                    inserted_char = ''

                # Update the children_list
                child = str(child).strip('\n')
                children_list += f'{child}\n'

        except TypeError:
            pass

        # If the end tag (</Element>) is set to False:
        if self.end_tag is not True:

            # Save the updated HTML to the object, without the end tag.
            self._html = f"""<{self.tag}{attr_list}>{inserted_char}{children_list}"""

        # If the Element is not a comment:
        elif self.tag != '!--':

            # Save the updated HTML to the object.
            self._html = f"""<{self.tag}{attr_list}>{inserted_char}{children_list}</{self.tag}>"""

        # If the Element is a comment:
        else:

            # Save the updated HTML Comment to the object.
            self._html = f"""<{self.tag}{inserted_char}{children_list}-->"""

    def reload(self):
        """Updates the object's HTML.
        Usable as an easy-to-overwrite
        public call to _gen_html"""

        self._gen_html()

    def __getitem__(self, key):
        """Magic Method override; returns
        the appropriate value when
        indexing into the object"""

        try:
            return self._items[key]

        except IndexError as e:
            print('Key: ' + str(key))
            raise e

    def __setitem__(self, key, value):
        """Magic Method override; sets
        the appropriate value when
        indexing into the object;
        updates HTML"""

        self._items[key] = value
        self._gen_html()

    def __getattr__(self, item):
        super().__getattribute__(item)

    def set_items(self, value: list):
        """Sets the self._items array to a
        value; updates HTML"""

        self._items = value
        self._gen_html()
        return self

    def add_item(self, item):
        """Appends an item onto self.items;
        updates HTML"""

        self._items.append(item)
        self._gen_html()
        return self

    def add_items(self, value: list):
        """Appends a list of values onto
        self.items; updates HTML"""

        for item in value:
            self._items.append(item)
        self._gen_html()
        return self

    # https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
    #  plus some personal additions to allow normal attr access as well
    # def __getattr__(self, name):
    #     """Magic Method override; Returns
    #     items in self._attributes as if they
    #     were actual attributes / properties"""
    #
    #     try:
    #
    #         return self._attributes
    #
    #     except KeyError:
    #
    #         try:
    #
    #             return super().__getattribute__(self, name)
    #
    #         except KeyError:
    #
    #             msg = "'{0}' object has no attribute '{1}'"
    #             raise AttributeError(msg.format(type(self).__name__, name))

    def __str__(self):
        """Magic Method override; Defines
        how to return object as string"""
        return self._html

    def __len__(self):
        """Magic Method override; defines
        how to return object length"""
        return len(self._items)


class A(Element):
    """ Represents an HTML a element;
    Defines a hyperlink

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword download: Str; Specifies that the target will be downloaded when a user clicks on the hyperlink. (default: None)
    :keyword href: Str; Specifies the URL of the page the link goes to. (default: None)
    :keyword hreflang: Str; Specifies the language of the linked document. (default: None)
    :keyword media: Str; Specifies what media/device the linked document is optimized for. (default: None)
    :keyword ping: List of Str; Specifies a space-separated list of URLs to which, when the link is followed, post requests with the body ping will be sent by the browser (in the background). Typically used for tracking. (default: None)
    :keyword referrerpolicy: A.ReferrerPolicy; Specifies which referrer information to send with the link. (default: None)
    :keyword rel: A.Rel; Specifies the relationship between the current document and the linked document. (default: None)
    :keyword target: A.Target; Specifies where to open the linked document. (default: None)
    :keyword HTMLtype: Str; Specifies the media type of the linked document (default: None) """

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        SAME_ORIGIN = 'same-origin'
        STRICT_ORIGIN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    class Rel(CustomEnum):
        ALTERNATE = 'alternate'
        AUTHOR = 'author'
        BOOKMARK = 'bookmark'
        EXTERNAL = 'external'
        HELP = 'help'
        LICENSE = 'license'
        NEXT = 'next'
        NOFOLLOW = 'nofollow'
        NOREFERRER = 'noreferrer'
        NOOPENER = 'noopener'
        PREV = 'prev'
        SEARCH = 'search'
        TAG = 'tag'

    class Target(CustomEnum):
        BLANK = '_blank'
        PARENT = '_parent'
        SELF = '_self'
        TOP = '_top'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.download: str = kwargs.get('download',
                                        None)  # Specifies that the target will be downloaded when a user clicks on the hyperlink
        self.href: str = kwargs.get('href', None)  # Specifies the URL of the page the link goes to
        self.hreflang: str = kwargs.get('hreflang', None)  # Specifies the language of the linked document
        self.media: str = kwargs.get('media', None)  # Specifies what media/device the linked document is optimized for

        # Specifies a space-separated list of URLs to which, when
        # the link is followed, post requests with the body ping
        # will be sent by the browser (in the background). Typically used for tracking.
        self.ping: list[str] = kwargs.get('ping', None)
        self.referrerpolicy: A.ReferrerPolicy = kwargs.get('referrerpolicy',
                                                           None)  # Specifies which referrer information to send with the link
        self.rel: A.Rel = kwargs.get('rel',
                                     None)  # Specifies the relationship between the current document and the linked document
        self.target: A.Target = kwargs.get('target', None)  # Specifies where to open the linked document
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the media type of the linked document

        if self.download is not None: attr.setdefault('download', self.download)
        if self.href is not None: attr.setdefault('href', self.href)
        if self.hreflang is not None: attr.setdefault('hreflang', self.hreflang)
        if self.media is not None: attr.setdefault('media', self.media)
        if self.ping is not None: attr.setdefault('ping', ' '.join(self.ping))
        if self.referrerpolicy is not None and self.referrerpolicy in A.Referrerpolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', A.Referrerpolicy[self.referrerpolicy.name])
        if self.rel is not None and self.rel in A.Rel.__members__.values(): attr.setdefault('rel', A.Rel[self.rel.name])
        if self.target is not None and self.target in A.Target.__members__.values(): attr.setdefault(
            'target', A.Target[self.target.name])
        if self.HTMLtype is not None: attr.setdefault('type', self.HTMLtype)

        super().__init__('a', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Abbr(Element):
    """Represents an HTML Abbreviation element;
    Defines an abbreviation or an acronym

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('abbr', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Address(Element):
    """Represents an HTML Address element;
    Defines contact information for the author/owner of a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('address', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Area(Element):
    """Represents an HTML Area element;
    Defines an area inside an image map.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword alt: Str; Specifies an alternate text for the area. Required if the href attribute is present. (default: None)
    :keyword coords: Str; Specifies the coordinates of the area. (default: None)
    :keyword download: Str; Specifies that the target will be downloaded when a user clicks on the hyperlink. (default: None)
    :keyword href: Str; Specifies the hyperlink target for the area. (default: None)
    :keyword hreflang: Str; Specifies the language of the target URL. (default: None)
    :keyword media: Str; Specifies what media/device the target URL is optimized for. (default: None)
    :keyword referrerpolicy: Area.ReferrerPolicy; Specifies which referrer information to send with the link. (default: None)
    :keyword rel: Area.Rel; Specifies the relationship between the current document and the target URL. (default: None)
    :keyword shape: Area.Shape; Specifies the shape of the area. (default: None)
    :keyword target: Area.Target; Specifies where to open the target URL. (default: None)
    :keyword HTMLtype: Str; Specifies the media type of the target URL. (default: None) """

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        SAME_ORIGIN = 'same-origin'
        STRICT_ORIGIN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    class Rel(CustomEnum):
        ALTERNATE = 'alternate'
        AUTHOR = 'author'
        BOOKMARK = 'bookmark'
        HELP = 'help'
        LICENSE = 'license'
        NEXT = 'next'
        NOFOLLOW = 'nofollow'
        NOREFERRER = 'noreferrer'
        PREFETCH = 'prefetch'
        PREV = 'prev'
        SEARCH = 'search'
        TAG = 'tag'

    class Shape(CustomEnum):
        DEFAULT = 'default'
        RECTANGLE = 'rect'
        CIRCLE = 'circle'
        POLY = 'poly'

    class Target(CustomEnum):
        BLANK = '_blank'
        PARENT = '_parent'
        SELF = '_self'
        TOP = '_top'

    def __init__(self, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.alt: str = kwargs.get('alt',
                                   None)  # Specifies an alternate text for the area. Required if the href attribute is present
        self.coords: str = kwargs.get('coords', None)  # Specifies the coordinates of the area
        self.download: str = kwargs.get('download',
                                        None)  # Specifies that the target will be downloaded when a user clicks on the hyperlink
        self.href: str = kwargs.get('href', None)  # Specifies the hyperlink target for the area
        self.hreflang: str = kwargs.get('hreflang', None)  # Specifies the language of the target URL
        self.media: str = kwargs.get('media', None)  # Specifies what media/device the target URL is optimized for
        self.referrerpolicy: Area.ReferrerPolicy = kwargs.get('referrerpolicy',
                                                              None)  # Specifies which referrer information to send with the link
        self.rel: Area.Rel = kwargs.get('rel',
                                        None)  # Specifies the relationship between the current document and the target URL
        self.shape: Area.Shape = kwargs.get('shape', None)  # Specifies the shape of the area
        self.target: Area.Target = kwargs.get('target', None)  # Specifies where to open the target URL
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the media type of the target URL

        if self.alt is not None:
            attr.setdefault('alt', self.alt)
        elif self.href is not None:
            raise AttributeError('alt attribute is required if the href attribute is present.')
        if self.coords is not None: attr.setdefault('coords', self.coords)
        if self.download is not None: attr.setdefault('shape', self.shape)
        if self.href is not None: attr.setdefault('href', self.href)
        if self.hreflang is not None: attr.setdefault('hreflang', self.hreflang)
        if self.media is not None: attr.setdefault('media', self.media)
        if self.referrerpolicy is not None and self.referrerpolicy in Area.Referrerpolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', Area.Referrerpolicy[self.referrerpolicy.name])
        if self.rel is not None and self.rel in Area.Rel.__members__.values(): attr.setdefault('rel',
                                                                                               Area.Rel[self.rel.name])
        if self.shape is not None and self.shape in Area.Shape.__members__.values(): attr.setdefault('shape',
                                                                                                     Area.Shape[
                                                                                                         self.shape.name])
        if self.target is not None: attr.setdefault('target', self.target)
        if self.HTMLtype is not None: attr.setdefault('type', self.HTMLtype)

        super().__init__('area', attr=attr, html=html, end_tag=False)


class Article(Element):
    """Represents an HTML Article element;
    Defines an article.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('article', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Aside(Element):
    """Represents an HTML Aside element;
    Defines content aside from the page content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('aside', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Audio(Element):
    """Represents an HTML Audio element;
    Defines embedded sound content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword autoplay: Bool; Specifies that the audio will start playing as soon as it is ready. (default: False)
    :keyword controls: Bool; Specifies that audio controls should be displayed (such as a play/pause button etc). (default: False)
    :keyword loop: Bool; Specifies that the audio will start over again, every time it is finished. (default: False)
    :keyword muted: Bool; Specifies that the audio output should be muted. (default: False)
    :keyword preload: Audio.Preload; Specifies if and how the author thinks the audio should be loaded when the page loads. (default: None) """

    class Preload(CustomEnum):
        AUTO = 'auto'
        METADATA = 'metadata'
        NONE = 'none'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.autoplay: bool = kwargs.get('autoplay',
                                         False)  # Specifies that the audio will start playing as soon as it is ready
        self.controls: bool = kwargs.get('controls',
                                         False)  # Specifies that audio controls should be displayed (such as a play/pause button etc)
        self.loop: bool = kwargs.get('loop',
                                     False)  # Specifies that the audio will start over again, every time it is finished
        self.muted: bool = kwargs.get('muted', False)  # Specifies that the audio output should be muted
        self.preload: Audio.Preload = kwargs.get('preload',
                                                 None)  # Specifies if and how the author thinks the audio should be loaded when the page loads

        if self.autoplay: attr.setdefault('autoplay', None)
        if self.controls: attr.setdefault('controls', None)
        if self.loop: attr.setdefault('loop', None)
        if self.muted: attr.setdefault('muted', None)
        if self.preload is not None and self.preload in Audio.Preload.__members__.values(): attr.setdefault('preload',
                                                                                                            Audio.Preload[
                                                                                                                self.preload.name])

        super().__init__('audio', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class B(Element):
    """Represents an HTML b element;
    Defines bold text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('b', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Base(Element):
    """Represents an HTML Base element;
    Specifies the base URL/target for all relative URLs in a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword href: Str; Specifies the base URL for all relative URLs in the page. (default: None)
    :keyword target: Base.Target; Specifies the default target for all hyperlinks and forms in the page. (default: None) """

    class Target(CustomEnum):
        BLANK = '_blank'
        PARENT = '_parent'
        SELF = '_self'
        TOP = '_top'

    def __init__(self, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.href: str = kwargs.get('href', None)  # Specifies the base URL for all relative URLs in the page
        self.target: Base.Target = kwargs.get('target',
                                              None)  # Specifies the default target for all hyperlinks and forms in the page

        if self.href is not None: attr.setdefault('href', self.href)
        if self.target is not None and self.target in Base.Target.__members__.values(): attr.setdefault(
            'target', Base.Target[self.target.name])

        super().__init__('base', attr=attr, html=html, end_tag=True)


class BDI(Element):
    """Represents an HTML Bdi element;
    Isolates a part of text that might be formatted in a different direction from other text outside it.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('bdi', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class BDO(Element):
    """Represents an HTML Bdo element;
    Overrides the current text direction.

    :param HTMLdir: BDO.Direction; Required. Specifies the text direction of the text inside the bdo element. (default: BDO.Direction.LEFT_TO_RIGHT)

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None) """

    class Direction(CustomEnum):
        LEFT_TO_RIGHT = 'ltr'
        RIGHT_TO_LEFT = 'rtl'

    def __init__(self, HTMLdir: Direction, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.HTMLdir = HTMLdir  # Required. Specifies the text direction of the text inside the <bdo> element

        # Specifies the text direction of the text inside the <bdo> element
        if self.HTMLdir is not None and self.HTMLdir in BDO.Direction: attr.setdefault('dir',
                                                                                       BDO.Direction[self.HTMLdir.name])

        super().__init__('bdo', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Blockquote(Element):
    """Represents an HTML Blockquote element;
    Defines a section that is quoted from another source.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword cite: Str; Specifies the source of the quotation. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.cite: str = kwargs.get('cite', None)  # Specifies the source of the quotation

        if self.cite is not None: attr.setdefault('cite', self.cite)

        super().__init__('blockquote', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Body(Element):
    """Represents an HTML Body element;
    Defines the document's body.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('body', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class BR(Element):
    """Represents an HTML br element;
    Defines a single line break.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('br', attr=attr, html=html, end_tag=False)


class Button(Element):
    """Represents an HTML Button element;
    Defines a clickable button.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword autofocus: Bool; Specifies that a button should automatically get focus when the page loads. (default: False)
    :keyword disabled: Bool; Specifies that a button should be disabled. (default: False)
    :keyword form: Str; Specifies which form the button belongs to. (default: None)
    :keyword formaction: Str; Specifies where to send the form-data when a form is submitted. Only for type="submit". (default: None)
    :keyword formenctype: Form.EncType; Specifies how form-data should be encoded before sending it to a server. Only for type="submit". (default: None)
    :keyword formmethod: Form.Method; Specifies how to send the form-data (which HTTP method to use). Only for type="submit". (default: None)
    :keyword formnovalidate: Bool; Specifies that the form-data should not be validated on submission. Only for type="submit". (default: False)
    :keyword formtarget: Form.Target or Str; Specifies where to display the response after submitting the form. Only for type="submit". (default: None)
    :keyword name: Str; Specifies a name for the button. (default: None)
    :keyword HTMLtype: Button.Type; Specifies the type of button. (default: None)
    :keyword value: Str; Specifies an initial value for the button. (default: None) """

    class Type(CustomEnum):
        BUTTON = 'button'
        RESET = 'reset'
        SUBMIT = 'submit'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.autofocus: bool = kwargs.get('autofocus', False)  # Specifies that a button should automatically get focus when the page loads
        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that a button should be disabled
        self.form: str = kwargs.get('form', None)  # Specifies which form the button belongs to
        self.formaction: str = kwargs.get('formaction', None)  # Specifies where to send the form-data when a form is submitted. Only for type="submit"
        self.formenctype: Form.EncType = kwargs.get('formenctype', None)  # Specifies how form-data should be encoded before sending it to a server. Only for type="submit"
        self.formmethod: Form.Method = kwargs.get('formmethod', None)  # Specifies how to send the form-data (which HTTP method to use). Only for type="submit"
        self.formnovalidate: bool = kwargs.get('formnovalidate', False)  # Specifies that the form-data should not be validated on submission. Only for type="submit"
        self.formtarget: [Form.Target, str] = kwargs.get('formtarget', None)  # Specifies where to display the response after submitting the form. Only for type="submit"
        self.name: str = kwargs.get('name', None)  # Specifies a name for the button
        self.HTMLtype: Button.Type = kwargs.get('HTMLtype', None)  # Specifies the type of button
        self.value: str = kwargs.get('value', None)  # Specifies an initial value for the button

        if self.autofocus: attr.setdefault('autofocus', None)
        if self.disabled: attr.setdefault('disabled', None)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.formaction is not None and self.HTMLtype == Button.Type.SUBMIT: attr.setdefault('formaction', self.formaction)
        if self.formenctype is not None and self.HTMLtype == Button.Type.SUBMIT: attr.setdefault('formenctype', self.formenctype)
        if self.formmethod is not None and self.formmethod in Form.Method and self.HTMLtype == Button.Type.SUBMIT: attr.setdefault('formmethod', self.formmethod)
        if self.formnovalidate is not None and self.HTMLtype == Button.Type.SUBMIT: attr.setdefault('formnovalidate', None)
        if self.formtarget is not None and self.HTMLtype == Button.Type.SUBMIT:
            if self.formtarget in Form.Target.__members__.values():
                attr.setdefault('formtarget', Form.Target[self.formtarget.name])
            else:
                attr.setdefault('formtarget', self.formtarget)
        if self.name is not None: attr.setdefault('name', self.name)
        if self.HTMLtype is not None and self.HTMLtype in Button.Type.__members__.values(): attr.setdefault('type', Button.Type[self.HTMLtype.name])
        elif self.HTMLtype is not None and self.HTMLtype in Button.Type.__members__.keys(): attr.setdefault('type', Button.Type[self.HTMLtype.name])
        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('button', attr=attr, html=html, end_tag=False)
        if items is not None: self.set_items(items)


class Canvas(Element):
    """Represents an HTML Canvas Element;
    Used to draw graphics, on the fly, via scripting (usually JavaScript).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword height: Float; Specifies the height of the canvas. Default value is 150. (default: None)
    :keyword width: Float; Specifies the width of the canvas Default value is 300. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.height: float = kwargs.get('height', None)  # Specifies the height of the canvas. Default value is 150
        self.width: float = kwargs.get('width', None)  # Specifies the width of the canvas Default value is 300

        if self.height is not None: attr.setdefault('height', str(self.height) + 'px')
        if self.width is not None: attr.setdefault('width', str(self.width) + 'px')

        super().__init__('canvas', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Caption(Element):
    """Represents an HTML Caption Element;
    Defines a table caption.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('caption', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Cite(Element):
    """Represents an HTML Cite Element;
    Defines the title of a work.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('cite', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Code(Element):
    """Represents an HTML Code Element;
    Defines a piece of computer code.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('code', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Col(Element):
    """Represents an HTML Col Element;
    Specifies column properties for each column within a <colgroup> element.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('col', attr=attr, html=html, end_tag=False)
        if items is not None: self.set_items(items)


class ColGroup(Element):
    """Represents an HTML ColGroup Element;
    Specifies a group of one or more columns in a table for formatting.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('colgroup', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Comment(Element):
    """Represents an HTML Comment Element;
    Defines a comment.

    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        html: str = kwargs.get('html', None)

        super().__init__('!--', html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Data(Element):
    """Represents an HTML Data Element;
    Adds a machine-readable translation of a given content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword value: Str; Specifies the machine-readable translation of the content of the element. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.value: str = kwargs.get('value',
                                     None)  # Specifies the machine-readable translation of the content of the element

        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('data', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class DataList(Element):
    """Represents an HTML DataList Element;
    Specifies a list of pre-defined options for input controls.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('datalist', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class DD(Element):
    """Represents an HTML DD Element;
    Defines a description/value of a term in a description list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('dd', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Del(Element):
    """Represents an HTML Del Element;
    Defines text that has been deleted from a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword cite: Str; Specifies a URL to a document that explains the reason why the text was deleted/changed. (default: None)
    :keyword datetime: Datetime; Specifies the date and time of when the text was deleted/changed. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.cite: str = kwargs.get('cite', None)
        self.datetime: datetime = kwargs.get('datetime', None)

        if self.cite is not None: attr.setdefault('cite',
                                                  self.cite)  # Specifies a URL to a document that explains the reason why the text was deleted/changed
        if self.datetime is not None: attr.setdefault('datetime', repr(
            self.datetime))  # Specifies the date and time of when the text was deleted/changed

        super().__init__('del', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Details(Element):
    """Represents an HTML Details Element;
    Defines additional details that the user can view or hide.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword open: Bool; Specifies that the details should be visible (open) to the user. (default: False) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.open: bool = kwargs.get('open', False)  # Specifies that the details should be visible (open) to the user

        if self.open: attr.setdefault('open', None)

        super().__init__('details', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class DFN(Element):
    """Represents an HTML DFN Element;
    Specifies a term that is going to be defined within the content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('dfn', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Dialog(Element):
    """Represents an HTML Dialog Element;
    Defines a dialog box or window.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword open: Bool; Specifies that the dialog element is active and that the user can interact with it. (default: False) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.open: bool = kwargs.get('open',
                                     False)  # Specifies that the dialog element is active and that the user can interact with it

        if self.open: attr.setdefault('open', None)

        super().__init__('dialog', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Div(Element):
    """Represents an HTML Div Element;
    Defines a section in a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('div', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class DL(Element):
    """Represents an HTML DL Element;
    Defines a description list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('dl', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class DT(Element):
    """Represents an HTML DT Element;
    Defines a term/name in a description list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('dt', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class EM(Element):
    """Represents an HTML EM Element;
    Defines emphasized text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('em', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Embed(Element):
    """Represents an HTML Embed Element;
    Defines a container for an external application.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword height: Float; Specifies the height of the embedded content. (default: None)
    :keyword width: Float; Specifies the width of the embedded content. (default: None)
    :keyword src: Str; Specifies the media type of the embedded content. (default: None)
    :keyword HTMLtype: Str; Specifies the address of the external file to embed. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.height: float = kwargs.get('height', None)  # Specifies the height of the embedded content
        self.width: float = kwargs.get('width', None)  # Specifies the width of the embedded content
        self.src: str = kwargs.get('src', None)  # Specifies the media type of the embedded content
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the address of the external file to embed

        if self.height is not None: attr.setdefault('height', str(self.height))
        if self.width is not None: attr.setdefault('width', str(self.width))
        if self.src is not None: attr.setdefault('src', str(self.src))
        if self.HTMLtype is not None: attr.setdefault('type', str(self.type))

        super().__init__('embed', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Fieldset(Element):
    """Represents an HTML Fieldset Element;
    Groups related elements in a form.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword disabled: Bool; Specifies that a group of related form elements should be disabled. (default: False)
    :keyword form: Str; Specifies which form the fieldset belongs to. (default: None)
    :keyword name: Str; Specifies a name for the fieldset. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.disabled: bool = kwargs.get('disabled',
                                         False)  # Specifies that a group of related form elements should be disabled
        self.form: str = kwargs.get('form', None)  # Specifies which form the fieldset belongs to
        self.name: str = kwargs.get('name', None)  # Specifies a name for the fieldset

        if self.disabled: attr.setdefault('disabled', None)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.name is not None: attr.setdefault('name', self.name)

        super().__init__('fieldset', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class FigCaption(Element):
    """Represents an HTML FigCaption Element;
    Defines a caption for a <figure> element.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('figcaption', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Figure(Element):
    """Represents an HTML Figure Element;
    Specifies self-contained content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('figure', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Footer(Element):
    """Represents an HTML Footer Element;
    Defines a footer for a document or section.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('footer', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Form(Element):
    """Represents an HTML Form Element;
    Defines an HTML form for user input.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword acceptcharset: Str; Specifies the character encodings that are to be used for the form submission. (default: None)
    :keyword action: Str; Specifies where to send the form-data when a form is submitted. (default: None)
    :keyword autocomplete: Bool; Specifies whether a form should have autocomplete on or off. (default: False)
    :keyword enctype: Form.EncType; Specifies how the form-data should be encoded when submitting it to the server (only for method="post"). (default: None)
    :keyword method: Form.Method; Specifies the HTTP method to use when sending form-data. (default: None)
    :keyword name: Str; Specifies the name of a form. (default: None)
    :keyword novalidate: Bool; Specifies that the form should not be validated when submitted. (default: False)
    :keyword rel: Form.Rel; Specifies the relationship between a linked resource and the current document. (default: None)
    :keyword target: Form.Target; Specifies where to display the response that is received after submitting the form. (default: None) """

    class EncType(CustomEnum):
        APPLICATION = 'application/x-www-form-urlencoded'
        MULTIPART = 'multipart/form-data'
        TEXT = 'text/plain'

    class Method(CustomEnum):
        GET = 'get'
        POST = 'post'

    class Rel(CustomEnum):
        EXTERNAL = 'external'
        HELP = 'help'
        LICENSE = 'license'
        NEXT = 'next'
        NOFOLLOW = 'nofollow'
        NOOPENER = 'noopener'
        NOREFERRER = 'noreferrer'
        OPENER = 'opener'
        PREV = 'prev'
        SEARCH = 'search'

    class Target(CustomEnum):
        BLANK = '_blank'
        PARENT = '_parent'
        SELF = '_self'
        TOP = '_top'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.acceptcharset: str = kwargs.get('acceptcharset', None)  # Specifies the character encodings that are to be used for the form submission
        self.action: str = kwargs.get('action', None)  # Specifies where to send the form-data when a form is submitted
        self.autocomplete: bool = kwargs.get('autocomplete', False)  # Specifies whether a form should have autocomplete on or off
        self.enctype: Form.EncType = kwargs.get('enctype', None)  # Specifies how the form-data should be encoded when submitting it to the server (only for method="post")
        self.method: Form.Method = kwargs.get('method', None)  # Specifies the HTTP method to use when sending form-data
        self.name: str = kwargs.get('name', None)  # Specifies the name of a form
        self.novalidate: bool = kwargs.get('novalidate', False)  # Specifies that the form should not be validated when submitted
        self.rel: Form.Rel = kwargs.get('rel', None)  # Specifies the relationship between a linked resource and the current document
        self.target: Form.Target = kwargs.get('target', None)  # Specifies where to display the response that is received after submitting the form

        if self.acceptcharset is not None: attr.setdefault('accept-charset', self.acceptcharset)
        if self.action is not None: attr.setdefault('action', self.action)
        if self.autocomplete and self.autocomplete is not None:
            attr.setdefault('autocomplete', 'on')
        elif not self.autocomplete and self.autocomplete is not None:
            attr.setdefault('autocomplete', 'off')
        if self.enctype is not None and self.enctype in Form.EncType.__members__.values(): attr.setdefault('enctype', Form.EncType[self.enctype.name])
        if self.method is not None and self.method in Form.Method.__members__.values(): attr.setdefault('method', Form.Method[self.method.name])
        if self.name is not None: attr.setdefault('name', self.name)
        if self.novalidate: attr.setdefault('novalidate', None)
        if self.rel is not None and self.rel in Form.Rel.__members__.values(): attr.setdefault('rel', Form.Rel[self.rel.name])
        if self.target is not None and self.target in Form.Target.__members__.values(): attr.setdefault('target', Form.Target[self.target.name])

        super().__init__('form', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class H(Element):
    """Represents Elements h1 through h6;
    Defines HTML headings.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword headertype: Int; Used to identify which header type to create. (default: 1) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        headertype: int = kwargs.get('headertype', 1)  # Used to identify which header type to create
        if headertype < 1:
            headertype = 1
        elif headertype > 6:
            headertype = 6

        super().__init__('h' + str(headertype), attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Head(Element):
    """Represents an HTML Head Element;
    Contains metadata/information for the document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('head', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Header(Element):
    """Represents an HTML Header Element;
    Defines a header for a document or section.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('header', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class HR(Element):
    """Represents an HTML HR Element;
    Defines a thematic change in the content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('hr', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class HTML(Element):
    """Represents an HTML HTML Element;
    Defines the root of an HTML document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword xmlns: Str; Specifies the XML namespace attribute (If you need your content to conform to XHTML). (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        # Specifies the XML namespace attribute (If you need your content to conform to XHTML)
        self.xmlns: str = kwargs.get('xmlns', None)

        if self.xmlns is not None: attr.setdefault('xmlns', self.xmlns)

        super().__init__('html', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class I(Element):
    """Represents an HTML I Element;
    Defines a part of text in an alternate voice or mood.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('i', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class IFrame(Element):
    """Represents an HTML IFrame Element;
    Defines an inline frame.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword allowfullscreen: Bool; Set to true if the <iframe> can activate fullscreen mode by calling the requestFullscreen() method. (default: None)
    :keyword allowpaymentrequest: Bool; Set to true if a cross-origin <iframe> should be allowed to invoke the Payment Request API. (default: None)
    :keyword height: Float; Specifies the height of an <iframe>. Default height is 150 pixels. (default: None)
    :keyword width: Float; Specifies the width of an <iframe>. Default width is 300 pixels. (default: None)
    :keyword loading: IFrame.Loading; Specifies whether a browser should load an iframe immediately or to defer loading of iframes until some conditions are met. (default: None)
    :keyword name: Str; Specifies the name of an <iframe>. (default: None)
    :keyword referrerpolicy: IFrame.ReferrerPolicy; Specifies which referrer information to send when fetching the iframe. (default: None)
    :keyword sandbox: IFrame.Sandbox; Enables an extra set of restrictions for the content in an <iframe>. (default: None)
    :keyword src: Str; Specifies the address of the document to embed in the <iframe>. (default: None)
    :keyword srcdoc: Str; Specifies the HTML content of the page to show in the <iframe>. (default: None) """

    class Loading(CustomEnum):
        EAGER = 'eager'
        LAZY = 'lazy'

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        SAME_ORIGIN = 'same-origin'
        STRICT_ORIGIN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    class Sandbox(CustomEnum):
        ALLOW_FORMS = 'allow-forms'
        ALLOW_POINTER_LOCK = 'allow-pointer-lock'
        ALLOW_POPUPS = 'allow-popups'
        ALLOW_SAME_ORIGIN = 'allow-same-origin'
        ALLOW_SCRIPTS = 'allow-scripts'
        ALLOW_TOP_NAVIGATION = 'allow_top_navigation'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.allowfullscreen: bool = kwargs.get('allowfullscreen',
                                                None)  # Set to true if the <iframe> can activate fullscreen mode by calling the requestFullscreen() method
        self.allowpaymentrequest: bool = kwargs.get('allowpaymentrequest',
                                                    None)  # Set to true if a cross-origin <iframe> should be allowed to invoke the Payment Request API
        self.height: float = kwargs.get('height',
                                        None)  # Specifies the height of an <iframe>. Default height is 150 pixels
        self.width: float = kwargs.get('width', None)  # Specifies the width of an <iframe>. Default width is 300 pixels
        self.loading: IFrame.Loading = kwargs.get('loading',
                                                  None)  # Specifies whether a browser should load an iframe immediately or to defer loading of iframes until some conditions are met
        self.name: str = kwargs.get('name', None)  # Specifies the name of an <iframe>
        self.referrerpolicy: IFrame.ReferrerPolicy = kwargs.get('referrerpolicy',
                                                                None)  # Specifies which referrer information to send when fetching the iframe
        self.sandbox: IFrame.Sandbox = kwargs.get('sandbox',
                                                  None)  # Enables an extra set of restrictions for the content in an <iframe>
        self.src: str = kwargs.get('src', None)  # Specifies the address of the document to embed in the <iframe>
        self.srcdoc: str = kwargs.get('srcdoc', None)  # Specifies the HTML content of the page to show in the <iframe>

        if self.allowfullscreen is not None and self.allowfullscreen:
            attr.setdefault('allowfullscreen', True)
        elif self.allowfullscreen is not None and not self.allowfullscreen:
            attr.setdefault('allowfullscreen', False)
        if self.allowpaymentrequest is not None and self.allowpaymentrequest:
            attr.setdefault('allowpaymentrequest', True)
        elif self.allowpaymentrequest is not None and not self.allowpaymentrequest:
            attr.setdefault('allowpaymentrequest', False)
        if self.height is not None: attr.setdefault('height', self.height)
        if self.width is not None: attr.setdefault('width', self.width)
        if self.loading is not None and self.loading in IFrame.Loading.__members__.values(): attr.setdefault('loading',
                                                                                                             IFrame.Loading[
                                                                                                                 self.loading.name])
        if self.referrerpolicy is not None and self.referrerpolicy in IFrame.Referrerpolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', IFrame.Referrerpolicy[self.referrerpolicy.name])
        if self.sandbox is not None and self.sandbox in IFrame.Sandbox.__members__.values(): attr.setdefault('sandbox',
                                                                                                             IFrame.Sandbox[
                                                                                                                 self.sandbox.name])
        if self.src is not None: attr.setdefault('src', self.src)
        if self.srcdoc is not None: attr.setdefault('srcdoc', self.srcdoc)

        super().__init__('iframe', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Img(Element):
    """Represents an HTML Img Element;
    Defines an image.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword alt: Str; Specifies an alternate text for an image. (default: None)
    :keyword crossorigin: Img.CrossOrigin; Allow images from third-party sites that allow cross-origin access to be used with canvas. (default: None)
    :keyword height: Float; Specifies the height of an image. (default: None)
    :keyword width: Float; Specifies the width of an image. (default: None)
    :keyword ismap: Bool; Specifies an image as a server-side image map. (default: False)
    :keyword loading: Img.Loading; Specifies whether a browser should load an image immediately or to defer loading of images until some conditions are met. (default: None)
    :keyword longdesc: Str; Specifies a URL to a detailed description of an image. (default: None)
    :keyword referrerpolicy: Img.ReferrerPolicy; Specifies which referrer information to use when fetching an image. (default: None)
    :keyword sizes: Str; Specifies image sizes for different page layouts. (default: None)
    :keyword src: Str; Specifies the path to the image. (default: None)
    :keyword srcset: List of Str; Specifies a list of image files to use in different situations. (default: None)
    :keyword usemap: Str; Specifies an image as a client-side image map. (default: None) """

    class CrossOrigin(CustomEnum):
        ANONYMOUS = 'anonymous'
        USE_CREDENTIALS = 'use-credentials'

    class Loading(CustomEnum):
        EAGER = 'eager'
        LAZY = 'lazy'

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        SAME_ORIGIN = 'same-origin'
        STRICT_ORIGIN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.alt: str = kwargs.get('alt', None)  # Specifies an alternate text for an image
        self.crossorigin: Img.CrossOrigin = kwargs.get('crossorigin',
                                                       None)  # Allow images from third-party sites that allow cross-origin access to be used with canvas
        self.height: float = kwargs.get('height', None)  # Specifies the height of an image
        self.width: float = kwargs.get('width', None)  # Specifies the width of an image
        self.ismap: bool = kwargs.get('ismap', False)  # Specifies an image as a server-side image map
        self.loading: Img.Loading = kwargs.get('loading',
                                               None)  # Specifies whether a browser should load an image immediately or to defer loading of images until some conditions are met
        self.longdesc: str = kwargs.get('longdesc', None)  # Specifies a URL to a detailed description of an image
        self.referrerpolicy: Img.Referrerpolicy = kwargs.get('referrerpolicy',
                                                             None)  # Specifies which referrer information to use when fetching an image
        self.sizes: str = kwargs.get('sizes', None)  # Specifies image sizes for different page layouts
        self.src: str = kwargs.get('src', None)  # Specifies the path to the image
        self.srcset: list[str] = kwargs.get('srcset',
                                            None)  # Specifies a list of image files to use in different situations
        self.usemap: str = kwargs.get('usemap', None)  # Specifies an image as a client-side image map

        if self.alt is not None: attr.setdefault('alt', self.alt)
        if self.crossorigin is not None and self.crossorigin in Img.CrossOrigin.__members__.values(): attr.setdefault(
            'crossorigin', Img.CrossOrigin[self.crossorigin.name])
        if self.height is not None: attr.setdefault('height', self.height)
        if self.width is not None: attr.setdefault('width', self.width)
        if self.ismap: attr.setdefault('ismap', None)
        if self.loading is not None and self.loading in Img.Loading.__members__.values(): attr.setdefault('loading',
                                                                                                          Img.Loading[
                                                                                                              self.loading.name])
        if self.longdesc is not None: attr.setdefault('longdesc', self.longdesc)
        if self.referrerpolicy is not None and self.referrerpolicy in Img.Referrerpolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', Img.Referrerpolicy[self.referrerpolicy])
        if self.sizes is not None: attr.setdefault('sizes', self.sizes)
        if self.src is not None: attr.setdefault('src', self.src)
        if self.srcset is not None: attr.setdefault('srcset', str(', '.join(self.srcset)))
        if self.usemap is not None:
            if self.usemap[0] != '#': self.usemap = '#' + str(self.usemap)
            attr.setdefault('usemap', self.usemap)

        super().__init__('img', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Input(Element):
    """Represents an HTML Input Element;
    Defines an input control.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword accept: List of Input.Accept's and Str; Specifies a filter for what file types the user can pick from the file input dialog box (only for type="file"). (default: None)
    :keyword alt: Str; Specifies an alternate text for images (only for type="image"). (default: None)
    :keyword autocomplete: Bool; Specifies whether an input element should have autocomplete enabled. (default: None)
    :keyword autofocus: Bool; Specifies that an input element should automatically get focus when the page loads. (default: False)
    :keyword checked: Bool; Specifies that an input element should be pre-selected when the page loads (for type="checkbox" or type="radio"). (default: False)
    :keyword dirname: Str; Specifies that the text direction will be submitted. (default: None)
    :keyword disabled: Bool; Specifies that an input element should be disabled. (default: False)
    :keyword form: Str; Specifies the form the input element belongs to. (default: None)
    :keyword formaction: Str; Specifies the URL of the file that will process the input control when the form is submitted (for type="submit" and type="image"). (default: None)
    :keyword formenctype: Form.EncType; Specifies how the form-data should be encoded when submitting it to the server (for type="submit" and type="image"). (default: None)
    :keyword formmethod: Form.Method; Defines the HTTP method for sending data to the action URL (for type="submit" and type="image"). (default: None)
    :keyword formnovalidate: Bool; Defines that form elements should not be validated when submitted. (default: False)
    :keyword formtarget: Form.Target or Str; Specifies where to display the response that is received after submitting the form (for type="submit" and type="image"). (default: None)
    :keyword height: Float; Specifies the height of an input element (only for type="image"). (default: None)
    :keyword width: Float; Specifies the width of an input element (only for type="image"). (default: None)
    :keyword list: Str; Refers to a <datalist> element that contains pre-defined options for an input element. (default: None)
    :keyword max: Str or Int; Specifies the maximum value for an input element. (default: None)
    :keyword maxlength: Int; Specifies the maximum number of characters allowed in an input element. (default: None)
    :keyword min: Str or Int; Specifies a minimum value for an input element. (default: None)
    :keyword minlength: Int; Specifies the minimum number of characters required in an input element. (default: None)
    :keyword multiple: Bool; Specifies that a user can enter more than one value in an input element. (default: False)
    :keyword name: Str; Specifies the name of an input element. (default: None)
    :keyword pattern: Str; Specifies a regular expression that an input element's value is checked against. (default: None)
    :keyword placeholder: Str; Specifies a short hint that describes the expected value of an input element. (default: None)
    :keyword readonly: Bool; Specifies that an input field is read-only. (default: False)
    :keyword required: Bool; Specifies that an input field must be filled out before submitting the form. (default: False)
    :keyword size: Int; Specifies the width, in characters, of an input element. (default: None)
    :keyword src: Str; Specifies the URL of the image to use as a submit button (only for type="image"). (default: None)
    :keyword step: Str; Specifies the interval between legal numbers in an input field. (default: None)
    :keyword value: Str; Specifies the value of an input element. (default: None) """

    class Type(CustomEnum):
        BUTTON = 'button'
        CHECKBOX = 'checkbox'
        COLOR = 'color'
        DATE = 'date'
        DATETIME = 'datetime-local'
        EMAIL = 'email'
        FILE = 'file'
        HIDDEN = 'hidden'
        IMAGE = 'image'
        MONTH = 'month'
        NUMBER = 'number'
        PASSWORD = 'password'
        RADIO = 'radio'
        RANGE = 'range'
        RESET = 'reset'
        SEARCH = 'search'
        SUBMIT = 'submit'
        TEL = 'tel'
        TEXT = 'text'
        TIME = 'time'
        URL = 'url'
        WEEK = 'week'

    class Accept(CustomEnum):
        FILE_EXTENSION = 'file_extension'
        AUDIO = 'audio/*'
        VIDEO = 'video/*'
        IMAGE = 'image/*'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.HTMLtype: Input.Type = kwargs.get('HTMLtype', Input.Type.TEXT)
        if self.HTMLtype is None: self.HTMLtype = Input.Type.TEXT

        self.accept: list[Input.Accept, str] = kwargs.get('accept',
                                                          None)  # Specifies a filter for what file types the user can pick from the file input dialog box (only for type="file")
        self.alt: str = kwargs.get('alt', None)  # Specifies an alternate text for images (only for type="image")
        self.autocomplete: bool = kwargs.get('autocomplete',
                                             None)  # Specifies whether an input element should have autocomplete enabled
        self.autofocus: bool = kwargs.get('autofocus',
                                          False)  # Specifies that an input element should automatically get focus when the page loads
        self.checked: bool = kwargs.get('checked',
                                        False)  # Specifies that an input element should be pre-selected when the page loads (for type="checkbox" or type="radio")
        self.dirname: str = kwargs.get('dirname', None)  # Specifies that the text direction will be submitted
        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that an input element should be disabled
        self.form: str = kwargs.get('form', None)  # Specifies the form the input element belongs to
        self.formaction: str = kwargs.get('formaction',
                                          None)  # Specifies the URL of the file that will process the input control when the form is submitted (for type="submit" and type="image")
        self.formenctype: Form.EncType = kwargs.get('formenctype',
                                                    None)  # Specifies how the form-data should be encoded when submitting it to the server (for type="submit" and type="image")
        self.formmethod: Form.Method = kwargs.get('formmethod',
                                                  None)  # Defines the HTTP method for sending data to the action URL (for type="submit" and type="image")
        self.formnovalidate: bool = kwargs.get('formnovalidate',
                                               False)  # Defines that form elements should not be validated when submitted
        self.formtarget: [Form.Target, str] = kwargs.get('formtarget',
                                                         None)  # Specifies where to display the response that is received after submitting the form (for type="submit" and type="image")
        self.height: float = kwargs.get('height',
                                        None)  # Specifies the height of an input element (only for type="image")
        self.width: float = kwargs.get('width',
                                       None)  # Specifies the width of an input element (only for type="image")
        self.list: str = kwargs.get('list',
                                    None)  # Refers to a datalist element that contains pre-defined options for an input element
        self.max: [str, int] = kwargs.get('max', None)  # Specifies the maximum value for an input element
        self.maxlength: int = kwargs.get('maxlength',
                                         None)  # Specifies the maximum number of characters allowed in an input element
        self.min: [str, int] = kwargs.get('min', None)  # Specifies a minimum value for an input element
        self.minlength: int = kwargs.get('minlength',
                                         None)  # Specifies the minimum number of characters required in an input element
        self.multiple: bool = kwargs.get('multiple',
                                         False)  # Specifies that a user can enter more than one value in an input element
        self.name: str = kwargs.get('name', None)  # Specifies the name of an input element
        self.pattern: str = kwargs.get('pattern',
                                       None)  # Specifies a regular expression that an input element's value is checked against
        self.placeholder: str = kwargs.get('placeholder',
                                           None)  # Specifies a short hint that describes the expected value of an input element
        self.readonly: bool = kwargs.get('readonly', False)  # Specifies that an input field is read-only
        self.required: bool = kwargs.get('required',
                                         False)  # Specifies that an input field must be filled out before submitting the form
        self.size: int = kwargs.get('size', None)  # Specifies the width, in characters, of an input element
        self.src: str = kwargs.get('src',
                                   None)  # Specifies the URL of the image to use as a submit button (only for type="image")
        self.step: str = kwargs.get('step', None)  # Specifies the interval between legal numbers in an input field
        self.value: str = kwargs.get('value', None)  # Specifies the value of an input element

        attr.setdefault('type', self.HTMLtype.value)

        if self.HTMLtype == Input.Type.CHECKBOX or self.HTMLtype == Input.Type.RADIO:
            if self.checked: attr.setdefault('checked', None)
        elif self.HTMLtype == Input.Type.FILE:
            if self.accept is not None and len(self.accept) > 0:
                if len(self.accept) == 1:
                    if self.accept[0] in Input.Accept.__members__.values():
                        attr.setdefault('accept', Input.Accept[self.accept[0].name])
                    else:
                        attr.setdefault('accept', self.accept[0])
                elif len(self.accept) > 1:
                    for _ in self.accept: _ = str(_)
                    self.accept: list[str]
                    attr.setdefault('accept', ','.join(self.accept))
        elif self.HTMLtype == Input.Type.IMAGE:
            if self.alt is not None: attr.setdefault('alt', self.alt)
            if self.formaction is not None: attr.setdefault('formaction', self.formaction)
            if self.formenctype is not None and self.formenctype in Form.EncType.__members__.values(): attr.setdefault(
                'formenctype', Form.EncType[self.formenctype.name])
            if self.formmethod is not None and self.formmethod in Form.Method.__members__.values(): attr.setdefault(
                'formmethod', Form.Method[self.formmethod.name])
            if self.formtarget is not None and self.formtarget in Form.Target.__members__.values(): attr.setdefault(
                'formtarget', Form.Target[self.formtarget.name])
            if self.height is not None: attr.setdefault('height', self.height)
            if self.width is not None: attr.setdefault('width', self.width)
            if self.src is not None: attr.setdefault('src', self.src)
        elif self.HTMLtype == Input.Type.SUBMIT:
            if self.formaction is not None: attr.setdefault('formaction', self.formaction)
            if self.formenctype is not None and self.formenctype in Form.EncType.__members__.values(): attr.setdefault(
                'formenctype', Form.EncType[self.formenctype.name])
            if self.formmethod is not None and self.formmethod in Form.Method.__members__.values(): attr.setdefault(
                'formmethod', Form.Method[self.formmethod.name])
            if self.formtarget is not None and self.formtarget in Form.Target.__members__.values(): attr.setdefault(
                'formtarget', Form.Target[self.formtarget.name])

        if self.autocomplete is not None: attr.setdefault('autocomplete',
                                                          'on') if self.autocomplete else attr.setdefault(
            'autocomplete', 'off')
        if self.autofocus: attr.setdefault('autofocus', None)
        if self.dirname is not None:
            if self.dirname[-4:-1] != '.dir': self.dirname += '.dir'
            attr.setdefault('dirname', self.dirname)
        if self.disabled: attr.setdefault('disabled', None)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.formnovalidate: attr.setdefault('formnovalidate', None)
        if self.list is not None: attr.setdefault('list', self.list)
        if self.max is not None: attr.setdefault('max', str(self.max))
        if self.maxlength is not None: attr.setdefault('maxlength', str(self.max))
        if self.min is not None: attr.setdefault('min', str(self.min))
        if self.minlength is not None: attr.setdefault('minlength', str(self.max))
        if self.multiple: attr.setdefault('multiple', None)
        if self.name is not None: attr.setdefault('name', self.name)
        if self.pattern is not None: attr.setdefault('pattern', self.pattern)
        if self.placeholder is not None: attr.setdefault('placeholder', self.placeholder)
        if self.readonly: attr.setdefault('readonly', None)
        if self.required: attr.setdefault('required', None)
        if self.size is not None: attr.setdefault('size', self.size)
        if self.step is not None: attr.setdefault('step', str(self.step))
        if self.value is not None: attr.setdefault('value', str(self.value))

        super().__init__('input', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Ins(Element):
    """Represents an HTML Ins Element;
    Defines a text that has been inserted into a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword cite: Specifies a URL to a document that explains the reason why the text was inserted/changed. (default: None)
    :keyword datetime: Specifies a URL to a document that explains the reason why the text was inserted/changed. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.cite: str = kwargs.get('cite',
                                    None)  # Specifies a URL to a document that explains the reason why the text was inserted/changed
        self.datetime: str = kwargs.get('datetime',
                                        None)  # Specifies a URL to a document that explains the reason why the text was inserted/changed

        super().__init__('ins', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Kbd(Element):
    """Represents an HTML Kbd Element;
    Defines keyboard input.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('kbd', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Label(Element):
    """Represents an HTML Label Element;
    Defines a label for an input element.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword HTMLfor: Str; Specifies the id of the form element the label should be bound to. (default: None)
    :keyword form: Str; Specifies which form the label belongs to. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.HTMLfor: str = kwargs.get('HTMLfor', None)  # Specifies the id of the form element the label should be bound to
        self.form: str = kwargs.get('form', None)  # Specifies which form the label belongs to

        if self.HTMLfor is not None: attr.setdefault('for', self.HTMLfor)
        if self.form is not None: attr.setdefault('form', self.form)

        super().__init__('label', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Legend(Element):
    """Represents an HTML Legend Element;
    Defines a caption for a <fieldset> element.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('legend', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class LI(Element):
    """Represents an HTML LI Element;
    Defines a list item.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword value: Int; Only for ol lists. Specifies the start value of a list item. The following list items will increment from that number. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.value: int = kwargs.get('value', None)

        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('li', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Link(Element):
    """Represents an HTML Link Element;
    Defines the relationship between a document and an external resource (most used to link to style sheets).

    :param rel: Link.Rel; Required. Specifies the relationship between the current document and the linked document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword crossorigin: Link.CrossOrigin; Specifies how the element handles cross-origin requests. (default: None)
    :keyword href: Str; Specifies the location of the linked document. (default: None)
    :keyword hreflang: Str; Specifies the language of the text in the linked document. (default: None)
    :keyword media: Str; Specifies on what device the linked document will be displayed. (default: None)
    :keyword referrerpolicy: Link.ReferrerPolicy; Specifies which referrer to use when fetching the resource. (default: None)
    :keyword sizes: Str; Specifies the size of the linked resource. Only for rel="icon". (default: None)
    :keyword HTMLtype: Str; Specifies the media type of the linked document. (default: None) """

    class CrossOrigin(CustomEnum):
        ANONYMOUS = 'anonymous'
        USE_CREDENTIALS = 'use-credentials'

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    class Rel(CustomEnum):
        ALTERNATE = 'alternate'
        AUTHOR = 'author'
        DNS_PREFETCH = 'dns_prefetch'
        HELP = 'help'
        ICON = 'icon'
        LICENSE = 'license'
        NEXT = 'next'
        PINGBACK = 'pingback'
        PRECONNECT = 'preconnect'
        PREFETCH = 'prefetch'
        PRELOAD = 'preload'
        PRERENDER = 'prerender'
        PREV = 'prev'
        SEARCH = 'search'
        STYLESHEET = 'stylesheet'

    def __init__(self, rel: Rel, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.crossorigin: Link.CrossOrigin = kwargs.get('crossorigin',
                                                        None)  # Specifies how the element handles cross-origin requests
        self.href: str = kwargs.get('href', None)  # Specifies the location of the linked document
        self.hreflang: str = kwargs.get('hreflang', None)  # Specifies the language of the text in the linked document
        self.media: str = kwargs.get('media', None)  # Specifies on what device the linked document will be displayed
        self.referrerpolicy: Link.ReferrerPolicy = kwargs.get('referrerpolicy',
                                                              None)  # Specifies which referrer to use when fetching the resource
        self.rel: Link.Rel = rel  # Required. Specifies the relationship between the current document and the linked document
        self.sizes: str = kwargs.get('sizes', None)  # Specifies the size of the linked resource. Only for rel="icon"
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the media type of the linked document

        if self.crossorigin is not None and self.crossorigin in Link.CrossOrigin.__members__.values(): attr.setdefault(
            'crossorigin', Link.CrossOrigin[self.crossorigin.name])
        if self.href is not None: attr.setdefault('href', self.href)
        if self.hreflang is not None: attr.setdefault('hreflang', self.hreflang)
        if self.media is not None: attr.setdefault('media', self.media)
        if self.referrerpolicy is not None and self.referrerpolicy in Link.ReferrerPolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', Link.ReferrerPolicy[self.referrerpolicy.name])
        if self.rel is not None and self.rel in Link.Rel.__members__.values(): attr.setdefault('rel', Link.Rel[self.rel.name])
        if self.sizes is not None: attr.setdefault('sizes', self.sizes)
        if self.HTMLtype is not None: attr.setdefault('type', self.type)

        super().__init__('link', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Main(Element):
    """Represents an HTML Main Element;
    Specifies the main content of a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('main', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Map(Element):
    """Represents an HTML Map Element;
    Defines an image map.

    :param name: Str; Required. Specifies the name of the image map.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None) """

    def __init__(self, name: str, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.name: str = name  # Required. Specifies the name of the image map

        attr.setdefault('name', self.name)

        super().__init__('map', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Mark(Element):
    """Represents an HTML Mark Element;
    Defines marked/highlighted text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('mark', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Meta(Element):
    """Represents an HTML Meta Element;
    Defines metadata about an HTML document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword charset: Str; Specifies the character encoding for the HTML document. (default: None)
    :keyword content: Str; Specifies the value associated with the http-equiv or name attribute. (default: None)
    :keyword httpequiv: Meta.HttpEquiv; Provides an HTTP header for the information/value of the content attribute. (default: None)
    :keyword name: Meta.Name; Specifies a name for the metadata. (default: None) """

    class HttpEquiv(CustomEnum):
        CONTENT_SEC_POLICY = 'content-security-policy'
        CONTENT_TYPE = 'content-type'
        DEFAULT_STYLE = 'default-style'
        REFRESH = 'refresh'

    class Name(CustomEnum):
        APPLICATION_NAME = 'application-name'
        AUTHOR = 'author'
        DESCRIPTION = 'description'
        GENERATOR = 'generator'
        KEYWORDS = 'keywords'
        VIEWPORT = 'viewport'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.charset: str = kwargs.get('charset', None)  # Specifies the character encoding for the HTML document
        self.content: str = kwargs.get('content',
                                       None)  # Specifies the value associated with the http-equiv or name attribute
        self.httpequiv: Meta.HttpEquiv = kwargs.get('httpequiv',
                                                    None)  # Provides an HTTP header for the information/value of the content attribute
        self.name: Meta.Name = kwargs.get('name', None)  # Specifies a name for the metadata

        if self.charset is not None: attr.setdefault('charset', self.charset)
        if self.content is not None: attr.setdefault('content', self.content)
        if self.httpequiv is not None and self.httpequiv in Meta.HttpEquiv.__members__.values(): attr.setdefault(
            'httpequiv', Meta.HttpEquiv[self.httpequiv.name])
        if self.name is not None and self.name in Meta.Name.__members__.values(): attr.setdefault('name', Meta.Name[
            self.Name.name])

        super().__init__('meta', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Meter(Element):
    """Represents an HTML Meter Element;
    Defines a scalar measurement within a known range (a gauge).

    :param value: Float; Required. Specifies the current value of the gauge

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword form: Str; Specifies which form the meter element belongs to. (default: None)
    :keyword high: Float; Specifies the range that is considered to be a high value. (default: None)
    :keyword low: Float; Specifies the range that is considered to be a low value. (default: None)
    :keyword max: Float; Specifies the maximum value of the range. (default: None)
    :keyword min: Float; Specifies the minimum value of the range. Default value is 0. (default: None)
    :keyword optimum: Float; Specifies what value is the optimal value for the gauge. (default: None) """

    def __init__(self, value: float, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.form: str = kwargs.get('form', None)  # Specifies which form the <meter> element belongs to
        self.high: float = kwargs.get('high', None)  # Specifies the range that is considered to be a high value
        self.low: float = kwargs.get('low', None)  # Specifies the range that is considered to be a low value
        self.max: float = kwargs.get('max', None)  # Specifies the maximum value of the range
        self.min: float = kwargs.get('min', None)  # Specifies the minimum value of the range. Default value is 0
        self.optimum: float = kwargs.get('optimum', None)  # Specifies what value is the optimal value for the gauge
        self.value: float = value  # Required. Specifies the current value of the gauge

        attr.setdefault('value', self.value)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.high is not None: attr.setdefault('high', self.high)
        if self.low is not None: attr.setdefault('low', self.low)
        if self.max is not None: attr.setdefault('max', self.max)
        if self.min is not None: attr.setdefault('min', self.min)
        if self.optimum is not None: attr.setdefault('optimum', self.optimum)

        super().__init__('meter', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Nav(Element):
    """Represents an HTML Nav Element;
    Defines navigation links.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('nav', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class NoScript(Element):
    """Represents an HTML NoScript Element;
    Defines an alternate content for users that do not support client-side scripts.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('noscript', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Object(Element):
    """Represents an HTML Object Element;
    Defines a container for an external application.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword data: Str; Specifies the URL of the resource to be used by the object. (default: None)
    :keyword form: Str; Specifies which form the object belongs to. (default: None)
    :keyword height: Float; Specifies the height of the object. (default: None)
    :keyword width: Float; Specifies the width of the object. (default: None)
    :keyword name: Str; Specifies a name for the object. (default: None)
    :keyword HTMLtype: Str; Specifies the media type of data specified in the data attribute. (default: None)
    :keyword typemustmatch: Bool; Specifies whether the type attribute and the actual content of the resource must match to be displayed. (default: None)
    :keyword usemap: Str; Specifies the name of a client-side image map to be used with the object. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.data: str = kwargs.get('data', None)  # Specifies the URL of the resource to be used by the object
        self.form: str = kwargs.get('form', None)  # Specifies which form the object belongs to
        self.height: float = kwargs.get('height', None)  # Specifies the height of the object
        self.width: float = kwargs.get('width', None)  # Specifies the width of the object
        self.name: str = kwargs.get('name', None)  # Specifies a name for the object
        self.HTMLtype: str = kwargs.get('HTMLtype',
                                        None)  # Specifies the media type of data specified in the data attribute
        self.typemustmatch: bool = kwargs.get('typemustmatch',
                                              None)  # Specifies whether the type attribute and the actual content of the resource must match to be displayed
        self.usemap: str = kwargs.get('usemap',
                                      None)  # Specifies the name of a client-side image map to be used with the object

        if self.data is not None: attr.setdefault('data', self.data)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.height is not None: attr.setdefault('height', self.height)
        if self.width is not None: attr.setdefault('width', self.width)
        if self.name is not None: attr.setdefault('name', self.name)
        if self.type is not None: attr.setdefault('type', self.type)
        if self.typemustmatch is not None: attr.setdefault('typemustmatch', self.typemustmatch)
        if self.usemap is not None: attr.setdefault('usemap', self.usemap) if self.usemap[
                                                                                  0] == '#' else attr.setdefault(
            'usemap', '#' + self.usemap)

        super().__init__('object', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class OL(Element):
    """Represents an HTML OL Element;
    Defines an ordered list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword reversed: Bool; Specifies that the list order should be reversed (9,8,7...). (default: False)
    :keyword start: Float; Specifies the start value of an ordered list. (default: None)
    :keyword HTMLtype: OL.Type; Specifies the kind of marker to use in the list. (default: OL.Type.DECIMAL) """

    class Type(CustomEnum):
        DECIMAL = '1'  # Default. Decimal numbers (1, 2, 3, 4)
        ALPHA_LOWERCASE = 'a'  # Alphabetically ordered list, lowercase (a, b, c, d)
        ALPHA_UPPERCASE = 'A'  # Alphabetically ordered list, uppercase (A, B, C, D)
        ROMAN_LOWERCASE = 'i'  # Roman numbers, lowercase (i, ii, iii, iv)
        ROMAN_UPPERCASE = 'I'  # Roman numbers, uppercase (I, II, III, IV)

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.reversed: bool = kwargs.get('reversed',
                                         False)  # Specifies that the list order should be reversed (9,8,7...)
        self.start: float = kwargs.get('start', None)  # Specifies the start value of an ordered list
        self.type: OL.Type = kwargs.get('HTMLtype', OL.Type.DECIMAL)  # Specifies the kind of marker to use in the list

        if self.reversed: attr.setdefault('reversed', None)
        if self.start is not None: attr.setdefault('start', self.start)
        if self.type is not None and self.type in OL.Type.__members__.values(): attr.setdefault('type',
                                                                                                OL.Type[self.type.name])

        super().__init__('ol', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class OptGroup(Element):
    """Represents an HTML OptGroup Element;
    Defines a group of related options in a drop-down list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword disabled: Bool; Specifies that an option-group should be disabled. (default: False)
    :keyword label: Str; Specifies a label for an option-group. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that an option-group should be disabled
        self.label: str = kwargs.get('label', None)  # Specifies a label for an option-group

        if self.disabled: attr.setdefault('disabled', None)
        if self.label is not None: attr.setdefault('label', self.label)

        super().__init__('optgroup', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Option(Element):
    """Represents an HTML Option Element;
    Defines an option in a drop-down list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword disabled: Bool; Specifies that an option should be disabled. (default: False)
    :keyword label: Str; Specifies a shorter label for an option. (default: None)
    :keyword selected: Bool; Specifies that an option should be pre-selected when the page loads. (default: False)
    :keyword value: Str; Specifies the value to be sent to a server. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that an option should be disabled
        self.label: str = kwargs.get('label', None)  # Specifies a shorter label for an option
        self.selected: bool = kwargs.get('selected', False)  # Specifies that an option should be pre-selected when the page loads
        self.value: any = kwargs.get('value', None)  # Specifies the value to be sent to a server

        if self.disabled: attr.setdefault('disabled', None)
        if self.label is not None: attr.setdefault('label', self.label)
        if self.selected: attr.setdefault('selected', None)
        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('option', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Output(Element):
    """Represents an HTML Output Element;
    Defines the result of a calculation.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword HTMLfor: Str; Specifies the relationship between the result of the calculation, and the elements used in the calculation. (default: None)
    :keyword form: Str; Specifies which form the output element belongs to. (default: None)
    :keyword name: Str; Specifies a name for the output element. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.HTMLfor: str = kwargs.get('HTMLfor',
                                       None)  # Specifies the relationship between the result of the calculation, and the elements used in the calculation
        self.form: str = kwargs.get('form', None)  # Specifies which form the output element belongs to
        self.name: str = kwargs.get('name', None)  # Specifies a name for the output element

        if self.HTMLfor is not None: attr.setdefault('for', self.HTMLfor)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.name is not None: attr.setdefault('name', self.name)

        super().__init__('output', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class P(Element):
    """Represents an HTML P Element;
    Defines a paragraph.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('p', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Param(Element):
    """Represents an HTML Param Element;
    Defines a parameter for an object.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword name: Str; Specifies the name of a parameter. (default: None)
    :keyword value: Str; Specifies the value of the parameter. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.name: str = kwargs.get('name', None)  # Specifies the name of a parameter
        self.value: str = kwargs.get('value', None)  # Specifies the value of the parameter

        if self.name is not None: attr.setdefault('name', self.name)
        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('param', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Picture(Element):
    """Represents an HTML Picture Element;
    Defines a container for multiple image resources.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('picture', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Pre(Element):
    """Represents an HTML Pre Element;
    Defines preformatted text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('pre', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Progress(Element):
    """Represents an HTML Progress Element;
    Represents the progress of a task.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword max: Float; Specifies how much work the task requires in total. Default value is 1. (default: 1.0)
    :keyword value: Float; Specifies how much of the task has been completed. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.max: float = kwargs.get('max',
                                     1.0)  # Specifies how much work the task requires in total. Default value is 1
        self.value: float = kwargs.get('value', None)  # Specifies how much of the task has been completed

        if self.max is not None: attr.setdefault('max', self.max)
        if self.value is not None: attr.setdefault('value', self.value)

        super().__init__('progress', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Q(Element):
    """Represents an HTML Q Element;
    Defines a short quotation.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword cite: Str; Specifies the source URL of the quote. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.cite: str = kwargs.get('cite', None)  # Specifies the source URL of the quote

        if self.cite is not None: attr.setdefault('cite', self.cite)

        super().__init__('q', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class RP(Element):
    """Represents an HTML RP Element;
    Defines what to show in browsers that do not support ruby annotations.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('rp', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class RT(Element):
    """Represents an HTML RT Element;
    Defines an explanation/pronunciation of characters (for East Asian typography).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('rt', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Ruby(Element):
    """Represents an HTML Ruby Element;
    Defines a ruby annotation (for East Asian typography).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('ruby', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class S(Element):
    """Represents an HTML S Element;
    Defines text that is no longer correct.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('s', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Samp(Element):
    """Represents an HTML Samp Element;
    Defines sample output from a computer program.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('samp', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Script(Element):
    """Represents an HTML Script Element;
    Defines a client-side script.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword htmlasync: Bool; Specifies that the script is downloaded in parallel to parsing the page, and executed as soon as it is available (before parsing completes) (only for external scripts). (default: False)
    :keyword crossorigin: Script.CrossOrigin; Sets the mode of the request to an HTTP CORS Request. (default: None)
    :keyword defer: Bool; Specifies that the script is downloaded in parallel to parsing the page, and executed after the page has finished parsing (only for external scripts). (default: False)
    :keyword integrity: Str; Allows a browser to check the fetched script to ensure that the code is never loaded if the source has been manipulated. (default: None)
    :keyword nomodule: Bool; Specifies that the script should not be executed in browsers supporting ES2015 modules. (default: None)
    :keyword referrerpolicy: Script.ReferrerPolicy; Specifies which referrer information to send when fetching a script. (default: None)
    :keyword src: Str; Specifies the URL of an external script file. (default: None)
    :keyword HTMLtype: Str; Specifies the media type of the script. (default: None) """

    class CrossOrigin(CustomEnum):
        ANONYMOUS = 'anonymous'
        USE_CREDENTIALS = 'use-credentials'

    class ReferrerPolicy(CustomEnum):
        NO_REFERRER = 'no-referrer'
        NO_REFERRER_DOWNGRADE = 'no-referrer-when-downgrade'
        ORIGIN = 'origin'
        ORIGIN_CROSS_ORIGIN = 'origin-when-cross-origin'
        SAME_ORIGIN = 'same-origin'
        STRICT_ORIGIN = 'strict-origin'
        STRICT_ORIGIN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
        UNSAFE_URL = 'unsafe-url'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.htmlasync: bool = kwargs.get('HTMLasync',
                                          False)  # Specifies that the script is downloaded in parallel to parsing the page, and executed as soon as it is available (before parsing completes) (only for external scripts)
        self.crossorigin: Script.CrossOrigin = kwargs.get('crossorigin',
                                                          None)  # Sets the mode of the request to an HTTP CORS Request
        self.defer: bool = kwargs.get('defer',
                                      False)  # Specifies that the script is downloaded in parallel to parsing the page, and executed after the page has finished parsing (only for external scripts)
        self.integrity: str = kwargs.get('integrity',
                                         None)  # Allows a browser to check the fetched script to ensure that the code is never loaded if the source has been manipulated
        self.nomodule: bool = kwargs.get('nomodule',
                                         None)  # Specifies that the script should not be executed in browsers supporting ES2015 modules
        self.referrerpolicy: Script.ReferrerPolicy = kwargs.get('referrerpolicy',
                                                                None)  # Specifies which referrer information to send when fetching a script
        self.src: str = kwargs.get('src', None)  # Specifies the URL of an external script file
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the media type of the script

        if self.htmlasync: attr.setdefault('async', None)
        if self.crossorigin is not None and self.crossorigin in Script.CrossOrigin.__members__.values(): attr.setdefault(
            'crossorigin', Script.CrossOrigin[self.crossorigin.name])
        if self.defer: attr.setdefault('defer', None)
        if self.integrity is not None: attr.setdefault('integrity', self.integrity)
        if self.nomodule is not None: attr.setdefault('nomodule', self.nomodule)
        if self.referrerpolicy is not None and self.referrerpolicy in Script.ReferrerPolicy.__members__.values(): attr.setdefault(
            'referrerpolicy', Script.ReferrerPolicy[self.referrerpolicy.name])
        if self.src is not None: attr.setdefault('src', self.src)
        if self.HTMLtype is not None: attr.setdefault('type', self.HTMLtype)

        super().__init__('script', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Section(Element):
    """Represents an HTML Section Element;
    Defines a section in a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('section', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Select(Element):
    """Represents an HTML Select Element;
    Defines a drop-down list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword autofocus: Bool; Specifies that the drop-down list should automatically get focus when the page loads. (default: False)
    :keyword disabled: Bool; Specifies that a drop-down list should be disabled. (default: False)
    :keyword form: Str; Defines which form the drop-down list belongs to. (default: None)
    :keyword multiple: Bool; Specifies that multiple options can be selected at once. (default: False)
    :keyword name: Str; Defines a name for the drop-down list. (default: None)
    :keyword required: Bool; Specifies that the user is required to select a value before submitting the form. (default: False)
    :keyword size: Int; Defines the number of visible options in a drop-down list. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.autofocus: bool = kwargs.get('autofocus',
                                          False)  # Specifies that the drop-down list should automatically get focus when the page loads
        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that a drop-down list should be disabled
        self.form: str = kwargs.get('form', None)  # Defines which form the drop-down list belongs to
        self.multiple: bool = kwargs.get('multiple', False)  # Specifies that multiple options can be selected at once
        self.name: str = kwargs.get('name', None)  # Defines a name for the drop-down list
        self.required: bool = kwargs.get('required',
                                         False)  # Specifies that the user is required to select a value before submitting the form
        self.size: int = kwargs.get('size', None)  # Defines the number of visible options in a drop-down list

        if self.autofocus: attr.setdefault('autofocus', None)
        if self.disabled: attr.setdefault('disabled', None)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.multiple: attr.setdefault('multiple', None)
        if self.name is not None: attr.setdefault('name', self.name)
        if self.required: attr.setdefault('required', None)
        if self.size is not None: attr.setdefault('size', self.size)

        super().__init__('select', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Small(Element):
    """Represents an HTML Small Element;
    Defines smaller text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('small', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Source(Element):
    """Represents an HTML Source Element;
    Defines multiple media resources for media elements (<video> and <audio>).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword media: Str; Accepts any valid media query that would normally be defined in a CSS. (default: None)
    :keyword sizes: Str; Specifies image sizes for different page layouts. (default: None)
    :keyword src: Str; Required when source is used in audio and video. Specifies the URL of the media file. (default: None)
    :keyword srcset: Str; Required when <source> is used in <picture>. Specifies the URL of the image to use in different situations. (default: None)
    :keyword HTMLtype: Str; Specifies the MIME-type of the resource. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.media: str = kwargs.get('media',
                                     None)  # Accepts any valid media query that would normally be defined in a CSS
        self.sizes: str = kwargs.get('sizes', None)  # Specifies image sizes for different page layouts
        self.src: str = kwargs.get('src',
                                   None)  # Required when source is used in audio and video. Specifies the URL of the media file
        self.srcset: str = kwargs.get('srcset',
                                      None)  # Required when source is used in picture. Specifies the URL of the image to use in different situations
        self.HTMLtype: str = kwargs.get('HTMLtype', None)  # Specifies the MIME-type of the resource

        if self.media is not None: attr.setdefault('media', self.media)
        if self.sizes is not None: attr.setdefault('sizes', self.sizes)
        if self.src is not None: attr.setdefault('src', self.src)
        if self.srcset is not None: attr.setdefault('srcset', self.srcset)
        if self.type is not None: attr.setdefault('type', self.type)

        super().__init__('source', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Span(Element):
    """Represents an HTML Span Element;
    Defines a section in a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('span', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Strong(Element):
    """Represents an HTML Strong Element;
    Defines important text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('strong', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Style(Element):
    """Represents an HTML Style Element;
    Defines style information for a document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword media: Str; Specifies what media/device the media resource is optimized for. (default: None)
    :keyword HTMLtype: Style.Type; Specifies the media type of the style tag. (default: None) """

    class Type(CustomEnum):
        TEXT_CSS = 'text/css'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.media: str = kwargs.get('media', None)  # Specifies what media/device the media resource is optimized for
        self.type: Style.Type = kwargs.get('HTMLtype', None)  # Specifies the media type of the <style> tag

        if self.media is not None: attr.setdefault('media', self.media)
        if self.type is not None and self.type in Style.Type.__members__.values(): attr.setdefault('type', Style.Type[
            self.type.name])

        super().__init__('style', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Sub(Element):
    """Represents an HTML Sub Element;
    Defines subscripted text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('sub', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Summary(Element):
    """Represents an HTML Summary Element;
    Defines a visible heading for a <details> element.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('summary', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Sup(Element):
    """Represents an HTML Sup Element;
    Defines superscripted text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('sup', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class SVG(Element):
    """Represents an HTML SVG Element;
    Defines a container for SVG graphics.
    WIP - WILL ADD EASY SVG GRAPHIC CREATION OPTIONS SOON

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('svg', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Table(Element):
    """Represents an HTML Table Element;
    Defines a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('table', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TBody(Element):
    """Represents an HTML TBody Element;
    Groups the body content in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('tbody', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TD(Element):
    """Represents an HTML TD Element;
    Defines a cell in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword colspan: Int; Specifies the number of columns a cell should span. (default: None)
    :keyword headers: Str; Specifies one or more header cells a cell is related to. (default: None)
    :keyword rowspan: Int; Sets the number of rows a cell should span. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.colspan: int = kwargs.get('colspan', None)  # Specifies the number of columns a cell should span
        self.headers: str = kwargs.get('headers', None)  # Specifies one or more header cells a cell is related to
        self.rowspan: int = kwargs.get('rowspan', None)  # Sets the number of rows a cell should span

        if self.colspan is not None: attr.setdefault('colspan', self.colspan)
        if self.headers is not None: attr.setdefault('headers', self.headers)
        if self.rowspan is not None: attr.setdefault('rowspan', self.rowspan)

        super().__init__('td', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Template(Element):
    """Represents an HTML Template Element;
    Defines a container for content that should be hidden when the page loads.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('template', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TextArea(Element):
    """Represents an HTML TextArea Element;
    Defines a multiline input control (text area).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword autofocus: Bool; Specifies that a text area should automatically get focus when the page loads. (default: False)
    :keyword cols: Int; Specifies the visible width of a text area. (default: None)
    :keyword rows: Int; Specifies the visible number of lines in a text area. (default: None)
    :keyword dirname: Str; Specifies that the text direction of the textarea will be submitted. (default: None)
    :keyword disabled: Bool; Specifies that a text area should be disabled. (default: False)
    :keyword form: Str; Specifies which form the text area belongs to. (default: None)
    :keyword maxlength: Int; Specifies the maximum number of characters allowed in the text area. (default: None)
    :keyword name: Str; Specifies a name for a text area. (default: None)
    :keyword placeholder: Str; Specifies a short hint that describes the expected value of a text area. (default: None)
    :keyword readonly: Bool; Specifies that a text area should be read-only. (default: False)
    :keyword required: Bool; Specifies that a text area is required/must be filled out. (default: False)
    :keyword wrap: TextArea.Wrap; Specifies how the text in a text area is to be wrapped when submitted in a form. (default: None) """

    class Wrap(CustomEnum):
        HARD = 'hard'
        SOFT = 'soft'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.autofocus: bool = kwargs.get('autofocus',
                                          False)  # Specifies that a text area should automatically get focus when the page loads
        self.cols: int = kwargs.get('cols', None)  # Specifies the visible width of a text area
        self.rows: int = kwargs.get('rows', None)  # Specifies the visible number of lines in a text area
        self.dirname: str = kwargs.get('dirname',
                                       None)  # Specifies that the text direction of the textarea will be submitted
        self.disabled: bool = kwargs.get('disabled', False)  # Specifies that a text area should be disabled
        self.form: str = kwargs.get('form', None)  # Specifies which form the text area belongs to
        self.maxlength: int = kwargs.get('maxlength',
                                         None)  # Specifies the maximum number of characters allowed in the text area
        self.name: str = kwargs.get('name', None)  # Specifies a name for a text area
        self.placeholder: str = kwargs.get('placeholder',
                                           None)  # Specifies a short hint that describes the expected value of a text area
        self.readonly: bool = kwargs.get('readonly', False)  # Specifies that a text area should be read-only
        self.required: bool = kwargs.get('required', False)  # Specifies that a text area is required/must be filled out
        self.wrap: TextArea.Wrap = kwargs.get('wrap',
                                              None)  # Specifies how the text in a text area is to be wrapped when submitted in a form

        if self.autofocus: attr.setdefault('autofocus', None)
        if self.cols is not None: attr.setdefault('cols', self.cols)
        if self.rows is not None: attr.setdefault('rows', self.rows)
        if self.dirname is not None: attr.setdefault('dirname', self.dirname if self.dirname[
                                                                                -4:-1] == '.dir' else self.dirname + '.dir')
        if self.disabled: attr.setdefault('disabled', None)
        if self.form is not None: attr.setdefault('form', self.form)
        if self.maxlength is not None: attr.setdefault('maxlength', self.maxlength)
        if self.name is not None: attr.setdefault('name', self.name)
        if self.placeholder is not None: attr.setdefault('placeholder', self.placeholder)
        if self.readonly: attr.setdefault('readonly', None)
        if self.required: attr.setdefault('required', None)
        if self.wrap is not None and self.wrap in TextArea.Wrap.__members__.values(): attr.setdefault('wrap',
                                                                                                      TextArea.Wrap[
                                                                                                          self.wrap.name])

        super().__init__('textarea', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TFoot(Element):
    """Represents an HTML TFoot Element;
    Groups the footer content in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('tfoot', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TH(Element):
    """Represents an HTML TH Element;
    Defines a header cell in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword abbr: Str; Specifies an abbreviated version of the content in a header cell. (default: None)
    :keyword colspan: Int; Specifies the number of columns a header cell should span. (default: None)
    :keyword headers: Str; Specifies one or more header cells a cell is related to. (default: None)
    :keyword rowspan: Int; Specifies the number of rows a header cell should span. (default: None)
    :keyword scope: TH.Scope; Specifies whether a header cell is a header for a column, row, or group of columns or rows. (default: None) """

    class Scope(CustomEnum):
        COL = 'col'
        COLGROUP = 'colgroup'
        ROW = 'row'
        ROWGROUP = 'rowgroup'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.abbr: str = kwargs.get('abbr', None)  # Specifies an abbreviated version of the content in a header cell
        self.colspan: int = kwargs.get('colspan', None)  # Specifies the number of columns a header cell should span
        self.headers: str = kwargs.get('headers', None)  # Specifies one or more header cells a cell is related to
        self.rowspan: int = kwargs.get('rowspan', None)  # Specifies the number of rows a header cell should span
        self.scope: TH.Scope = kwargs.get('scope',
                                          None)  # Specifies whether a header cell is a header for a column, row, or group of columns or rows

        if self.abbr is not None: attr.setdefault('abbr', self.abbr)
        if self.colspan is not None: attr.setdefault('colspan', self.colspan)
        if self.headers is not None: attr.setdefault('headers', self.headers)
        if self.rowspan is not None: attr.setdefault('rowspan', self.rowspan)
        if self.scope is not None and self.scope in TH.Scope.__members__.values(): attr.setdefault('scope', TH.Scope[
            self.scope.name])

        super().__init__('th', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class THead(Element):
    """Represents an HTML THead Element;
    Groups the header content in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('thead', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Time(Element):
    """Represents an HTML Time Element;
    Defines a specific time (or datetime).

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword datetime: Str; Represents a machine-readable format of the time element. (default: None) """

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.datetime: str = kwargs.get('datetime', None)  # Represents a machine-readable format of the <time> element

        if self.datetime is not None: attr.setdefault('datetime', self.datetime)

        super().__init__('time', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Title(Element):
    """Represents an HTML Title Element;
    Defines a title for the document.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('title', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class TR(Element):
    """Represents an HTML TR Element;
    Defines a row in a table.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('tr', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Track(Element):
    """Represents an HTML Track Element;
    Defines text tracks for media elements (<video> and <audio>).

    :param src: Str; Required. Specifies the URL of the track file.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword default: Bool; Specifies that the track is to be enabled if the user's preferences do not indicate that another track would be more appropriate. (default: False)
    :keyword kind: Track.Kind; Specifies the kind of text track. (default: None)
    :keyword label: Str; Specifies the title of the text track. (default: None)
    :keyword srclang: Str; Specifies the language of the track text data (required if kind="subtitles"). (default: None) """

    class Kind(CustomEnum):
        CAPTIONS = 'captions'
        CHAPTERS = 'chapters'
        DESCRIPTIONS = 'descriptions'
        METADATA = 'metadata'
        SUBTITLES = 'subtitles'

    def __init__(self, src: str, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.default: bool = kwargs.get('default',
                                        False)  # Specifies that the track is to be enabled if the user's preferences do not indicate that another track would be more appropriate
        self.kind: Track.Kind = kwargs.get('kind', None)  # Specifies the kind of text track
        self.label: str = kwargs.get('label', None)  # Specifies the title of the text track
        self.src: str = src  # Required. Specifies the URL of the track file
        self.srclang: str = kwargs.get('srclang',
                                       None)  # Specifies the language of the track text data (required if kind="subtitles")

        if self.default: attr.setdefault('default', None)
        if self.kind is not None and self.kind in Track.Kind.__members__.values(): attr.setdefault('kind', Track.Kind[
            self.kind.name])
        if self.label is not None: attr.setdefault('label', self.label)
        if self.kind == Track.Kind.SUBTITLES:
            attr.setdefault('src', self.srclang)
        elif self.srclang is not None:
            attr.setdefault('src', self.srclang)

        super().__init__('track', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class U(Element):
    """Represents an HTML U Element;
    Defines some text that is unarticulated and styled differently from normal text.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('u', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class UL(Element):
    """Represents an HTML UL Element;
    Defines an unordered list.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('ul', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Var(Element):
    """Represents an HTML Var Element;
    Defines a variable.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('var', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class Video(Element):
    """Represents an HTML Video Element;
    Defines embedded video content.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)

    :keyword autoplay: Bool; Specifies that the video will start playing as soon as it is ready. (default: False)
    :keyword controls: Bool; Specifies that video controls should be displayed (such as a play/pause button etc). (default: False)
    :keyword height: Float; Sets the height of the video player. (default: None)
    :keyword width: Float; Sets the width of the video player. (default: None)
    :keyword loop: Bool; Specifies that the video will start over again, every time it is finished. (default: False)
    :keyword muted: Bool; Specifies that the audio output of the video should be muted. (default: False)
    :keyword poster: Str; Specifies an image to be shown while the video is downloading, or until the user hits the play button. (default: None)
    :keyword preload: Video.Preload; Specifies if and how the author thinks the video should be loaded when the page loads. (default: None)
    :keyword src: Str; Specifies the URL of the video file. (default: None) """

    class Preload(CustomEnum):
        AUTO = 'auto'
        METADATA = 'metadata'
        NONE = 'none'

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        self.autoplay: bool = kwargs.get('autoplay',
                                         False)  # Specifies that the video will start playing as soon as it is ready
        self.controls: bool = kwargs.get('controls',
                                         False)  # Specifies that video controls should be displayed (such as a play/pause button etc).
        self.height: float = kwargs.get('height', None)  # Sets the height of the video player
        self.width: float = kwargs.get('width', None)  # Sets the width of the video player
        self.loop: bool = kwargs.get('loop',
                                     False)  # Specifies that the video will start over again, every time it is finished
        self.muted: bool = kwargs.get('muted', False)  # Specifies that the audio output of the video should be muted
        self.poster: str = kwargs.get('poster',
                                      None)  # Specifies an image to be shown while the video is downloading, or until the user hits the play button
        self.preload: Video.Preload = kwargs.get('preload',
                                                 None)  # Specifies if and how the author thinks the video should be loaded when the page loads
        self.src: str = kwargs.get('src', None)  # Specifies the URL of the video file

        if self.autoplay: attr.setdefault('autoplay', None)
        if self.controls: attr.setdefault('controls', None)
        if self.height is not None: attr.setdefault('height', self.height)
        if self.width is not None: attr.setdefault('width', self.width)
        if self.loop: attr.setdefault('loop', None)
        if self.muted: attr.setdefault('muted', None)
        if self.poster is not None: attr.setdefault('poster', self.poster)
        if self.preload is not None and self.preload in Video.Preload.__members__.values(): attr.setdefault(
            Video.Preload[self.preload.name])
        if self.src is not None: attr.setdefault('src', self.src)

        super().__init__('video', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)


class WBR(Element):
    """Represents an HTML WBR Element;
    Defines a possible line-break.

    :keyword attr: Attributes Dictionary that places items as an attribute in an Element. (default: {})
    :keyword html: Str to override object's generated HTML value. Does not update the rest of the object to reflect HTML str. (default: None)"""

    def __init__(self, items: list = None, **kwargs):
        attr: dict = kwargs.get('attr', {})
        html: str = kwargs.get('html', None)

        super().__init__('wbr', attr=attr, html=html, end_tag=True)
        if items is not None: self.set_items(items)
