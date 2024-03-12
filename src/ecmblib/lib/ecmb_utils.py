#####################################################################
# File: ecmb_utils.py
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

import re, inspect, datetime
from enum import Enum
from typing import Callable


class ecmbException(Exception):
    pass


class ecmbUtils():
    
    @staticmethod
    def get_caller(stack_nr: int = 0) -> str:
        stack_nr += 1
        try:
            stack = inspect.stack()
            classname = stack[stack_nr][0].f_locals["self"].__class__.__name__
            methodname = stack[stack_nr][0].f_code.co_name
            return f'{classname}.{methodname}():'
        except:
            return ecmbUtils.get_caller(stack_nr +1)
    

    @staticmethod
    def write_warning(warnings: bool|Callable, msg: str, stack_nr: int = 0) -> None:
        caller = ecmbUtils.get_caller(stack_nr + 1)
        if warnings == True:
            print(f'\033[1;33;40m  -- WARNING: {caller} {msg}\033[0m', flush=True)
        elif callable(warnings):
            warnings(f'WARNING: {caller} {msg}')

    
    @staticmethod
    def raise_exception(msg: str, stack_nr: int = 0) -> None:
        caller = ecmbUtils.get_caller(stack_nr + 1)
        raise ecmbException(f'{caller} {msg}')


    @staticmethod
    def enum_value(value) -> str:
        if isinstance(value, Enum):
            return value.value
        return value
		
		
    @staticmethod
    def enum_values(enum_class: Enum) -> list:
        return [e.value for e in enum_class]
    

    @staticmethod
    def validate_utf8(raise_exception: bool, varname: str,  value:str, stack_nr: int = 0) -> bool:
        if type(value) == str and value != '':
            try:
                tmp = value.encode(encoding='utf-8').decode(encoding='utf-8')
            except:
                if raise_exception:
                    ecmbUtils.raise_exception(f'{varname} contains invalid UTF-8 characters!', stack_nr + 1)
                return False
        return True
        

    @staticmethod
    def validate_str_or_none(raise_exception: bool, varname: str,  value, stack_nr: int = 0) -> bool:
        if value != None and type(value) != str:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be a string or None!', stack_nr + 1)
            return False
        return ecmbUtils.validate_utf8(raise_exception, varname,  value, stack_nr + 1)
    

    @staticmethod
    def validate_not_empty_str(raise_exception: bool, varname: str,  value, stack_nr: int = 0) -> bool:
        if type(value) != str or value == '':
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be a not empty string!', stack_nr + 1)
            return False
        return ecmbUtils.validate_utf8(raise_exception, varname,  value, stack_nr + 1)
    

    @staticmethod
    def validate_int(raise_exception: bool, varname: str,  value, min_value: int = None, max_value: int = None, stack_nr: int = 0) -> bool:
        if type(value) != int or (min_value != None and value < min_value) or (max_value != None and value > max_value):
            if raise_exception:
                msg = f'{varname} has to be as integer'
                msg += ' >= ' + str(min_value) if min_value != None else ''
                msg += ' <= ' + str(max_value) if max_value != None else ''
                msg += '!'
                ecmbUtils.raise_exception(msg, stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_enum(raise_exception: bool, varname: str,  value, enum_class: Enum, stack_nr: int = 0) -> bool:
        enum_values = [e.value for e in enum_class]
        if not value or type(value) != str or not value in enum_values:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be one of these values: "'+('", "'.join(enum_values)) +'"!', stack_nr + 1)
            return False
        return True
    
    @staticmethod
    def validate_in_list(raise_exception: bool, varname: str,  value, value_list: list, stack_nr: int = 0) -> bool:
        if value == None or not value in value_list:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be one of these values: "'+('", "'.join(value_list)) +'"!', stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_regex(raise_exception: bool, varname: str,  value, regex: str, stack_nr: int = 0) -> bool:
        if type(value) != str or not re.match(regex, value):
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be as string and match: "{regex}"!', stack_nr + 1)
            return False
        return ecmbUtils.validate_utf8(raise_exception, varname,  value, stack_nr + 1)
    

    @staticmethod
    def validate_date(raise_exception: bool, varname: str,  value:str, stack_nr: int = 0) -> None:
        res = ecmbUtils.validate_regex(raise_exception, varname, value, '^[0-9]{4}(-[0-9]{2}-[0-9]{2})?$', stack_nr + 1)

        if not res:
            return res

        current_year = datetime.date.today().year
        if re.match('^[0-9]{4}$', value):
            year = int(value)
        else:
            try:
                d = datetime.date.fromisoformat(value)
                year = d.year
            except:
                if raise_exception:
                    ecmbUtils.raise_exception(f'{varname} is not a valid date!', stack_nr + 1)
                return False
            
        if year < 1900 or year > current_year + 1:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be between 1900 and ' + str(current_year + 1), stack_nr + 1)
            return False
        
        return True
    