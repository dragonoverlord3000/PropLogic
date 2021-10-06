import numpy as np
from tabulate import tabulate

from convert.styles import style_converter_token, style_converter_truth_table

# Identify the main logical connectives in each column in the truth table and then just rearrange some stuff
def to_minimal_truth_table(truth_table:list, verbose:bool) -> list:
    """
    Args:
        truth_table (list): the truth table from 'interpreter.setup_truth_table' or the 'minimal' version of it
        verbose (bool): whether to print the output immediately or not

    Returns (list):
        Minimal version of the truth table
    """
    pass

# to latex using 'tabulate'
def to_latex(truth_table:list, headers:(str or list)="firstrow", verbose:bool=False, style:str="style_1_ltx") -> str:
    """
    Args:
        truth_table (list): the truth table from 'interpreter.setup_truth_table' or the 'minimal' version of it
        verbose (bool): whether to print the output immediately or not
        headers (str, list): either specify the headers using a string or provide a list of headers

    Returns (str):
        String of latex code
    """
    tt = style_converter_truth_table(truth_table, style)
    latexified_tt = tabulate(tt, headers=headers, tablefmt="latex_raw", stralign="center")
    if verbose: print(latexified_tt);
    return latexified_tt

# to html using 'tabulate'
def to_html(truth_table:list, headers:(str or list)="firstrow", verbose:bool=False, style:str="style_1") -> str:
    """
    Args:
        truth_table (list): the truth table from 'interpreter.setup_truth_table' or the 'minimal' version of it
        verbose (bool): whether to print the output immediately or not
        headers (str, list): either specify the headers using a string or provide a list of headers

    Returns (str):
        String of latex code
    """
    tt = style_converter_truth_table(truth_table, style)
    htmlified_tt = tabulate(truth_table, headers=headers, tablefmt="latex", stralign="center")
    if verbose: print(htmlified_tt);
    return htmlified_tt


# to pdf using pylatex
def to_pdf(truth_table:list, headers:(str or list)) -> None:
    pass

# to image
def to_image(truth_table:list, im_specs:dict) -> None:
    pass

















