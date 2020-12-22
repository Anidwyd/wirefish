import urwid
import os

class TraceTreeWidget(urwid.TreeWidget):
    """ Display widget for leaf nodes """
    def get_display_text(self):
        depth = self.get_node().get_depth()
        text = self.get_node().get_value()['name']
        if depth == 1 or depth == 2:
            return ( ['frame', 'protocol'][depth-1], ' ' + text)
        return ( 'body', text )



class TraceNode(urwid.TreeNode):
    """ Structure de données pour les feuille. """
    def load_widget(self):
        return TraceTreeWidget(self)



class TraceParentNode(urwid.ParentNode):
    """ Structure de données pour les noeuds parents. """
    def load_widget(self):
        return TraceTreeWidget(self)


    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))


    def load_child_node(self, key):
        """ Retourne soit un TraceNode soit un TraceParentNode """
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = TraceParentNode
        else:
            childclass = TraceNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)
    


class Interface:
    palette = [
        ('head', 'light blue', 'black', 'standout'),
        ('body', 'white', 'black'),
            ('frame', 'black', 'light green'),
            ('protocol', 'black', 'dark cyan'),
        ('foot', 'white', 'black'),
            ('version', 'white', 'black', 'bold'),
            ('key', 'dark gray', 'black','underline'),
            ('quit', 'light red, bold', 'black'),
        ('error', 'dark red', 'black'),
        ]

    footer_text = [
        ('version', "WireFish 1.0"), "              ",
        ('key', "HAUT"), ",", ('key', "BAS"), ",", ('key', "GAUCHE"), "    ",
        ('key', "HAUT"), ",", ('key', "BAS DE PAGE"),"    ",
        ('key', "+"), ",",
        ('key', "-"), "     ",
        ('key', "DEBUT"), ",",
        ('key', "FIN"), "    ",
        ('quit', "Q"),
        ]
    

    def __init__(self, data=None):

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../data/text.txt')

        with open(filename, 'r') as f:
            self.header = urwid.Text( u"".join(f.readlines()), align='center' )

        self.trace_tree = urwid.TreeListBox(urwid.TreeWalker(TraceParentNode(data)))
        self.trace_tree.offset_rows = 1
        self.res_box = urwid.LineBox(urwid.Padding(self.trace_tree, left=1, right=1))
        
        self.footer = urwid.AttrWrap( urwid.Text( self.footer_text ), 'foot')

        # Assembler les widgets pour construire le layout
        self.layout = urwid.Frame(
            header=urwid.AttrWrap(self.header, 'head' ),
            body=urwid.AttrWrap( self.res_box, 'body' ),
            footer=self.footer )


    def main(self):
        """ Lance le programme. """
        
        self.loop = urwid.MainLoop(self.layout, self.palette,
            unhandled_input=self.unhandled_input)
        self.loop.run()


    def unhandled_input(self, k):
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()