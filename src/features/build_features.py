import os
import csv
import plotly.graph_objects as go
from PIL import Image

def main():
    os.chdir('/Volumes/YT/')
    IMAGES = build_img_list()
    IMAGES = fix_jpeg_to_jpg(IMAGES)
    SORTED_NAMES = profile_imgdir(IMAGES)
    profile_images(IMAGES)
    good_images_bad_names(IMAGES)
    plot_names(SORTED_NAMES)
    close_all(IMAGES)

def build_img_list():
    files = os.listdir()
    images = []
    for file in files:
        try:
            image = Image.open(file)
            images.append(file)
        except IOError:
            pass
    return images

def fix_jpeg_to_jpg(images):
    jpeg = 0
    for filename in images:
        name, ext = os.path.splitext(filename)
        if ext == '.jpeg':
            jpeg += 1
            os.rename(filename, name + '.jpg')
            images.remove(filename)
            images.append(name + '.jpg')
    if jpeg > 0:
        print('Renamed ' + str(jpeg) + ' jpeg images to jpg')
    return images

# Check if a string is an integer.
def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Check if name conforms to 'subject number' convention.
def good_filename(name):
    words = name.split()

    # Check last word is number
    if not represents_int(words[-1]):
        return False

    if len(words) == 1:
        return False

    # Loop through remainder of words, checking for capitalisation
    for i in range(0, len(words)-1):
        if words[i] != words[i].capitalize():
            return False
    return True

# Find out how many files in directory are properly named.
def profile_imgdir(images):
    print("Images: " + str(len(images)))
    goodnames = []
    badnames = []
    for filename in images:
        name, _ = os.path.splitext(filename)
        if good_filename(name):
            goodnames.append(name)
        else:
            badnames.append(name)

    print("Good filenames: " + str(len(goodnames)))
    names = {}
    for name in goodnames:
        name = name.rsplit(' ', 1)[0]
        if name in names.keys():
            names[name] += 1
        else:
            names[name] = 1

    sorted_names = sorted(names.items(), key=lambda x: x[1])
    return sorted_names

def profile_images(images):
    flaws = []
    for filename in images:
        image_flaws = []
        image = Image.open(filename)
        width, height = image.size

        # Proper name?
        name, _ = os.path.splitext(filename)
        if not good_filename(name):
            image_flaws.append('No')
        else:
            image_flaws.append('')

        # Bad ratio?
        if width/height != 16/9:
            if width/height < 16/9 * 1.005 and width/height > 16/9 * 0.995:
                image_flaws.append('passable')
            else:
                image_flaws.append('bad')
        else:
            image_flaws.append('')

        # Too small?
        if width < 1280:
            image_flaws.append('too small')
        else:
            image_flaws.append('')
        image.close()
        flaws.append(image_flaws)

    write_out(images, flaws)

def write_out(images, flaws):
    print('Writing CSV')
    output_file = open('bad.csv', 'w', newline='')
    output_writer = csv.writer(output_file)
    output_writer.writerow(['Filename', 'Proper name', 'Bad ratio', 'Too small'])

    for image in images:
        row = flaws.pop(0)
        row.insert(0, image)
        output_writer.writerow(row)
    output_file.close()

def good_images_bad_names(images):
    for filename in images:
        image = Image.open(filename)
        width, height = image.size
        name, _ = os.path.splitext(filename)
        if width == 1920 and height == 1080 and not good_filename(name):
            print(name)
        if width == 1600 and height == 900 and not good_filename(name):
            print(name)

def plot_names(name_list):

    x_axis = []
    y_axis = []
    for i in name_list:
        x, y = i
        x_axis.append(x)
        y_axis.append(y)

    fig = go.Figure(go.Bar(x=x_axis, y=y_axis))
    fig.show()

def close_all(images):
    for filename in images:
        image = Image.open(filename)
        width, height = image.size
        name, _ = os.path.splitext(filename)
        if width == 1920 and height == 1080 and not good_filename(name):
            print(name)
        if width == 1600 and height == 900 and not good_filename(name):
            print(name)

if __name__ == '__main__':
    main()
    