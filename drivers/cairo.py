try:
    import cairocffi as cairo
except:
    import cairo

"""
TODO

try:
Change to having some sort of graphics context with the current state
instead of recreating the scenegraph on this side with the objects.
"""

class CmdMxin(object):
    def __init__(self, cmd, *args):
        self.args = args
        self.cmd = cmd
    
    def rendergraph(self, element):
        print 'cmd rendergraph', self.__class__
        pass

    def render(self, element, *args, **kwargs):
        m = getattr(self, element.cmd)
        m(*element.args)

class SceneGraphMixin(object):
    def __init__(self, *args):
        self.args = args

    def render(self):
        pass

    def rendergraph(self, scenegraph, level=0, *args, **kwargs):
        print ' ' * level * 4 +  'rendergraph ', self.__class__
        klass = self.__class__
        for element in scenegraph.elements:
            #print ' ' * level * 4, element, element.elements
            subklass = getattr(klass, element.__class__.__name__)
            inst = subklass(*element.args)

            if element.elements is not None:
                inst.rendergraph(element, level+1, *args, **kwargs)
            else:
                inst.render(element, level=level+1, *args, **kwargs)


class Canvas(SceneGraphMixin):    
    def __init__(self, *args, **kwargs):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)

    def rendergraph(self, *args, **kwargs):
        """
        """
        if 'ctx' not in kwargs:
            kwargs['ctx'] = cairo.Context(self.surface)
        
        super(Canvas, self).rendergraph(*args, **kwargs)

    class Color(SceneGraphMixin):
        def render(self, element, *args, **kwargs):
            if element.cmd == 'fill':
                pass
            elif element.cmd == 'stroke':
                pass
            print ' ' * 4 * kwargs.get('level') + 'render %s cairo color' % element.cmd

    class Path(SceneGraphMixin):
        class PathElement(CmdMxin):
            def lineto(self, x, y):
                print 'lineto:', x, y
                pass

            def moveto(self, x, y):
                print 'moveto:', x, y
                pass


        def render(self, element, *args, **kwargs):
            print  ' ' * 4 * kwargs.get('level') + 'render cairo path'

def render(scenegraph, level=0):
    canvas = Canvas()
    canvas.rendergraph(scenegraph, level=0)

