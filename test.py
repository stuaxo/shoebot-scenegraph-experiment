import drivers.cairo

from scenegraph import *

if __name__=="__main__":
    c = Canvas()
    c.stroke(0, 0, 0)
    c.fill(1, 1, 1)
    
    p = c.path()
    p.moveto(0, 0)
    p.lineto(10, 0)
    p.lineto(10, 10)
    p.lineto(0, 10)
    p.lineto(0, 0)

    print ''    
    print 'Traverse:'
    traverse(c.scenegraph)
    
    print ''
    print 'Render:'
    drivers.cairo.render(c.scenegraph)
