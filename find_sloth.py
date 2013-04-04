import random
import urllib2
import simplejson
import re
import linecache
import string

def find_sloth(search_terms):
    filename = "sloth"

    searchTerm = "sloth"
    if (search_terms):
        searchTerm += " " + search_terms

    # # find random work from dictionary
    # try:
    #     line = linecache.getline("dictionary.txt", random.randint(1, 99000))
    #     line = string.rstrip(line)
    #     searchTerm = "sloth " + line
    # except:
    #     pass

    print searchTerm

# escape spaces
    searchTerm = searchTerm.replace(' ','%20')

# Choose random start page. Images are retrieved in groups of 4
    sloth_start = random.randint(0, 15)
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(sloth_start*4))
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

# Get JSON result
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']

# Choose a random image from the result group
    result_size = len(dataInfo)
    imgurl = dataInfo[random.randint(0, result_size-1)]['unescapedUrl']
    extension = re.findall(r'[\w]+$', imgurl)[0]

    img = urllib2.urlopen(imgurl).read()
    img_name = filename+ "." + extension
    imgfile = open(img_name, 'w')
    imgfile.write(img)
    imgfile.close()

    print imgurl
    return img_name

if __name__ == '__main__':
    find_sloth()
