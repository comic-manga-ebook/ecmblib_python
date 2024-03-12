"""
 File: ecmb_validator.py
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

import re, os, yaml, io, zipfile, path
from typing import Callable
from lxml import etree
from PIL import ImageFile
import datetime

class ecmbValidator():

    _validator_path = None
    _schema_location = None
    _error_callback = None
    _is_valid = None

    _xml_image_width = None
    _xml_image_height = None

    _xml_navigation = None
    _xml_content = None
    _xml_files_list = None

    def __init__(self, error_callback: Callable = None):

        self._validator_path = path.Path(__file__).abspath().parent + '/'
        self.error_callback = error_callback
        self._load_config()
        

    def validate(self, file_name: str) -> bool:
        return self._validate(file_name, False)
    

    def validate_fast(self, file_name: str) -> bool:
        return self._validate(file_name, True)
    

    def _validate(self, file_name: str, fast: bool) -> bool:
        self._is_valid = True

        if not os.path.isfile(file_name):
            self._write_error('File not found!')
        else: 
            if re.search(r'\.xml$', file_name, re.IGNORECASE):
                with open(file_name, 'rb') as f:
                    xml_content = f.read()
                self._validate_xml(xml_content)
            elif re.search(r'\.ecmb$', file_name, re.IGNORECASE):
                self._validate_ecmb(file_name, fast)
            else:
                self._write_error('Unknown file-type!')
        
        return self._is_valid
        

    def _validate_ecmb(self, file_name: str, fast: bool) -> bool:
        if not zipfile.is_zipfile(file_name):
            self._write_error('Invalid eCMB-File!')
            return False

        try:
            ecmb_file = zipfile.ZipFile(file_name, 'r')
        except:
            self._write_error('Faild to open eCMB-File!')
            return False
        
        zip_file_list = ecmb_file.namelist()
        
        if not 'ecmb.xml' in zip_file_list:
            self._write_error('ecmb.xml is missing!')
            return False

        with ecmb_file.open('ecmb.xml', 'r') as f:
            xml_content = f.read()

        if not self._validate_xml(xml_content):
            return False
        
        for xml_file in self._xml_files_list:
            xml_file_name = xml_file[0][1:]
            double_allowed = True if xml_file[1] else False

            if not xml_file_name in zip_file_list:
                self._write_error(f'"/{xml_file_name}" is missing!')
            elif not fast:
                image_size = self._get_image_size(ecmb_file, xml_file_name)
                if not image_size:
                    self._write_error(f'Faild to get image-size from "/{xml_file_name}"!')
                
                is_double = (image_size[0] / image_size[1]) > (self._xml_image_width / self._xml_image_height * 1.5)
                
                if double_allowed != is_double:
                    self._write_error(f'Image "/{xml_file_name}" has wrong size!')
        
        return True


    def _get_image_size(self, ecmb_file: zipfile.ZipFile, file_name: str) -> tuple[int, int]:
        with ecmb_file.open(file_name, "r") as f:
            parser = ImageFile.Parser()
            chunk = f.read(2048)
            count=2048
            while chunk != "":
                parser.feed(chunk)
                if parser.image:
                    return parser.image.size
                chunk = f.read(2048)
                count+=2048
            

    def _validate_xml(self, xml_content: str) -> bool:
        root = self._load_xml(xml_content)
        if root == None:
            return False
        
        self._xml_image_width = int(root.get('width'))
        self._xml_image_height = int(root.get('height'))

        for publishdate in root.iter('publishdate'):
            self._validate_date(publishdate.text)
        
        self._xml_navigation = []
        self._xml_content = []
        self._xml_files_list = []
        
        content = root.find('content')
        self._read_xml_content(content, '/content')

        if content.get('cover_front'):
            self._xml_files_list.append(('/'+content.get('cover_front'), False))

        if content.get('cover_rear'):
            self._xml_files_list.append(('/'+content.get('cover_rear'), False))

        navigation = root.find('navigation')
        if navigation == None:
            return True
        
        self._read_xml_navigation(navigation)
        for ele in self._xml_navigation:
            if not re.search(r'^/content/[a-z0-9_-]', ele) or not ele in self._xml_content:
                self._write_error(f'Navigation-Target "{ele}" not found!')

        return True
        

    def _read_xml_navigation(self, main_node: etree.Element, path: str = '') -> None:
        for node in main_node:
            match node.tag:
                case 'headline':
                    self._read_xml_navigation(node, path)
                case 'link':
                    self._xml_navigation.append(path + node.get('href'))
                case 'chapter':
                    dir = node.get('dir')
                    self._xml_navigation.append(path + dir)
                    self._xml_navigation.append(path + dir + node.get('href'))
                    self._read_xml_navigation(node, path + dir)


    def _read_xml_content(self, main_node: etree.Element, path: str = '') -> None:
        for node in main_node:
            match node.tag:
                case 'img':
                    src = path + '/' + node.get('src')
                    self._xml_content.append(src)
                    self._xml_files_list.append((src, False))
                case 'dimg':
                    src = path + '/' + node.get('src')
                    self._xml_content.append(src + '#auto')
                    self._xml_content.append(src + '#left')
                    self._xml_content.append(src + '#right')
                    self._xml_files_list.append((src, True))
                case 'dir':
                    name = node.get('name')
                    self._xml_content.append(path + '/' + name)
                    self._read_xml_content(node, path + '/' + name)


    def _load_xml(self, xml_content: str) -> etree.Element:
        try:
            tmp = xml_content.decode(encoding='utf-8').encode(encoding='utf-8')
        except:
            self._write_error('XML contains invalid UTF-8 characters')
            return
        
        try:
            fp = io.BytesIO(xml_content)
            fp.seek(0)
            xml_doc = etree.parse(fp)
            root = xml_doc.getroot()
            ecmb_version = root.get('version')
        except:
            self._write_error('Invalid XML-File!')
            return

        if not ecmb_version or not re.match(r'^[1-9][0-9]*\.[0-9]+$', ecmb_version):
            self._write_error('Invalid eCMB version-number!')
            return

        xsd_path = self._schema_location + f'ecmb-v{ecmb_version}.xsd'

        if not os.path.exists(xsd_path):
            self._write_error(f'XSD with version "{ecmb_version}" not found!')
            return

        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        if not xmlschema.validate(xml_doc):
            self._write_error('eCMB-XML is invalid!')
            return
        
        return root
    

    def _load_config(self) -> None:
        try: 
            with open(self._validator_path + 'ecmb_validator_config.yml', 'r') as file:
                config = yaml.safe_load(file)
            
            schema_location = config['schema_location']
            if not schema_location:
                raise Exception()
        except:
            raise Exception('Config not found or invalid!')
                
        if not re.search(r'[\/\\]$', schema_location):
            schema_location += '/'

        if not re.search(r'[:]', schema_location):
            schema_location = self._validator_path + schema_location
        
        if not os.path.isdir(schema_location):
            raise Exception('Schema-Location not found or not a directory!')
        
        self._schema_location = schema_location
    

    def _validate_date(self, date_text: str) -> None:
        current_year = datetime.date.today().year
        if re.match('^[0-9]{4}$', date_text):
            year = int(date_text)
        else:
            try:
                d = datetime.date.fromisoformat(date_text)
                year = d.year
            except:
                self._write_error("invalid publishdate")
                return
            
        if year < 1900 or year > current_year + 1:
            self._write_error("publishdate has to be between 1900 and " + str(current_year + 1))

    
    def _write_error(self, msg: str) -> None:
        self._is_valid = False
        if self.error_callback and callable(self.error_callback):
            self.error_callback(msg)