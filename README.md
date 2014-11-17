Scenegraph renderer experiment.

Implements a simple nodebox/shoebot like grammar end renders using a scenegraph.


Example, rendering to cairo.
```python
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

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)

    drivers.cairo.render(c.scenegraph, ctx)

    surface.write_to_png("output.png")

    # Display the graph we just rendered
    debug(c)
```

The simple commands, add elements to the scenegraph, for instance - the example 
above creates the following scenegraph:

```
 <scenegraph.SceneGraph object at 0x14f4810>
     <Color fill (0.0, 0.0, 1.0)>
     <Color stroke (0, 1, 0)>
     <Path>
         <PathElement moveto (0, 0)>
         <PathElement lineto (100, 0)>
         <PathElement lineto (100, 100)>
         <PathElement lineto (0, 100)>
         <PathElement lineto (0, 0)>   
```

Drivers render the graph by traversing it and instanciating classes that mirror 
those in the scenegraph, but that can do the rendering.



Finding classes:
================

In the cairo driver, classes are nested, the TraverserMixn can find the
implementation by looking inside the child class.

```python
class Canvas(TraverserMixin):
    ....
    class Path(TraverserMixin):
        class PathElement(CmdMxin):
            def lineto(self, traverser, x, y):
                traverser.ctx.line_to(x, y)

            def moveto(self, traverser, x, y):
                traverser.ctx.move_to(x, y)

            def rect(self, traverser, width, height):
                traverser.ctx.rectangle(0, 0, width, height)

```

Commands
--------

In the code above some PathElement is a CmdMixin - this allows functions to be
used.



TODO
====

State passed around needs to be much more simple.


