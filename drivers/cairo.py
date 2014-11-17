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
        """
        Render using a method with the same name as cmd
        """
        self.cmd = cmd
    
    def rendergraph(self, traverser, scenegraph, element):
        print 'cmd rendergraph', self.__class__
        pass

    def enter(self, traverser, element, *args, **kwargs):
        pass

    def render(self, traverser, element, *args, **kwargs):
        m = getattr(self, element.cmd)
        m(traverser, *element.args)

    def leave(self, traverser, element, *args, **kwargs):
        pass


class TraverserMixin(object):
    def __init__(self, *args):
        self.args = args

    def render(self):
        pass

    def enter(self, *args, **kwargs):
        pass

    def leave(self, *args, **kwargs):
        pass

    def rendergraph(self, traverser, scenegraph, level=0, *args, **kwargs):
        #print ' ' * level * 4 +  'rendergraph ', self.__class__
        klass = self.__class__
        for element in scenegraph.elements:
            #print ' ' * level * 4, element, element.elements
            childklass = getattr(klass, element.__class__.__name__)
            inst = childklass(*element.args)

            if element.elements is not None:
                inst.enter(traverser, element, level=level+1, *args, **kwargs)
                inst.rendergraph(traverser, element, level=level+1, *args, **kwargs)
                inst.leave(traverser, element, level=level+1, *args, **kwargs)
            else:
                inst.enter(traverser, element, level=level+1, *args, **kwargs)
                inst.render(traverser, element, level=level+1, *args, **kwargs)
                inst.leave(traverser, element, level=level+1, *args, **kwargs)


class Canvas(TraverserMixin):
    def __init__(self, ctx):
        """
        :param ctx: Cairo context
        """
        self.ctx = ctx

        self.fill_color = None
        self.stroke_color = None

    def rendergraph(self, traverser, *args, **kwargs):
        """
        """
        if traverser is None:
            traverser = self

        if 'ctx' not in kwargs:
            kwargs['ctx'] = cairo.Context(self.surface)

        super(Canvas, self).rendergraph(traverser, *args, **kwargs)

    class Color(TraverserMixin):
        def render(self, traverser, element, *args, **kwargs):
            #print ' ' * 4 * kwargs.get('level') + ' cairo %s: %s ' % (element.cmd, element.args)
            #print 'set_source_rgb ', element.args

            if element.cmd == 'fill':
                traverser.fill_color = element.args
            elif element.cmd == 'fill':
                traverser.stroke_color = element.args

            if len(args) == 3:
                traverser.ctx.set_source_rgb(*element.args)
            elif len(args) == 4:
                traverser.ctx.set_source_rgb(*element.args)

    class Path(TraverserMixin):
        class PathElement(CmdMxin):
            def lineto(self, traverser, x, y):
                traverser.ctx.line_to(x, y)

            def moveto(self, traverser, x, y):
                traverser.ctx.move_to(x, y)

            def rect(self, traverser, width, height):
                traverser.ctx.rectangle(0, 0, width, height)

        def leave(self, traverser, element, *args, **kwargs):
            """
            BUG - This is just wrong, shouldn't be setting color here
            """
            #print ' ' * 4 * kwargs.get('level') + 'leave cairo path'

            if traverser.fill_color is not None:
                traverser.ctx.set_source_rgba(*traverser.fill_color)
                traverser.ctx.fill()
            elif traverser.stroke_color is not None:
                traverser.ctx.set_source_rgba(*traverser.stroke_color)
                traverser.ctx.stroke()


def render(scenegraph, ctx):
    canvas = Canvas(ctx)
    canvas.rendergraph(None, scenegraph, level=0, ctx=ctx)

