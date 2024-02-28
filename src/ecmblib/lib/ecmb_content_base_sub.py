#####################################################################
# File: ecmb_content_base_sub.py
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

from __future__ import annotations
from io import BytesIO
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase
from .ecmb_content_image import ecmbContentImage

class ecmbContentBaseSub(ecmbContentBase):

    _contents = None
    
    def add_image(self, src_or_image: str|BytesIO|ecmbContentImage, unique_id: str = None) -> ecmbContentImage:
        """add_image

        Adds/creates an image
        
        :note:
        * provide a unique-id if you want to access this image easily later at navigation
        * if you add a previously created ecmbContentImage all other parameters are ignored

        :param src_or_image: an image (single-page or double-page) or a previously created ecmbContentImage
        :type src_or_image: str | BytesIO | ecmbContentImage
        :param unique_id: provide a unique-id if you want to access this image easily later at navigation
        :type unique_id: str, optional

        :rtype: ecmbContentImage
        """
        image_obj = None
        if type(src_or_image) == ecmbContentImage:
            image_obj = src_or_image
        elif type(src_or_image) == BytesIO or type(src_or_image) == str:
            image_obj = ecmbContentImage(self._book_obj, src_or_image, unique_id)     
        else:
            ecmbUtils.raise_exception('please provide ecmbContentImage, BytesIO or a path to an existing image-file!')
        
        image_obj.int_set_parent(self)
        self._contents.append(image_obj)

        return image_obj


    def add_folder(self, uid_or_folder: str|ecmbContentFolder = None) -> ecmbContentFolder:
        """add_folder 
        
        Adds/creates an (sub-)folder. If you want to use chapters (and subchapters) in navigation you have to organize the images in folders, coz a chapter points to a folder.

        :note:
        * because the class will generate internal names no name is necesary
        * provide a unique-id if you want to access this folder easily later at navigation

        :param uid_or_folder: an unique-id or a previously created ecmbContentFolder
        :type uid_or_folder: str | ecmbContentFolder, optional
        
        :rtype: ecmbContentFolder
        """        
        folder_obj = None

        if type(uid_or_folder) == ecmbContentFolder:
            folder_obj = uid_or_folder
        elif type(uid_or_folder) == str or uid_or_folder == None:
            folder_obj = ecmbContentFolder(self._book_obj, uid_or_folder)
        else:
            ecmbUtils.raise_exception('please provide ecmbContentFolder, a unique_id or None!')
            
        folder_obj.int_set_parent(self)
        self._contents.append(folder_obj)

        return folder_obj
    

    def int_contains(self, obj: ecmbContentBase) -> bool:
        unique_id = obj.get_unique_id()
        for content in self._contents:
            if unique_id == content.get_unique_id() or (type(content) != ecmbContentImage and content.int_contains(obj)):
                return True
        return False



# for type-hinting and and type-check in combination with "from __future__ import annotations"
# can't include them on top coz these ar subclasses of ecmbNavigationBaseSub
from .ecmb_content_folder import ecmbContentFolder


        
