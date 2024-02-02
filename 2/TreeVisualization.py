import graphviz
from node import Node

def inorder_traversal(root, dot, codebook, code=''):
    if isinstance(root, Node):
        inorder_traversal(root.zero, dot, codebook, code+'0')
        dot.node(str(code), label=str(code))
        if isinstance(root.zero, Node):
            dot.edge(str(code+'0'), str(code), style='dotted')
        elif isinstance(root.zero, bytes):
            dot.edge(str(root.zero), str(code), style='dotted')
        if isinstance(root.one, Node):
            dot.edge(str(code), str(code+'1'), style='dotted')
        elif isinstance(root.one, bytes):
            dot.edge(str(code), str(root.one), style='dotted')
        inorder_traversal(root.one, dot, codebook, code+'1')
    elif isinstance(root, bytes):
        dot.node(str(root) , label=str(root)+ ' : ' + code )

def preorder_traversal(root, dot, codebook, code=''):
    if isinstance(root, Node):
        dot.node(str(code), label=code)
        if isinstance(root.zero, Node):
            dot.edge(str(code), code+'0', style='dotted')
        elif isinstance(root.zero, bytes):
            dot.edge(str(code), code+'0', style='dotted')
        if isinstance(root.one, Node):
            dot.edge(str(code), code+'1', style='dotted')
        elif isinstance(root.one, bytes):
            dot.edge(str(code), code+'1', style='dotted')
        preorder_traversal(root.zero, dot, codebook, code+'0')
        preorder_traversal(root.one, dot, codebook, code+'1')
    elif isinstance(root, bytes):
        dot.node(str(root) , label=str(root)+ ' : ' + code )

def postorder_traversal(root, dot, codebook, code=''):
    if isinstance(root, Node):
        postorder_traversal(root.zero, dot, codebook, code+'0')
        postorder_traversal(root.one, dot, codebook, code+'1')
        dot.node(str(code), label=str(code))
        if isinstance(root.zero, Node):
            dot.edge(str(code+'0'), str(code), style='dotted')
        elif isinstance(root.zero, bytes):
            dot.edge(str(root.zero), str(code), style='dotted')
        if isinstance(root.one, Node):
            dot.edge(str(code+'1'), str(code), style='dotted')
        elif isinstance(root.one, bytes):
            dot.edge(str(root.one), str(code), style='dotted')
    elif isinstance(root, bytes):
        dot.node(str(root) , label=str(root)+ ' : ' + code )

def visualize_binary_tree(root, codebook):
    dot_inorder = graphviz.Digraph(comment='Inorder Traversal')
    inorder_traversal(root, dot_inorder, codebook)
    dot_inorder.render('inorder_traversal', view=True, format='png')

    dot_preorder = graphviz.Digraph(comment='Preorder Traversal')
    preorder_traversal(root, dot_preorder, codebook)
    dot_preorder.render('preorder_traversal', view=True, format='png')

    dot_postorder = graphviz.Digraph(comment='Postorder Traversal')
    postorder_traversal(root, dot_postorder, codebook)
    dot_postorder.render('postorder_traversal', view=True, format='png')
