import zipfile, os, re, shutil
from lxml import etree
from typing import Callable

from .lib.ecmb_enums import *
from .lib.ecmb_utils import ecmbUtils, ecmbException

from .lib.ecmb_metadata import ecmbMetaData
from .lib.ecmb_metadata_based_on import ecmbMetaDataBasedOn

from .lib.ecmb_content import ecmbContent
from .lib.ecmb_content_folder import ecmbContentFolder
from .lib.ecmb_content_image import ecmbContentImage

from .lib.ecmb_navigation import ecmbNavigation
from .lib.ecmb_navigation_headline import ecmbNavigationHeadline
from .lib.ecmb_navigation_chapter import ecmbNavigationChapter
from .lib.ecmb_navigation_item import ecmbNavigationItem

from .ecmb_definition.validator.python.ecmb_validator import ecmbValidator

class ecmbBook:

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

    def __init__(self, book_type: BOOK_TYPE, language: str, uid: str, width: int, height: int):  
        book_type = ecmbUtils.enum_value(book_type)
        
        ecmbUtils.validate_enum(True, 'book_type', book_type, BOOK_TYPE)
        ecmbUtils.validate_regex(True, 'language', language, r'^[a-z]{2}$')
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


    def get_metadata(self) -> ecmbMetaData:
        return self._metadata_obj
    
    metadata: ecmbMetaData = property(get_metadata) 

    
    def get_based_on(self) -> ecmbMetaDataBasedOn:
        return self._metadata_obj.based_on
    
    based_on: ecmbMetaDataBasedOn = property(get_based_on) 

    
    def get_content(self) -> ecmbContent:
        return self._content_obj
    
    content: ecmbContent = property(get_content) 


    def get_navigation(self) -> ecmbNavigation:
        return self._navigation_obj
    
    navigation: ecmbNavigation = property(get_navigation) 


    def write(self, file_name: str, warnings: bool|Callable = True, demo_mode: bool = False) -> None:

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
    