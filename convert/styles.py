import numpy as np

from interpreter.definitions.tokens import TokenType, Token

########### STYLES ###########
# Standard style
style_1 = {TokenType.TRUE: "T", TokenType.FALSE: "F", TokenType.PROPVAR: lambda x: x.value, TokenType.NEGATION: "~", TokenType.DISJUNCTION: "|",
           TokenType.CONJUNCTION: "&", TokenType.IMPLICATION: ">", TokenType.CONVERSEIMPLICATION: "<", 
           TokenType.BICONDITIONAL: "<>", TokenType.LPAREN: "(", TokenType.RPAREN: ")"}

style_1_ltx = {TokenType.TRUE: "T", TokenType.FALSE: "F", TokenType.PROPVAR: lambda x: x.value, TokenType.NEGATION: "$\\neg$", TokenType.DISJUNCTION: "$\\lor$",
              TokenType.CONJUNCTION: "$\\land$", TokenType.IMPLICATION: "$\\rightarrow$", TokenType.CONVERSEIMPLICATION: "$\leftarrow$", 
              TokenType.BICONDITIONAL: "$\\leftrightarrow$", TokenType.LPAREN: "$($", TokenType.RPAREN: "$)$"}


style_dict = {"style_1": style_1, "style_1_ltx": style_1_ltx}

########### STYLE CONVERTERS ###########
def style_converter_token(inp:Token, style_str:str="style_1"):
    """
    Args:
        inp (Token): the token who's style is to be converted
        style_str (str): the style 

    Returns (str):
        Token, but in the style of 'style_str'
    """

    style = style_dict[style_str]
    t_type = inp.type
    converted = style[t_type]
    if type(converted) == str:
        return converted
    elif callable(converted):
        return converted(inp)
    else:
        print(f"Error, could not style '{inp}' using style: '{style_str}'")

def style_converter_truth_table(truth_table:list, style_str:str="style_1"):
    n_truth_table = truth_table

    def handle_header(elem:(list or str), depth=0):
        ret_str = ""

        if isinstance(elem, (list, tuple)):
            if depth > 0: ret_str += "(";
            for el in elem:
                ret_str += handle_header(el, depth=(depth + 1))
            if depth > 0: ret_str += ")"
        else:
            ret_str += style_converter_token(inp=elem, style_str=style_str)
        
        return ret_str

    for i, column in enumerate(truth_table):
        for j, elem in enumerate(column):
            if type(elem) == list:
                header = handle_header(elem)
                    # header += style_converter_token(inp=f, style_str=style_str)
                n_truth_table[i][j] = header
                
            else:
                n_truth_table[i][j] = style_converter_token(inp=elem, style_str=style_str)

    print(f"Truth table: \n{truth_table}")

    return n_truth_table


