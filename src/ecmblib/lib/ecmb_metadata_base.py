#####################################################################
# File: ecmb_metadata_base.py
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

from abc import ABC, abstractmethod
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *

class ecmbMetaDataBase(ABC):

    _data = None

    def __init__(self):
       self._data = {}


    def set_isbn(self, isbn: str) -> None:
        """set_isbn

        :param isbn: isbn-10 or isbn-13
        :type isbn: str
        """        
        if isbn != None and isbn != '':
            ecmbUtils.validate_regex(True, 'isbn', isbn, '^([0-9]{10}|[0-9]{13})$')
        self._data['isbn'] = (isbn, {})

    
    def set_publisher(self, publisher: str, href: str = None) -> None:
        """set_publisher 

        :param publisher: the name of the publisher
        :type publisher: str
        :param href: the homepage of the publisher
        :type href: str, optional
        """        
        ecmbUtils.validate_str_or_none(True, 'publisher', publisher)
        if href != None and href != '':
            ecmbUtils.validate_regex(True, 'href', href, '^(http|https)://.+$')
            if not publisher:
                ecmbUtils.raise_exception('publisher is mandatory when link to puslisher is given!')
        self._data['publisher'] = (publisher, {'href': href})


    def set_publishdate(self, publishdate: str) -> None:
        """set_publishdate 

        :param publishdate: the publishe-date of the book (YYYY-MM-DD or YYYY)
        :type publishdate: str 
        """        
        if publishdate != None and publishdate != '':
            ecmbUtils.validate_date(True, 'publishdate', publishdate)
        self._data['publishdate'] = (publishdate, {})
        

    def add_author(self, name: str, role: AUTHOR_ROLE = AUTHOR_ROLE.AUTHOR, href: str = None) -> None:
        """add_author 

        :param name: the name of the author
        :type name: str
        :param role: the role of the author
        :type role: AUTHOR_ROLE, optional
        :param href: the homepage of the author
        :type href: str, optional
        """        
        role = ecmbUtils.enum_value(role)

        ecmbUtils.validate_not_empty_str(True, 'name', name)
        ecmbUtils.validate_enum(True, 'role', role, AUTHOR_ROLE)
        if href != None and href != '':
            ecmbUtils.validate_regex(True, 'href', href, '^(http|https)://.+$')
            
        if not self._data.get('authors'):
            self._data['authors'] = []
        self._data['authors'].append(('author', name, {'role': role, 'href': href}))


    @abstractmethod
    def int_validate(self) -> None:
        pass


    @abstractmethod
    def int_build(self) -> etree.Element:
        pass


    def _build(self, main_node: etree.Element) -> bool:
        found = False
        for node_name, node_data in self._data.items():
            if type(node_data) == list:
                found_list = False
                main_node_list = etree.Element(node_name)
                for list_data in node_data:
                    value = self._clean_value(list_data[1])
                    if value != None:
                        found_list = True
                        etree.SubElement(main_node_list, list_data[0], attrib = self._clean_attributes(list_data[2])).text = value
                if found_list:
                    found = True
                    main_node.append(main_node_list)
            else:
                value = self._clean_value(node_data[0])
                if value != None:
                    found = True
                    etree.SubElement(main_node, node_name, attrib = self._clean_attributes(node_data[1])).text = value
        return found


    def _clean_attributes(self, attributes:dict) -> dict:
        result = {}
        if type(attributes) == dict:
            for attr_name, attr_value in attributes.items():
                attr_value = self._clean_value(attr_value)
                if attr_value != None:
                    result[attr_name] = attr_value
        return result
    

    def _clean_value(self, value) -> str:
       if value != None and value != '':
            if type(value) == bool:
                value = 'true' if value else 'false'
            return str(value)
       return None