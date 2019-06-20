import numpy as np
import operator
import matplotlib.pyplot as plt
import pandas as pd
import geopandas
import pgeocode

# parsing #

#barbools,pieciphersuites,piefp,piemx
# adds to the number of duplicates of a key
# value can be a list or an individual item,
# parameter value must be [value] if want list
def addDups(dct, key, value=1): #names
    temp=dct
    if key in temp:
        if str(type(value)) == "<class 'list'>":
            temp[key].append(value)
        else:
            temp[key] += value
    else:
        temp.update({key:value})
    return temp

# sorts a dict by its values (or len(values) if values are lists),
# and removes any values below a limit
#-only sorts if values aren't lists
def sortDict(dct, minDups=0, showOther=False,reverse=False):
    temp=dict()
    for key in dct:
        if str(type(dct[key])) == "<class 'list'>":
            numDups = len(dct[key])
            value=[dct[key]]
        else:
            numDups = dct[key]
            value=dct[key]
        if numDups > minDups:
            temp.update({key:dct[key]})
        elif showOther:
            temp=addDups(temp,'other',value)
            
    if len(dct) > 0 and str(type(list(dct.values())[0])) != "<class 'list'>":
        temp = sorted(temp.items(), key=operator.itemgetter(1))
        if reverse:
            temp.reverse()
    return dict(temp)

# graphs #

# maps a key to a colour, if not already mapped
# would be nicer if had colour as parameter,
# but doing so makes it the same every time...
def mapColour(dct, key, colour=-1):
    temp=dct
    if colour == -1:
        colour=np.random.uniform(0,1,size=4)
    if key not in dct:
        temp.update({key:colour})
    return temp

# labels a group of bars (init labels height)
def labelBars(rects, xalign='center', y=-1, txt='height', colour='k'):
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()

        #could be done better?
        if txt == 'height':
            out='{0:.3f}'.format(height)
        else:
            out=txt[rects.index(rect)]
        if y == -1:
            yOut=rect.get_y()
        else:
            yOut=y
            
        plt.annotate(out,
                    xy=(rect.get_x() + rect.get_width() / 2, yOut),
                    xytext=(offset[xalign]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=xalign,
                    color = colour)

# maps #

# maps coordinates onto a given base
def mapCoords(lats, longs, base, colour='r'):
    df = pd.DataFrame(
        {'Latitude': lats,
         'Longitude': longs})
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
    
    # add points
    gdf.plot(ax=base, color=colour)

# gets approximate coordinates for a given postcode
def getCoordsFromPostcodes(postcodes, country='ie'):
    nomi = pgeocode.Nominatim(country)
    lats=[]
    longs=[]
    for postcode in postcodes:
        if postcode:
            if country == 'ie': # might have to do something similar for some other countries idk
                coords = nomi.query_postal_code(postcode[:3])
            else:
                coords = nomi.query_postal_code(postcode)
            lats.append(coords['latitude'])
            longs.append(coords['longitude'])
    return lats, longs
