import sys
from .bpyth_human import human_readable_bytes

#############################################################################################################
###
### Programming tools and introspection
###
#############################################################################################################


class runstat:
    '''
    wraps a function, to keep a running count of how many times it's been called
    
    print_mit_stat = runstat(print)
    print_mit_stat() # funktioniert jetzt wie print
    print_mit_stat.time_since()  # Wann wurde die Funktion zuletzt aufgerufen?
    print_mit_stat.count()       # wie oft ist die Funktion aufgerufen worden? 
    
    '''

    def __init__(self, func):
        self.func = func
        self.count = 0
        self.time  = time.perf_counter()     
        
    def time_since(self):
        result = round(time.perf_counter() - self.time, 1)
        self.time  = time.perf_counter() 
        return "{} sec".format(result)

    def __call__(self, *args, **kwargs):
        self.count += 1
        self.time  = time.perf_counter()         
        return self.func(*args, **kwargs)
    



def raise_if(error):
# ---------------------------------------------------------------------------------------------       
    if error:
        raise Exception(error)    
# ---------------------------------------------------------------------------------------------      




def memory_consumption(locals_):
    '''
    Returns the memory consumption of all local variables.
    Call:
    bpy.memory_consumption(locals())
    '''
    
    for name, size in sorted((    (name, sys.getsizeof(value)) for name, value in locals_.items()    ),
                             key= lambda x: -x[1])[:10]:
        print("{:>30}: {:>8}".format(  name, human_readable_bytes(size)   ))
    
 
    