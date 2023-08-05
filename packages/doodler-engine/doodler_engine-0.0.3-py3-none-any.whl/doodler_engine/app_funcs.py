# Written by Dr Daniel Buscombe, Marda Science LLC
# for the USGS Coastal Change Hazards Program
#
# MIT License
#
# Copyright (c) 2020-2021, Marda Science LLC
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

from glob import glob

import io, os, psutil, logging, base64, PIL.Image
# from .plot_utils import dummy_fig, add_layout_images_to_fig
import zipfile

##========================================================
def get_asset_files():
    files = sorted(glob('assets/*.jpg')) + sorted(glob('assets/*.JPG')) + sorted(glob('assets/*.jpeg'))

    # Any image with 'dash' in the name is used for styling and is not data to be processed
    files = [f for f in files if 'dash' not in f]
    return files

##========================================================
def look_up_seg(d, key):
    """ Returns a PIL.Image object """
    data = d[key]
    img_bytes = base64.b64decode(data)
    img = PIL.Image.open(io.BytesIO(img_bytes))
    return img

##========================================================
def listToString(s):
    # initialize an empty string
    str1 = " "
    # return string
    return (str1.join(s))

##========================================================
def uploaded_files(filelist,UPLOAD_DIRECTORY,LABELED_DIRECTORY):
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            if 'jpg' in filename:
                files.append(filename)
            if 'JPG' in filename:
                files.append(filename)
            if 'jpeg' in filename:
                files.append(filename)

    labeled_files = []
    for filename in os.listdir(LABELED_DIRECTORY):
        path = os.path.join(LABELED_DIRECTORY, filename)
        if os.path.isfile(path):
            if 'jpg' in filename:
                labeled_files.append(filename)
            if 'JPG' in filename:
                labeled_files.append(filename)
            if 'jpeg' in filename:
                labeled_files.append(filename)
            if 'zip' in filename:
                zipF = zipfile.ZipFile(path)
                zfilelist = zipF.namelist()
                for zfiles in zfilelist:
                    if 'jpg' in zfiles:
                        labeled_files.append(zfiles)
                    if 'JPG' in zfiles:
                        labeled_files.append(zfiles)
                    if 'jpeg' in zfiles:
                        labeled_files.append(zfiles)
                

    with open(filelist, 'w') as filehandle:
        for listitem in labeled_files:
            filehandle.write('%s\n' % listitem)

    return sorted(files), sorted(labeled_files)


# ##========================================================
# def make_and_return_default_figure(
#     images,#=[DEFAULT_IMAGE_PATH],
#     stroke_color,#=convert_integer_class_to_color(class_label_colormap,DEFAULT_LABEL_CLASS),
#     pen_width,#=DEFAULT_PEN_WIDTH,
#     shapes#=[],
# ):
#     """
#     create and return the default Dash/plotly figure object
#     """
#     fig = dummy_fig() #plot_utils.

#     add_layout_images_to_fig(fig, images) #plot_utils.

#     fig.update_layout(
#         {
#             "dragmode": "drawopenpath",
#             "shapes": shapes,
#             "newshape.line.color": stroke_color,
#             "newshape.line.width": pen_width,
#             "margin": dict(l=0, r=0, b=0, t=0, pad=4),
#             "height": 650
#         }
#     )

#     return fig

#