import numpy as np

from interpreter.definitions.tableaux_tree import Node


def to_latex():
    # Maybe view the source code for tables by the 'tabulate' package and then modify:
    # https://www.logicmatters.net/resources/pdfs/L4LProoftrees.pdf
    # This might be simpler: http://davidagler.com/projects/LatexAndSymLogic_AnIntroduction.pdf
    pass

# to pdf using pylatex
def to_pdf(tableaux:Node, headers:(str or list)) -> None:
    pass

# to image
def to_image(tableaux:Node, im_specs:dict) -> None:
    pass







