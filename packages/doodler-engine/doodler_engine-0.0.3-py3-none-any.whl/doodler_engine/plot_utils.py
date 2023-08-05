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

#========================================================
## ``````````````````````````` imports
##========================================================
import PIL.Image
# import plotly.graph_objects as go
# # import skimage.util
# from plotly.utils import ImageUriValidator
from PIL import ExifTags

# ##========================================================
# def dummy_fig():
#     """ create a dummy figure to be later modified """
#     fig = go.Figure(go.Scatter(x=[], y=[]))
#     fig.update_layout(template=None)
#     fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
#     fig.update_yaxes(
#         showgrid=False, scaleanchor="x", showticklabels=False, zeroline=False
#     )
#     return fig

##========================================================
def pilim(im):
    if type(im) == type(str()):
        im = PIL.Image.open(im)		 	 	

        for orientation in ExifTags.TAGS.keys():
            # if ExifTags.TAGS[orientation]=='Orientation':
            #    break
            try:
                exif=dict(im._getexif().items())
                if exif[orientation] == 3:
                    im=im.rotate(180, expand=True)
                    # print("Image rotated 180 deg")
                elif exif[orientation] == 6:
                    im=im.rotate(270, expand=True)
                    # print("Image rotated 270 deg")
                elif exif[orientation] == 8:
                    im=im.rotate(90, expand=True)
                    # print("Image rotated 90 deg")
            except:
                # print('no exif')
                pass
    return im

##========================================================
def add_layout_images_to_fig(fig,
    images,
    update_ranges=True):
    """ images is a sequence of PIL Image objects """
    """Updates the figure to display the image provided. It places the image on the bottom layer
    to allow the doodles to show on top. The aspect ratio of the image is not maintained and all grid and tick lines
    are removed to only display the image."""

    if len(images) <= 0:
        return fig

    try:
        for im in images:
            # if image is a path to an image, load the image to get its size
            width, height = pilim(im).size
            # Add images
            fig.add_layout_image(
                dict(
                    source=im,
                    xref="x",
                    yref="y",
                    x=0,
                    y=0,
                    sizex=width,
                    sizey=height,
                    sizing="fill",
                    layer="below",
                )
            )
        if update_ranges:
            width, height = [
                max([pilim(im).size[i] for im in images]) for i in range(2)
            ]
            # Gets the max height and width for all of the images so the canvas can display
            #  both the highest and lowest images

            fig.update_xaxes(
                showgrid=False, range=(0, width), showticklabels=False, zeroline=False
            )
            fig.update_yaxes(
                showgrid=False,
                scaleanchor="x",
                range=(height, 0),
                showticklabels=False,
                zeroline=False,
            )
    except:
        pass
    return fig


# ##========================================================
# def pil2uri(img):
#     """ conevrts PIL image to uri"""
#     return ImageUriValidator.pil_image_to_uri(img)
