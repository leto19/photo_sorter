
import os.path
import sys
import json
from PIL import Image, ExifTags
from datetime import datetime
import shutil
from calendar import month_name
import argparse
def get_date(filename):
    image_exif = Image.open(filename)._getexif()
    if image_exif:
        # Make a map with tag names
        exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items(
        ) if k in ExifTags.TAGS and type(v) is not bytes}
        #print(json.dumps(exif, indent=4))
        # Grab the date
        date_obj = datetime.strptime(
            exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        
    else:
        print("could not get a date!")
        date_obj = datetime.ctime()
    return date_obj


folder = sys.argv[1]
names = os.listdir(folder) 

"""
if os.path.exists("%soutput" % folder):
    pass
else:
    os.mkdir("%soutput"%folder)
"""

pics = [name for name in names if name.endswith(
    '.png') or name.endswith('.jpg') or name.endswith('.JPG')]
folder_out = folder
#folder_out = folder + "output/"
for pic in pics:
    pic_date = get_date("%s%s" % (folder, pic))
    print(pic," : ",pic_date)

    # make directories
    if os.path.exists("%s%s" % (folder_out, pic_date.year)):
        print("already a folder for that year!")
    else:
        os.mkdir("%s%s" % (folder_out, pic_date.year))

    if os.path.exists("%s%s/%s" % (folder_out, pic_date.year, month_name[pic_date.month])):
        print("already a folder for that month!")
    else:
        os.mkdir("%s%s/%s" %
                 (folder_out, pic_date.year, month_name[pic_date.month]))

    #copy files to folder
    if len(sys.argv) == 3 and sys.argv[2] == "-m":
        shutil.move("%s%s" % (folder, pic), "%s%s/%s" %
                    (folder_out, pic_date.year, month_name[pic_date.month]))
    else:
        shutil.copy("%s%s" % (folder, pic), "%s%s/%s" %
                    (folder_out, pic_date.year, month_name[pic_date.month]))
