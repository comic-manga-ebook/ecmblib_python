#####################################################################
# File: ecmb_content_image.py
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

import zipfile
from io import BytesIO
from lxml import etree
from typing import Callable
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase

class ecmbContentImage(ecmbContentBase):
    """ecmbContentImage 
    
    :note:
    * provide a unique-id if you want to access this image easily later at navigation

    :param book_obj:
    :type book_obj: ecmbBook
    :param src: an image (single-page or double-page)
    :type src: str | BytesIO
    :param unique_id: provide a unique-id if you want to access this image easily later at navigation
    :type unique_id: str, optional
    """    

    _src = None
    _src_format = None
    _is_double = None
    
    def __init__(self, book_obj, src: str|BytesIO, unique_id: str = None):
        self._init(book_obj, unique_id)

        msg = 'for image: "' + src + '"' if type(src) == str else 'at unique_id: "' + self._unique_id + '"'

        (is_double, src_format) = self._check_image(src, 'src', True)
            
        self._src = src
        self._src_format = src_format
        self._is_double = is_double


    def int_validate(self, warnings: bool|Callable) -> bool:
        self._book_obj.int_get_next_page_nr()

        if self._is_double:
            page_nr = self._book_obj.int_get_next_page_nr()
            if page_nr % 2 != 0:
                msg = 'image: "' + self._src + '"' if type(self._src ) == str else 'image with the unique_id: "' + self._unique_id + '"'
                ecmbUtils.write_warning(warnings, f'{msg} is on an uneven page!')

        return True
    

    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        self._build_id = self._book_obj.int_get_next_build_id()
        file_path = self.int_get_build_path(False)

        if self._is_double:
            node = etree.Element('dimg')
        else:
            node = etree.Element('img')

        node.set('src', self._build_id + '.' + self._src_format)
        self._write_image(target_file, file_path + '.' + self._src_format, self._src)

        return node
    

    def int_get_image_path(self, target_side: TARGET_SIDE = TARGET_SIDE.AUTO) -> str:
        target_side = ecmbUtils.enum_value(target_side)

        link = self.int_get_build_path()
        link += '.' + self._src_format
        if self._is_double:
            link += '#' + (target_side if target_side else TARGET_SIDE.AUTO.value)

        return link