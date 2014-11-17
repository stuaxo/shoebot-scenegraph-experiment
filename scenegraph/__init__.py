import colour

"""
path elements

moveto x, y
lineto x, y
"""


def debug(scenegraph, level=0):
    """
    Traverse scenegraph and print each node
    """
    for element in scenegraph.elements:
        if element.elements is not None:
            print ' ' * (level * 4), element
            debug(element, level + 1)
        else:
            print ' ' * (level * 4), element


class SceneGraph(object):
    def __init__(self):
        self.elements = []
        
    def add(self, element):
        self.elements.append(element)
        return element


class PathElement(object):
    elements = None
    
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args
        
    def __repr__(self):
        return '<PathElement {} {}>'.format(self.cmd, self.args)
        

class Color(object):
    elements = None
    
    def __init__(self, cmd, *args):
        """
        :param cmd: foreground | background
        """
        self.cmd = cmd
        col = args[0]

        if isinstance(args[0], basestring):
            self.args = colour.hex2rgb(colour.web2hex(col))
        elif len(args) in [3, 4]:
            self.args = args

    def __repr__(self):
        return '<Color {} {}>'.format(self.cmd, self.args)


class Path(object):
    def __init__(self):
        self.elements = []
        self.args = []

    def lineto(self, x, y):
        return self.elements.append(PathElement("lineto", x, y))

    def moveto(self, x, y):
        return self.elements.append(PathElement("moveto", x, y))
    
    def __repr__(self):
        return '<Path>'


class Canvas(object):
    def __init__(self):
        self.scenegraph = SceneGraph()
        self.elements = [self.scenegraph]

        ## These should really be stored in the graph somewhere
        self.fill_color = None
        self.stroke_color = None

    def fill(self, *args):
        c = args
        return self.scenegraph.add(Color("fill", *c))
        
    def stroke(self, *args):
        c = args
        return self.scenegraph.add(Color("stroke", *c))
    
    def path(self):
        p = Path()
        return self.scenegraph.add(p)


