#####################################################################
# File: ecmb.py
# Copyright (c) 2023 Clemens K. (https://github.com/metacreature)
# 
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#####################################################################

import zipfile, os, re, shutil 
from lxml import etree
from typing import Callable

from .lib.ecmb_enums import *
from .lib.ecmb_utils import ecmbUtils, ecmbException 

from .lib.ecmb_metadata import ecmbMetaData
from .lib.ecmb_metadata_original import ecmbMetaDataOriginal
from .lib.ecmb_metadata_based_on import ecmbMetaDataBasedOn

from .lib.ecmb_content import ecmbContent
from .lib.ecmb_content_folder import ecmbContentFolder
from .lib.ecmb_content_image import ecmbContentImage

from .lib.ecmb_navigation import ecmbNavigation
from .lib.ecmb_navigation_headline import ecmbNavigationHeadline
from .lib.ecmb_navigation_chapter import ecmbNavigationChapter
from .lib.ecmb_navigation_link import ecmbNavigationLink

from .ecmb_definition.validator.python.ecmb_validator import ecmbValidator

class ecmbBook:
    """
    The main class to genererate `*`.ecmb - files 

    :note: 
    * the title is mandatory, so please call book.metadata.set_title('My Title')
    * the width and height "should" be the size of the images. It not exact, coz when I was building fan-translated Mangas, all images had a different size and aspect-ratio, but the aspect-ratio is enterly important for the validator to validate the correct placement of double-page-images. (Formula: id_double = (img_width / img_height) > (book_width / book_height * 1.5))
    * chapters with an uneven page-count are supported, also double-pages on an uneven page and uneven page-count of the book ... of course you will get a warning
    * All functions in the library will raise an ecmbException on invalid values!

    :param book_type: the book-type defines the reading-direction of the book
    :type book_type: BOOK_TYPE
    :param language: language of the content (ISO 639-1 language-code)
    :type language: str
    :param uid: unique-id of the book (minlength: 16, maxlength:255)
    :type uid: str 
    :param width: approximately width of the images
    :type width: int
    :param height: approximately height of the images
    :type height: int
    """      

    _version = None
    _book_type = None
    _language = None
    _uid = None
    _width = None
    _height = None

    _content_ref = None

    _metadata_obj = None
    _content_obj = None
    _navigation_obj = None
    
    _build_id_counter = None
    _page_nr_counter = None

    def __init__(self, book_type: BOOK_TYPE, language: LANGUAGE_CODE, uid: str, width: int, height: int):
        book_type = ecmbUtils.enum_value(book_type)
        
        ecmbUtils.validate_enum(True, 'book_type', book_type, BOOK_TYPE)
        ecmbUtils.validate_enum(True, 'language', language, LANGUAGE_CODE)
        ecmbUtils.validate_regex(True, 'uid', uid, r'^[a-z0-9_]{16,255}$')
        ecmbUtils.validate_int(True, 'width', width, 100)
        ecmbUtils.validate_int(True, 'height', height, 100)

        self._content_ref = {}

        self._metadata_obj = ecmbMetaData()
        self._content_obj = ecmbContent(self)
        self._navigation_obj = ecmbNavigation(self)

        self._version = '1.0'
        self._book_type = book_type
        self._language = language
        self._uid = uid
        self._width = width
        self._height = height


    @property
    def metadata(self) -> ecmbMetaData:
        """metadata

        You can add the book's meta-data like title, genres, ... to ecmbMetaData

        :rtype: ecmbMetaData
        """         
        return self._metadata_obj


    @property
    def original(self) -> ecmbMetaDataOriginal:
        """
        alias for ecmbMetaData.original

        If the book was (fan-) translated you can add the information for the original book to ecmbMetaDataOriginal.

        :rtype: ecmbMetaDataOriginal
        """        
        return self._metadata_obj.original
    

    @property
    def based_on(self) -> ecmbMetaDataBasedOn:
        '''
        alias for ecmbMetaData.based_on

        If the book based on eg. a light-novel and you want to give that credit, you can add the information to ecmbMetaDataBasedOn

        :rtype: ecmbMetaDataBasedOn
        '''
        return self._metadata_obj.based_on

  
    @property  
    def content(self) -> ecmbContent:
        """content 

        Add folders and images to ecmbContent

        :rtype: ecmbContent
        """        
        return self._content_obj


    @property
    def navigation(self) -> ecmbNavigation:
        """navigation 

        Add Chapters, Headlines or Links to ecmbNavigation

        :rtype: ecmbNavigation
        """    
        return self._navigation_obj


    def write(self, file_name: str, warnings: bool|Callable = True, demo_mode: bool = False) -> None:
        """write 

        :param file_name:
        :type file_name: str
        :param warnings: defines if warnings should be printed to the console or not or alternatively use a callback-function myfunc(msg)
        :type warnings: bool | Callable, optional
        :param demo_mode: in demo-mode the generated file will be automaticaly unszipped
        :type demo_mode: bool, optional
        """        
        self._validate(warnings)
        
        if re.search(r'\.ecmb$', file_name) == None:
            file_name += '.ecmb'

        target_file = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)

        try:
            target_file.writestr('mimetype', 'application/ecmb+zip', compress_type=zipfile.ZIP_STORED)

            root = etree.Element('ecmb')
            root.set('version', self._version)
            root.set('type', self._book_type)
            root.set('language', self._language)
            root.set('uid', self._uid)
            root.set('width', str(self._width))
            root.set('height', str(self._height))

            metadata_node = self._metadata_obj.int_build()
            if metadata_node != None:
                root.append(metadata_node)

            self._build_id_counter = 0
            content_node = self._content_obj.int_build(target_file)
            if content_node != None:
                root.append(content_node)

            navigation_node = self._navigation_obj.int_build()
            if navigation_node != None:
                root.append(navigation_node)

            xml_str = etree.tostring(root, pretty_print=demo_mode, xml_declaration=True, encoding="utf-8")
            target_file.writestr('ecmb.xml', xml_str)

        except Exception as e:
            target_file.close()
            os.remove(file_name) 
            raise e

        target_file.close()

        # validate the result
        validator = ecmbValidator()
        if not validator.validate(file_name):
            os.remove(file_name) 
            ecmbUtils.raise_exception('An Error occured during creation of the file!')

        if demo_mode:
            target_file = zipfile.ZipFile(file_name, 'r')
            if os.path.exists(file_name+'_unpacked'):
                shutil.rmtree(file_name+'_unpacked')
            target_file.extractall(file_name+'_unpacked')
            target_file.close()


    def int_register_content(self, content: ecmbContentFolder|ecmbContentImage) -> None:
        if content.get_unique_id() in self._content_ref.keys():
            ecmbUtils.raise_exception(f'the book contains allready content with the unique_id "' + content.get_unique_id() + '"!', 1)
        self._content_ref[content.get_unique_id()] = content


    def int_get_content(self, ref): # no typehining coz don't want the user to see the class ecmbContentBase
        from .lib.ecmb_content_base import ecmbContentBase
        unique_id = ref.get_unique_id() if isinstance(ref, ecmbContentBase) else ref
        return self._content_ref.get(unique_id)


    def int_get_width(self) -> int:
        return self._width
    

    def int_get_height(self) -> int:
        return self._height
    

    def int_get_next_build_id(self) -> str:
        self._build_id_counter  += 1

        char_map = '0123456789abcdefghijklmnopqrstuvwxyz'

        build_id_int = self._build_id_counter
        build_id_str = ''

        while build_id_int > 0:
            build_id_str = char_map[build_id_int % 36] + build_id_str
            build_id_int = int((build_id_int - (build_id_int % 36))  / 36)
        
        return build_id_str
    

    def int_get_next_page_nr(self) -> int:
        self._page_nr_counter  += 1
        return self._page_nr_counter
    

    def _validate(self, warnings: bool|Callable = True) -> None:
        self._metadata_obj.int_validate()

        self._page_nr_counter = 0
        self._content_obj.int_validate(warnings)
        if self._page_nr_counter % 2 != 0:
            ecmbUtils.write_warning(warnings, f'the Book has an an uneven page-count!')

        self._navigation_obj.int_validate(warnings)
    
