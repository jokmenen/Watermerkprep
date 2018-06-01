#!/usr/bin/env python
import sys
print(sys.argv[0],sys.version)
from PIL import Image, ExifTags
import os, watermarking, sys , piexif


print(sys.argv[0])
try:

    # Meh geen zin om dit af te maken, verander de hardcode maar
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

    VERTICAAL = False
    WMSOURCE = "wm.png"
    ACCEPTEDEXTS = [".jpg", ".jpeg",
                    ".png"]  # add extensions that can be accepted by the program. I cannot really get pngs to work


    # Check if argument passed is a file or folder, then either open the file or change into folder.
    def processArgv(args):

        # check if a file or folder is parsed
        if os.path.isfile(args[1]):  # File --> Image

            try:
                os.chdir(os.path.dirname(args[1]))

            except:
                print("Oeps, folder could not be opened")
                input("Enter om doortegaan")

            il = findParsables([args[1]])
            print("Processing Single Image...")


        else:  # Folder
            print("Processing Folder...")

            # go to the target dir
            try:
                os.chdir(args[1])

            except:
                print("Oeps, folder could not be opened")
                input("Enter om doortegaan")

            print("Making filelist")
            fl = makeFileList()  # get all the files in the current folder
            print("making imagelist")
            il = findParsables(fl)  # filter out all the unparsable files

        # verwerk de imagelist
        print("Adding EXIF...")
        #doAddEXIF(il)

    def makeFileList():
        # make list of images
        filelist = os.listdir()
        return filelist


    def findParsables(filelist):
        imagelist = []
        for file in filelist:  # filter out unparsable items (non-image files)
            if getExtention(file) in ACCEPTEDEXTS:
                # print(file, "kept")
                imagelist += [os.path.basename(file)]
                # imagelist+=[file]
            else:
                # print(file, "removed")
                continue

        return imagelist


    def doAddEXIF(imagelist):

        i = 0
        for image in imagelist:
            try:
                i += 1
                progressPercentage = i / len(imagelist) * 100
                print("Processing image #{}/{} | {:.1f}%".format(i, len(imagelist), progressPercentage), end="\r")
                fname = image
                im = fixOrientation(fname)


            except Exception as ex:
                print(image, "EXIFdata could not be added", ex)


    def getExtention(string):
        lastDot = string.rfind(".")
        size = len(string)
        if lastDot > 0:
            return string[lastDot:size].lower()
        else:
            return None


    # Checkt met behulp van exif tag hoe het plaatje gedraait moet zijn, wat wel zo handig is bij het checken van de orientatie. (dit is gejat van SO trouwens lol)
    def fixOrientation(image):


        if not('exif' in Image.open(image).info):
            print("No exif data found, Adding...")
            zeroth_ifd = {piexif.ImageIFD.Orientation: 1} #Laat de exif aangeven dat ie horizontaal is
            exif_dict = {"0th": zeroth_ifd} #voeg horizontaal toe aan de exif dictionary
            exif_bytes = piexif.dump(exif_dict) #dumpen naar bytes
            piexif.insert(exif_bytes, image) #invoegen in de afbeelding
            return image
        else:
            print("exif data already found")

            DEBUG = False
            if DEBUG:
                print("DEBUG mode enabled, Removing exif and running method again")
                piexif.remove(image)
                fixOrientation(image)




    #                  #
    # START OF PROGRAM #
    #                  #


    if len(sys.argv) == 2:

        processArgv(sys.argv)
        print("bla")

    elif len(sys.argv) > 2:
        print("Multiple arguments found... Parsing...")
        for idx, arg in enumerate(sys.argv):
            if idx == 0:
                continue
            else:
                print("Processing argument {}: {}...".format(idx, arg))
                processArgv([sys.argv[0], arg])
                print()
    else:
        print("jema")
        processArgv([sys.argv,os.getcwd()+"\exiftest2.jpeg"])
#        else:
#            wm_source = WMSOURCE

#    if not(dirchanged):
#        wm = Image.open(wm_source) Kan weg want wordt in processarg al gedaan

    input("Press enter to quit")

except Exception as henk:
    print("OEPS")
    print(sys.exc_info())
    print(os.getcwd())
    input(henk)


