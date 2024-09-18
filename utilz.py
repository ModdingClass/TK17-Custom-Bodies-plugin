import bpy
import json
import math
import re
from collections import OrderedDict

# Function to check if an object has non-default transforms
def has_non_default_transforms(obj):
    tolerance = 1e-6
    return (
        any(abs(val) > tolerance for val in obj.location) or
        any(abs(val) > tolerance for val in obj.rotation_euler) or
        any(abs(val - 1.0) > tolerance for val in obj.scale)
    )

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
	def draw(self, context):
		self.layout.label(message)
	bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# Function to show a popup warning
def show_warning(message):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title="Warning", icon='ERROR')


def prnDict(aDict, br='\n', html=0, keyAlign='l',   sortKey=0,  keyPrefix='',   keySuffix='',  valuePrefix='', valueSuffix='', leftMargin=0,   indent=1 ):
	#from: https://code.activestate.com/recipes/327142-print-a-dictionary-in-a-structural-way/
	#sortKey require: odict() # an ordered dict, if you want the keys sorted.
    #     Dave Benjamin 
    #     http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/161403
    if aDict:
        #------------------------------ sort key
        if sortKey:
            dic = aDict.copy()
            keys = dic.keys()
            keys.sort()
            aDict = odict()
            for k in keys:
                aDict[k] = dic[k]
        #------------------- wrap keys with ' ' (quotes) if str
        tmp = ['{']
        ks = [type(x)==str and "'%s'"%x or x for x in aDict.keys()]
        #------------------- wrap values with ' ' (quotes) if str
        vs = [type(x)==str and "'%s'"%x or x for x in aDict.values()] 
        maxKeyLen = max([len(str(x)) for x in ks])
        for i in range(len(ks)):
            #-------------------------- Adjust key width
            k = {1            : str(ks[i]).ljust(maxKeyLen),
                 keyAlign=='r': str(ks[i]).rjust(maxKeyLen) }[1]
            v = vs[i]        
            tmp.append(' '* indent+ '%s%s%s:%s%s%s,' %(keyPrefix, k, keySuffix, valuePrefix,v,valueSuffix))
        tmp[-1] = tmp[-1][:-1] # remove the ',' in the last item
        tmp.append('}')
        if leftMargin:
          tmp = [ ' '*leftMargin + x for x in tmp ]
        if html:
            return '<code>%s</code>' %br.join(tmp).replace(' ','&nbsp;')
        else:
            return br.join(tmp)     
    else:
        return '{}'



# Function to remove quotes inside square brackets
def remove_quotes_from_brackets(text):
    def replace_quotes(match):
        return match.group(0).replace('"', '')
    return re.sub(r'\[.*?\]', replace_quotes, text)

# Function to load and parse JSON data
def load_json(filepath):
    with open(filepath, 'r') as infile:
        return json.load(infile)

def deselect_all_objects():
    #bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.context.selected_objects:
        ob.select = False



