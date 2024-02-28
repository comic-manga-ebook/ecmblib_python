#####################################################################
# File: ecmb_enums.py
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

from enum import Enum

class ALLOWED_IMAGE_EXTENTIONS(Enum):
    """ALLOWED_IMAGE_EXTENTIONS 
    
    * JPG = 'jpg'
    * JPEG = 'jpeg'
    * PNG = 'png'
    * WEBP = 'webp'
    """    
    JPG = 'jpg'
    JPEG = 'jpeg'
    PNG = 'png'
    WEBP = 'webp'


class BOOK_TYPE(Enum):
    """BOOK_TYPE 
    
    * MANGA = 'manga'
    * COMIC = 'comic'
    """    
    MANGA = 'manga'
    COMIC = 'comic'


class BASED_ON_TYPE(Enum):
    """BASED_ON_TYPE 

    * NOVEL = 'Novel'
    * LIGHTNOVEL = 'Lightnovel'
    * MANGA = 'Manga'
    * COMIC = 'Comic'
    * ANIME = 'Anime'
    * GAME = 'Game'
    * OTHER ='Other'
    """    
    NOVEL = 'Novel'
    LIGHTNOVEL = 'Lightnovel'
    MANGA = 'Manga'
    COMIC = 'Comic'
    ANIME = 'Anime'
    GAME = 'Game'
    OTHER ='Other'
    

class AUTHOR_ROLE(Enum):
    """AUTHOR_ROLE 
    
    * AUTHOR = 'Author'
    * COAUTHOR = 'Co-Author'
    * STORY = 'Story'
    * ART = 'Art'
    * COLORIST = 'Colorist'
    * COVERARTIST = 'CoverArtist'
    """    
    AUTHOR = 'Author'
    COAUTHOR = 'Co-Author'
    STORY = 'Story'
    ART = 'Art'
    COLORIST = 'Colorist'
    COVERARTIST = 'CoverArtist'


class EDITOR_ROLE(Enum):
    """EDITOR_ROLE 
    
    * TRANSLATOR = 'Translator'
    * SCANNER = 'Scanner'
    """    
    TRANSLATOR = 'Translator'
    SCANNER = 'Scanner'


class CONTENT_WARNING(Enum):
    """CONTENT_WARNING 
    
    * ADULT = 'Adult'
    * MATURE_THEMES = 'Mature Themes'
    * NUDITY = 'Nudity'
    * SEXUAL_CONTENT = 'Sexual Content'
    * EXPLICIT_SEX = 'Explict Sex'
    * HENTAI = 'Hentai'
    * PROSTITUTION = 'Prostitution'
    * INCEST = 'Incest'
    * VIOLENCE = 'Violence'
    * EXPLICIT_VIOLENCE = 'Explicit Violence'
    * TERRORISM = 'Terrorism'
    * EMOTIONAL_ABUSE= 'Emotional Abuse'
    * SEXUAL_ABUSE = 'Sexual Abuse'
    * PHYSICAL_ABUSE = 'Physical Abuse'
    * DOMESTIC_ABUSE = 'Domestic Abuse'
    * SELF_HARM = 'Self-Harm'
    * SUICIDE = 'Suicide'
    * DRUGS = 'Drugs'
    """
    ADULT = 'Adult'
    MATURE_THEMES = 'Mature Themes'
    NUDITY = 'Nudity'
    SEXUAL_CONTENT = 'Sexual Content'
    EXPLICIT_SEX = 'Explict Sex'
    HENTAI = 'Hentai'
    PROSTITUTION = 'Prostitution'
    INCEST = 'Incest'
    VIOLENCE = 'Violence'
    EXPLICIT_VIOLENCE = 'Explicit Violence'
    TERRORISM = 'Terrorism'
    EMOTIONAL_ABUSE= 'Emotional Abuse'
    SEXUAL_ABUSE = 'Sexual Abuse'
    PHYSICAL_ABUSE = 'Physical Abuse'
    DOMESTIC_ABUSE = 'Domestic Abuse'
    SELF_HARM = 'Self-Harm'
    SUICIDE = 'Suicide'
    DRUGS = 'Drugs'


class TARGET_SIDE(Enum):
    """TARGET_SIDE 

    * AUTO = 'auto'
    * LEFT = 'left'
    * RIGHT = 'right'
    """    
    AUTO = 'auto'
    LEFT = 'left'
    RIGHT = 'right'