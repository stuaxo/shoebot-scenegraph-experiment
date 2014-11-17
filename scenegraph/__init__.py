import colour

"""
path elements

moveto x, y
lineto x, y
"""

def traverse(scenegraph, level=0):
    for element in scenegraph.elements:
        if element.elements is not None:
            print ' ' * (level * 4), element
            traverse(element, level + 1)
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

        # Convert type into 
        t = type(args)
        if t == tuple and len(args) in [3, 4]:
            self.args = args
        elif t in [str, unicode]:
            self.args = colour.hex2rgb(colour.web2hex(args))
        
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
        
    def fill(self, *args):
        c = args
        return self.scenegraph.add(Color("fill", *c))
        
    def stroke(self, *args):
        c = args
        return self.scenegraph.add(Color("stroke", *c))
    
    def path(self):
        p = Path()
        return self.scenegraph.add(p)


