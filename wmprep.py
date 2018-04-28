from PIL import Image, ExifTags
import os, watermarking, sys

#Meh geen zin om dit af te maken, verander de hardcode maar
# CONFIG = "wm.cfg"
#
# configvars = ["WATERMARK", "VERTICAL"]
#
# with open(CONFIG) as cfg:
#     arglist = cfg.readlines()
#     print(arglist)
#     for line in arglist:
#         if line[0] == "#":
#             print(line)
#         for vars in configvars:
#             if line[:len(vars)] == vars:
#                 print("asdasoijasd", vars)
#
#             else:
#                 #print("huh",line[:len(vars)],vars, line, len(vars))
#                 print("else")
#
#
#

VERTICAAL = False
WMSOURCE = "wm.png"

dirchanged = False

if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        wm_source = sys.argv[1]
    else:
        dirchanged = True
        wm_source = WMSOURCE
        wm = Image.open(wm_source)
        try:
            os.chdir(sys.argv[1])

        except:
            print("Oeps")
            input("Enter om doortegaan")

elif len(sys.argv) > 2:
    print("Too many arguments!")
    input("Press enter to quit")
    sys.exit(1)
else:
    wm_source = WMSOURCE

if not(dirchanged):
    wm = Image.open(wm_source)

#Checkt met behulp van exif tag hoe het plaatje gedraait moet zijn, wat wel zo handig is bij het checken van de orientatie. (dit is gejat van SO trouwens lol)
def fixOrientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        return image

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass


#Make Vertical and Watermerk dirs
dirs = ["Verticaal","Watermerk"]

for name in dirs:
    if name == "Verticaal" and not(VERTICAAL):
        pass
    else:
        if not os.path.exists(name):
            os.makedirs(name)

#make list of images
filelist = os.listdir()
imagelist = []
print(filelist)
for file in filelist:
    if file[-4:].lower() == ".jpg":
        print(file, "kept")
        imagelist+=[file]
    else:
        print(file, "removed")

print(imagelist)

for image in imagelist:
    try:
        fname = image
        im = Image.open(fname)
        im = fixOrientation(im)

        #horizontaal
        if im.size[0]>=im.size[1]:
            print(fname, "is horizontaal.",im.size[0],im.size[1])

        else:
            print(fname, "is verticaal.")
            if VERTICAAL:
                print("Placing in vertical folder!")
                os.rename(fname, r"Vertical\\" + fname)

        watermarking.watermerk(im,fname,wm,r"Watermerk\\" )

    except Exception as ex:
        print(image, "could not be watermarked", ex)

    finally:
        im.close()

wm.close()
input("Press enter to quit")


