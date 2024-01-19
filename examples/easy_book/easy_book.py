# only for relative import if you cloned the project
# you have to delete this if ecmblib is installed as a module
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(str(directory.parent.parent.parent) + '/src/')


from ecmblib import ecmbBook, BOOK_TYPE, CONTENT_WARNING



print('\n', flush=True)


# create book-obj
###################################################

# book-type, language, unique-id, width of the images, height of the images
# The width and height "should" be the size of the images. 
# It not exact, coz when I was building fan-translated Mangas, all images had a different size and aspect-ratio, 
# but the aspect-ratio is enterly important for the validator to validate the correct placement of double-page-images.
# Formula: id_double = (img_width / img_height) > (book_width / book_height * 1.5)
# the minimun length of the unique_id is 16 - its recommended to use a md5-hash with a prefix of the publishers name 
book = ecmbBook(BOOK_TYPE.MANGA, 'en', 'bestmangapublisherinc_98a2cd12fea1168d', 900, 1200)



# add some meta-data
###################################################

book.metadata.set_title('The Big Trip')
book.metadata.set_volume(1)
book.metadata.set_summary('A stick figure goes on a big thrilling hiking-trip.')

book.metadata.add_author('Clemens K.')

book.metadata.add_genre('Adventure')
book.metadata.add_genre('Summer')

# it's really recommended to use this if necessary
book.metadata.add_content_warning(CONTENT_WARNING.SEXUAL_CONTENT)



# set the cover-images
###################################################

book.content.set_cover_front('../source_images/front.jpg')
book.content.set_cover_rear('../source_images/rear.jpg')



# adding some content
###################################################

folder1 = book.content.add_folder()
folder1.add_image('../source_images/img_1.jpg')
folder1.add_image('../source_images/img_2.jpg')

# you can define unique_ids to access the the objects easier for the navigation
# it would be a good idea to use file- and folder-paths of your source-files
folder2 = book.content.add_folder('the hiking-trip')
folder2.add_image('../source_images/img_3.jpg', unique_id = 'the start of the hiking-trip')

folder2.add_image('../source_images/img_4.jpg')
folder2.add_image('../source_images/img_5.jpg')
folder2.add_image('../source_images/img_6.jpg')

# double pages require to have the full, left and right image
folder2.add_image('../source_images/img_7.jpg', '../source_images/img_7_left.jpg', '../source_images/img_7_left.jpg')

folder2.add_image('../source_images/img_8.jpg')
folder2.add_image('../source_images/img_9.jpg')



# add navigation
###################################################

# you can pass either an object or a unique-id
# first param is of course the label
# if you want to link to a specific image (default is the first one) you can pass either an image-object or a unique-id
book.navigation.add_chapter('Chapter 1', folder1, title='The Bus-Trip')
book.navigation.add_chapter('Chapter 2', 'the hiking-trip', 'the start of the hiking-trip', title='The Hiking-Trip')



# write the book 
###################################################

book.write('easy_book.ecmb', warnings=True, demo_mode=True)



print('  "easy_book.ecmb" was generated successfull!')


print('\n', flush=True)