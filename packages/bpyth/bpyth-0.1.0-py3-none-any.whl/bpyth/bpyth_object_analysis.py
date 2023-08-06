

#############################################################################################################
###
### Object analysis
###
#############################################################################################################        
    
def stype(obj):
    '''
    Returns the type as a short string
    '''
    return type(obj).__name__.split('.')[-1]
   
    
    

def rtype(inputobjekt):    
    '''
    Recursive type. Parses an n-dimensional object and returns a tuple of stype for the scalar in the top left corner. 
    E.g. an array of lists of ints returns ('ndarray', 'list', 'int').
    Caution: only a single scalar is found. A heterogeneous data structure cannot be parsed meaningfully. 
    '''
    
    # DataFrame
    if stype(inputobjekt) == 'DataFrame':
        try:
            s = inputobjekt.iloc[0]
        except:
            return ('DataFrame',)
        try:
            e = s.iloc[0]
        except:
            return ('DataFrame','Series')        
        return ('DataFrame','Series',stype(e))
    
    
    def itype(inputobjekt, result=-1 ):

        # type bestimmen
        t = stype(inputobjekt)
        #print(result,t)

        if result == -1:
            result = []
            result.append(t)
        else:
            result.append(t)
        #print(t, len(result))

        if t in ['str']: # iterable, soll aber nicht durchiteriert werden
            return result  

        if t in ['dict']: 
            iterator = iter(inputobjekt.values())
        else:
            try:
                iterator = iter(inputobjekt)
            # nicht iterable: Rekursionsende    
            except TypeError:
                return result

        # ist iterable
        try: 
            return itype( next(iterator), result=result )   
        except StopIteration:
            return result
        # -- ENDE itype
    
    # rtype
    result = itype(inputobjekt)
    result = [e for e in result if not  e.endswith('_')] # filtert z.B. 'str_' raus
    return tuple(result)    
    
    
    

def shape(obj):
    '''
    Recursive len. Parses an n-dimensional object and returns a tuple of sizes.
    Caution: only a single scalar is found. A heterogeneous data structure cannot be parsed meaningfully.     
    '''
    
    # Trivialfälle
    if not has_shape(obj):
        return tuple()
    if stype(obj) == 'DataFrame':
        return obj.shape
    
    def ishape(obj):
        try:
            shapes = []
            if isinstance(obj, dict):
                for x in obj.values():
                    if has_shape(x):     
                        shapes.append( ishape(x) )
                    else:
                        shapes.append( [0] )
            else:
                for x in obj:
                    if has_shape(x):    
                        shapes.append( ishape(x) )
                    else:
                        shapes.append( [0] )

        except TypeError:
            shapes = [0]

        try:
            shape = shapes[0]
        except IndexError:
            shape = []
        if shapes.count(shape) != len(shapes): 
            raise ValueError('Ragged list')
        try:
            # Einzusetzender Wert
            shape.append( len(obj) )
        except:
            return []
            #shape.append(0)
        return shape
    
    result = reversed(ishape(obj))
    # Nullen entfernen
    result = [ s for s in result if s > 0]
    return tuple(result)    
    
    

def has_shape(inputobjekt):
    '''
    Does an object have additional dimensions?
    Skalars: No
    Strings: No (per definition)    
    Empty Iterables: No (per definition)    
    Other Iterables: Yes
    '''
    
    if stype(inputobjekt) in ['str']: # iterable, soll aber nicht durchiteriert werden
        return False    
    try:
        iterator = iter(inputobjekt)
    except TypeError:
        return False
    else:
        try:
            test = next(iterator)
            return True
        except StopIteration:
            return False        
    