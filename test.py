import cairocffi as cairo
import drivers.cairo

from scenegraph import *

if __name__=="__main__":
    c = Canvas()
    c.fill("blue")
    c.stroke(0, 1, 0)
    
    p = c.path()
    p.moveto(0, 0)
    p.lineto(100, 0)
    p.lineto(100, 100)
    p.lineto(0, 100)
    p.lineto(0, 0)

    # Render to cairo surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)
    drivers.cairo.render(c.scenegraph, ctx)
    
    surface.write_to_png("output.png")

    # Display the graph we just rendered
    debug(c)