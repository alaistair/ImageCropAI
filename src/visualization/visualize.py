import pandas as pd
import streamlit as st
import imghdr
import memory_profiler
import os
from PIL import Image
import sys
sys.path.append('../')
import features.build_features
m1 = memory_profiler.memory_usage()

st.title('ImageCropAI')

# Load image data
#IMAGE_PATH = '/Volumes/YT/'
IMAGE_PATH = '../../data/raw/'

#@st.cache
def load_data(IMAGE_PATH):
    f = []
    for (_, _, filenames) in os.walk(IMAGE_PATH):
        f.extend(filenames)
        break
    image_names = []
    image_size = []
    image_dim = []
    for filename in filenames:
        fullname = IMAGE_PATH + filename
        try:
            image = Image.open(fullname)
            image_names.append(filename)
            image_size.append(round(os.path.getsize(fullname)/1000000, 3))
            image_dim.append(image.size)
            image.close()
        except IOError:
            pass
        
    images_data = pd.DataFrame({'Name': image_names,
                                'Size (Mb)': image_size,
                                'Dimensions (w x h)': image_dim})

    
    return images_data

def add_features(images_data):
    images_data['Good name'] = ""
    for name in images_data['Name']:
        if features.build_features.good_filename(name):
            images_data['Good name'] = 'Yes'
        else:
            images_data['Good name'] = 'No'
    return images_data

images_data = load_data(IMAGE_PATH)
images_data.sort_values(by=['Name'], inplace=True)
images_data = images_data.reset_index(drop=True)


images_data = add_features(images_data)


st.write(images_data)
st.write(str(len(images_data)) + ' images, average size: ' + str(round(images_data['Size (Mb)'].mean(),2)) + ' Mb')

image_focus = st.selectbox(
    'Image to edit:',
    images_data['Name']
)
image_focus = IMAGE_PATH + image_focus

st.image(image_focus, use_column_width=True)

st.sidebar.selectbox('Hello', ('yes', 'no'))
st.sidebar.text('Hello')
m2 = memory_profiler.memory_usage()

st.sidebar.text('Used ' + str(m2[0] - m1[0]) + ' Mb to execute')