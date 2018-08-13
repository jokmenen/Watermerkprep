#!/usr/bin/env python

from PIL import Image, ExifTags
import os, watermarking, sys

print(sys.argv[0],sys.version)
try:

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
    
    
    

    
    VERTICAAL = False
    WMSOURCE = "wm.png"
    ACCEPTEDEXTS = [".jpg",".jpeg",".png"] #add extensions that can be accepted by the program. I cannot really get pngs to work

    
    #Check if argument passed is a file or folder, then either open the file or change into folder.
    def processArgv(args,wm):
        
        
            
            #check if a file or folder is parsed
            if os.path.isfile(args[1]): #File --> Image
                
                try:
                    os.chdir(os.path.dirname(args[1]))
    
                except:
                    print("Oeps, folder could not be opened")
                    input("Enter om doortegaan")
                    
                print("Making Watermark dir")    
                makeDir() #make the "Watermark" dir
                il = findParsables([args[1]])
                print("Processing Single Image...")
                
                
            else: #Folder
                print("Processing Folder...")
                
                #go to the target dir
                try:
                    os.chdir(args[1]) 
    
                except:
                    print("Oeps, folder could not be opened")
                    input("Enter om doortegaan")
                    
                print("Making Watermark dir")    
                makeDir() #make the "Watermark" dir
                print("Making filelist")  
                fl = makeFileList() #get all the files in the current folder
                print("making imagelist")  
                il = findParsables(fl) #filter out all the unparsable files
                
            #verwerk de imagelist  
            print("Watermarking...")           
            doWatermark(il,wm)
        
        
    def makeDir():
        #Make Watermerk dir
        if not os.path.exists("Watermerk"):
            os.makedirs("Watermerk")
                    
    def makeFileList():
        #make list of images
        filelist = os.listdir()
        return filelist

            
        
    def findParsables(filelist):
        imagelist = []
        for file in filelist: #filter out unparsable items (non-image files)
            if getExtention(file) in ACCEPTEDEXTS:
                #print(file, "kept")
                imagelist+=[os.path.basename(file)]
                #imagelist+=[file]
            else:
                #print(file, "removed")
                continue
    
        return imagelist
        
        
    def doWatermark(imagelist,watermarkfile):
        
        
        i = 0
        for image in imagelist: 
            try:
                i+=1
                progressPercentage = i/len(imagelist)*100
                print("Processing image #{}/{} | {:.1f}%".format(i,len(imagelist),progressPercentage), end="\r")
                fname = image
                im = Image.open(fname)
                p = im.load()
                im = fixOrientation(im)
               
#                #horizontaal
#                if im.width>=im.height:
#                    print(fname, "is horizontaal.",im.size[0],im.size[1])
#    
#                else:
#                    print(fname, "is verticaal.")
#                    if VERTICAAL:
#                        print("Placing in vertical folder!")
#                        os.rename(fname, r"Vertical\\" + fname)
    
                watermarking.watermerk(im,fname,watermarkfile,r"Watermerk\\",getExtention(fname))
                
                
    
            except Exception as ex:
                print(image, "could not be watermarked", ex)
    
                
    
    def getExtention(string):
        lastDot = string.rfind(".")
        size = len(string)
        if lastDot>0:
            return string[lastDot:size].lower()
        else:
            return None
            
    
    
    #Checkt met behulp van exif tag hoe het plaatje gedraait moet zijn, wat wel zo handig is bij het checken van de orientatie. (dit is gejat van SO trouwens lol)
    def fixOrientation(image):
        try:

            if image._getexif().items() == None:
                print("joepie")


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
            print("No EXIF found, trying non-exif method...")
            try:
                if image.height > image.width:
                    image = image.rotate(90, expand=True)
                    print("WARNING: Possible upside down images. Manual check recommended.")
                    return image
                else:
                    return image
            except:
                print("Manual mode failed, returning original...")
                return image
            # cases: image don't have getexif
            
                 
                
                

                
                
                
    #                  #
    # START OF PROGRAM #
    #                  #              
                
    wm_source = os.path.dirname(sys.argv[0])+'\\'+WMSOURCE #select watermark
    with Image.open(wm_source) as wm:
            
        if len(sys.argv) == 2:
            
                processArgv(sys.argv,wm)
    
        elif len(sys.argv) > 2:
            print("Multiple arguments found... Parsing...")
            for idx,arg in enumerate(sys.argv):
                if idx == 0:
                    continue
                else:
                    print("Processing argument {}: {}...".format(idx,arg))
                    processArgv([sys.argv[0],arg],wm)
                    print()
#        else:
#            wm_source = WMSOURCE

#    if not(dirchanged):
#        wm = Image.open(wm_source) Kan weg want wordt in processarg al gedaan





    
    input("Press enter to quit")

except Exception as henk:
    print(sys.exc_info())
    print(os.getcwd())
    input(henk)
    


    

