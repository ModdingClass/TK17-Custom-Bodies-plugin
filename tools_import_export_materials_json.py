import bpy
import json



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



#ob.data.polygons[0].material_index
#ob.data.materials

#for m in bpy.context.object.material_slots:
#    print(m.name)

#ob.material_slots[:][0].name

#https://polycount.com/discussion/213244/blender-python-2-79-writing-vertex-indices-from-vertex-groups

def exportMaterialsToJsonFile(ob, filename):
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and materials?!? (do we realy need that?!?)
    ob.update_from_editmode()
    #
    mats = ob.material_slots
    materialsExport = {mat.name:[ ] for mat in mats}
    #materialsExport = ob.material_slots.keys()   <-TypeError: list indices must be integers or slices, not str
    for f in ob.data.polygons:
        materialsExport[ob.material_slots[:][f.material_index].name].append(f.index)
    with open(filename, 'w') as outfile:
        outfile.write(prnDict(materialsExport).replace("'", "\""))


def importMaterialsFromJsonFile(ob, filename):
    def checkIfMaterialExistElseCreateIt(ob, material):
        mat = bpy.data.materials.get(material)
        #if it doesnt exist, create it.
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name=material)
            #assign material
        if mat.name not in ob.material_slots.keys():
            ob.data.materials.append(mat)     
        return mat

    #
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and weights
    ob.update_from_editmode()
    #
    f = open(filename,)
    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()     # Closing file
    #
    #
    for matName,faceIndices in data.items():
        material = checkIfMaterialExistElseCreateIt(ob, matName)
        material_index = bpy.context.object.material_slots.find(material.name)
        for i in faceIndices:
            ob.data.polygons[i].material_index = material_index
    #


