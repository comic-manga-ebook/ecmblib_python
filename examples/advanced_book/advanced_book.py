import io
from PIL import Image

# only for relative import if you cloned the project
# you have to delete this if ecmblib is installed as a module
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(str(directory.parent.parent.parent) + '/src/')


from ecmblib import ecmbBook, ecmbException, BOOK_TYPE, AUTHOR_ROLE, CONTENT_WARNING, BASED_ON_TYPE, TARGET_SIDE


print('\n', flush=True)

# create book-obj
###################################################

# book-type, language, unique-id, width of the images, height of the images
# The width and height "should" be the size of the images. 
# It not exact, coz when I was building fan-translated Mangas, all images had a different size and aspect-ratio, 
# but the aspect-ratio is enterly important for the validator to validate the correct placement of double-page-images.
# Formula: id_double = (img_width / img_height) > (book_width / book_height * 1.5)
# the minimun length of the unique_id is 16 - its recommended to use a md5-hash with a prefix of the publishers name 
book = ecmbBook(BOOK_TYPE.MANGA, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)



# add some meta-data
###################################################

book.metadata.set_isbn('0123456789')
book.metadata.set_publisher('BestMangaPublisher Inc.', href='https://www.bestmangapublisher-inc.com')
book.metadata.set_publishdate('2023-01-18')
book.metadata.set_title('The Big Trip')
book.metadata.set_volume(1)
book.metadata.set_summary('A stick figure goes on a big thrilling hiking-trip.')

book.metadata.add_author('Clemens K.', AUTHOR_ROLE.STORY, href='https://github.com/metacreature')
book.metadata.add_author('Clemens K.', AUTHOR_ROLE.ART, href='https://github.com/metacreature')

book.metadata.add_genre('Adventure')
book.metadata.add_genre('Summer')

# it's really recommended to use this if necessary
book.metadata.add_content_warning(CONTENT_WARNING.SEXUAL_CONTENT)



# add data of the book which the story is based on
###################################################

book.based_on.set_type(BASED_ON_TYPE.LIGHTNOVEL)
book.based_on.set_isbn('9876543210')
book.based_on.set_publisher('BestNovelPublisher Inc.', href='https://www.bestnovelpublisher-inc.com')
book.based_on.set_publishdate('1986')
book.based_on.set_title('The Scary Hiking')

book.based_on.add_author('Agatha Christie', AUTHOR_ROLE.AUTHOR, href='https://www.agatha-christie.net')



# NOTE!
# passing an invalid value will cause an ecmbException
# an invalid value @ the constructor of ecmbBook, a wrong image-size @ contents aso. will also cause an ecmbException
try:
    book.metadata.set_summary(12345)
except ecmbException as e:
    print('EXCEPTION: ' + str(e), flush=True)


# set the cover-images
###################################################

book.content.set_cover_front('../source_images/front.jpg')
book.content.set_cover_rear('../source_images/rear.jpg')



# adding some content
###################################################

# folders with an uneven page-count are supported
# also double-pages on an uneven page and uneven page-count of the book ... of course you will get a warning
folder1 = book.content.add_folder()
# folder1.add_image('../source_images/img_1.jpg')
folder1.add_image('../source_images/img_2.jpg')

# you can define unique_ids to access the the objects easier for the navigation
# it would be a good idea to use file- and folder-paths of your source-files
folder2 = book.content.add_folder('the hiking-trip')
folder2.add_image('../source_images/img_3.jpg', unique_id = 'the start of the hiking-trip')
folder2.add_image('../source_images/img_4.jpg')
the_girl = folder2.add_image('../source_images/img_5.jpg')
folder2.add_image('../source_images/img_6.jpg')

# double pages require to have the full, left and right image
# every image can be a BytesIO, if you want the edit/split them on-the-fly
img = Image.open('../source_images/img_7.jpg')

img_left = img.crop((0, 0, 900, 1200))
img_right = img.crop((900, 0, 1800, 1200))

fp_left = io.BytesIO()
fp_right = io.BytesIO()
			
img_left.save(fp_left, 'jpeg', quality= 85)
img_right.save(fp_right, 'jpeg', quality= 85)

folder2.add_image('../source_images/img_7.jpg', fp_left, fp_right, unique_id='the summit')

del img, img_left, img_right, fp_left, fp_right

# subfolders and sub-sub-sub-sub-folders are supported 
# every folder have to have at least one image, even if there is only one in a sub-sub-sub-sub-folder
# you can mix folders and images on the same level
folder3 = folder2.add_folder()
folder3.add_image('../source_images/img_8.jpg')
folder3.add_image('../source_images/img_9.jpg')



# add navigation
###################################################

# you can pass either an object or a unique-id
# first param is of course the label
highlights = book.navigation.add_headline('Highlights')
highlights.add_link('The Girl', the_girl)

# on double-pages you can choose one side if you want to which is nice if the user reads the book in portrait-mode. Default is 'auto'
# this also works for folders
highlights.add_link('The Summit', 'the summit', target_side=TARGET_SIDE.LEFT)

# if you want to link to a specific image (default is the first one) you can pass either an image-object or a unique-id
chapter1 = book.navigation.add_chapter('Chapter 1', folder1, title='The Bus-Trip')
chapter2 = book.navigation.add_chapter('Chapter 2', 'the hiking-trip', 'the start of the hiking-trip', title='The Hiking-Trip')
chapter2.add_link('The Summit', 'the summit', target_side=TARGET_SIDE.LEFT)
chapter2.add_chapter('Chapter 2.1', folder3, title='Downhill')

# NOTE!
# you can mix headlines, chapters and links like you want, but i recommend to not mess around ... eg. sub-chapter in the root:
# book.navigation.add_chapter('Chapter 2.1', folder3, title='Downhill') 
#
# Of course the linked images must be part of the chapter's folder, otherwhise you will get an Exception




# write the book 
###################################################
def log_message(msg):
    print(msg, flush=True)
    with open('advanced_book.log', 'a') as f:
        f.write(msg + '\n')

def warning_callback(msg):
    log_message(msg)


log_message('\nStart building "advanced_book.ecmb"')

# NOTE!
# an empty folder, navigation-mismatch or a missing book-title will cause an ecmbException
try:
    book.write('advanced_book.ecmb', warnings=warning_callback, demo_mode=True)
    log_message('SUCCESS!')
except ecmbException as e:
    log_message('ERROR: ' + str(e))


print('\n', flush=True)