import ast
import sys
import piwigo

## Catalogues as keys, filepaths as value(s) in list.

def piwigoUpload(imageLocs, cat):
    photoSite = piwigo.Piwigo('http://samandgraemewedding.co.uk/piwigo')
    photoSite.pwg.session.login(username='egcyf', password='bigvegPIWIGO10')
    for imageLoc in imageLocs:
        photoSite.pwg.images.addSimple(image=imageLoc, category=cat)
    photoSite.pwg.session.logout()
    print "Upload complete!"


if __name__ == "__main__":
    print "Hello!"
    try:
        argDict = ast.literal_eval(sys.argv[1])
    except:
        sys.exit()
    print argDict
    print type(argDict)
    photoSite = piwigo.Piwigo('http://samandgraemewedding.co.uk/piwigo')
    photoSite.pwg.session.login(username='egcyf', password='bigvegPIWIGO10')
    for cat in argDict:
        print cat
        imageLocs = argDict[cat]
        for imageLoc in imageLocs:
            print imageLoc
            photoSite.pwg.images.addSimple(image=imageLoc, category=cat)            
    photoSite.pwg.session.logout()
    print "Upload complete!"
