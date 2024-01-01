"""
 File: ecmb_metadata_based_on.py
 Copyright (c) 2023 Clemens K. (https://github.com/metacreature)
 
 MIT License
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *
from .ecmb_metadata_base import ecmbMetaDataBase


class ecmbMetaDataOriginal(ecmbMetaDataBase):

    _msg = None
    _node = None

    def __init__(self):
       super().__init__()
       self._msg = f'if you provide a original-information the title is mandatory! Please use book.original.set_title("My Book Title")'
       self._node = 'original'
    
    def set_language(self, language: str) -> None:
        if language != None and language != '':
            ecmbUtils.validate_regex(True, 'language', language, '^[a-z]{2}$')
        self._data['isbn'] = (language, {})


    def set_title(self, title: str) -> None:
        ecmbUtils.validate_str_or_none(True, 'title', title)
        self._data['title'] = (title, {})
    

    def int_validate(self) -> None:
        found = False
        for value in self._data.values():
            if type(value) == list:
                for list_value in value:
                    if list_value[1] != None and list_value[1] != '':
                        found = True
            else:
                if value[0] != None and value[0] != '':
                    found = True
        if not found:
            return

        title = self._data.get('title')
        title = title[0] if type(title) == tuple else None
        if type(title) != str or title  == '':
            ecmbUtils.raise_exception(self._msg)


    def int_build(self) -> etree.Element:
        self.int_validate()

        found = False
        main_node = etree.Element(self._node)

        if self._build(main_node):
            found = True

        if found:
            return main_node
        return None