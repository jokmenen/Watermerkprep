

def watermerk(plaatje, pnaam, watermerk,oFolder):
    try:
        #assumes pictures are already orientation-corrected
        wm = watermerk
        im = plaatje
        file = pnaam

        # file = "Test2.JPG"
        # wm_name = "wm.png"
        # wm = Image.open(wm_name)
        # im = Image.open(file)
        # im = fixOrientation(im)

        #aspect ratio formula
        ar = (im.width/5)/wm.width
        #print(ar)
        wm = wm.resize((int(ar*wm.width),int(ar*wm.height)), 0)
        if watermerk.format == "PNG":
            im.paste(wm, (im.width-wm.width,im.height-wm.height),wm)
        elif watermerk.format == "MPO":
            im.paste(wm, (im.width - wm.width, im.height - wm.height))
        im.save(oFolder  + file[:-4] + "-Watermarked"+file[-4:], "JPEG")
    except Exception as ex :
        print(ex)

if __name__ == '__main__':
    from PIL import Image, ExifTags
    import os, watermarking, sys

    fname = "Test.JPG"
    im = Image.open(fname)
    wm = Image.open("Test.JPG")
    print(wm.format)

    watermerk(im,fname,wm)


