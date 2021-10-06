##### IMPORTS #####
import numpy as np

from truth_table import truth_table_dict
from tokens import TokenType, Token
from math import floor
import time

from tabulate import tabulate

##### VARIABLES #####
connectives = [TokenType.NEGATION, TokenType.CONJUNCTION, TokenType.DISJUNCTION, 
                  TokenType.IMPLICATION, TokenType.CONVERSEIMPLICATION,
                  TokenType.BICONDITIONAL]
unary_connectives = [TokenType.NEGATION]
binary_connectives = [TokenType.CONJUNCTION, TokenType.DISJUNCTION, 
                      TokenType.IMPLICATION, TokenType.CONVERSEIMPLICATION,
                      TokenType.BICONDITIONAL]

symbol_types = [TokenType.TRUE, TokenType.FALSE, TokenType.PROPVAR]

##### FUNCTIONS #####
def extract_propositional_vars(tokens:list) -> list:
    """
    Args:
        tokens (list): list of all the tokens generated

    Returns (list):
        a set of the propositional variables in the expression - in list format
    """
    pass

def order_propositional_vars(prop_vars:list, order:list = []) -> list:
    """
    Args: 
        prop_vars (list): list of the propositional variables
        order (list): the ordering of the propositional variables
            - default is [] which is interpreted as 'alphabetic order'
    """
    ordered_prop_vars = []

    if len(order) == 0:
        # alphabetize
        pass
    elif len(order) == len(prop_vars):
        ordered_prop_vars = prop_vars
    
    else:
        print(f"Given order '{order}' does not have the same number of elements as the given propositional variables '{prop_vars}'")
        ordered_prop_vars = prop_vars

    return ordered_prop_vars


##### INTERPRETER #####
class Interpreter:
    def __init__(self, RPN:list) -> None:
        self.RPN_input = RPN

    def calculate_truth_assignment(self, truth_assignment:dict = {}, run_time:float = 10.0, RPN=None) -> TokenType:
        """
        Args:
            truth_assignment_dict (dict): a dictionary relating every truth propositional variable to a truth assignment e.g. {"a": True, "b": False, ..., "c": True}
            run_time (float): the time in seconds before throwing a run time error

        Returns (TokenType):
            Will return TokenType.TRUE or TokenType.FALSE depending on what the expression and truth assignment evaluated to
        """

        evaluated = RPN if RPN else self.RPN_input
        idx = 0
        start_time = time.time()

        while len(evaluated) > 1 and time.time() - start_time < run_time:
            # Handle propositional variables according to the given truth assignment
            if evaluated[idx].type == TokenType.PROPVAR:
                evaluated[idx] = Token(TokenType.TRUE) if truth_assignment[evaluated[idx].value] else Token(TokenType.FALSE)

            # Handle unary connectives
            elif evaluated[idx].type in unary_connectives:
                evaluated = evaluated[:idx - 1] + [truth_table_dict[evaluated[idx].type](evaluated[idx-1])] + evaluated[idx+1:]
                idx -= 1 # We remove two characters and add one, so our index should go one back

            # Handle binary connectives 
            elif evaluated[idx].type in binary_connectives:
                evaluated = evaluated[:idx-2] + [truth_table_dict[evaluated[idx].type](evaluated[idx-2], evaluated[idx-1])] + evaluated[idx+1:]
                idx -= 2 # We remove three characters and add one, so our index should go two back

            idx += 1

        if len(evaluated) > 1:
            print(f"Error, maximum allotted run time, ('{run_time}'), exceeded")
        
        return evaluated[0]

    def setup_truth_table(self, style="array"):
        """
        Args:
            style (str): the style to print the table in, there is support for:
                - array -> will return a truth table array
                - png -> will create a PNG image of the truth table
                - pdf -> will create a pdf (using PyLatex)
                - latex -> will print a string of latex code by creating a pdf (using PyLatex) and then reading off the table part of the '.tex' file
        
        Returns (png file, str, pdf file):
            Depends on the 'style' you choose

        Note: I could just use `self.calculate_truth_assignment` on all permutations of truth assignments,
        but that would be a very ineffective solution since I would be calculating every truth value from
        the beginning every time - so this implementation is more effective.
        """

        # https://github.com/JAEarly/latextable and https://colab.research.google.com/drive/1Iq10lHznMngg1-Uoo-QtpTPii1JDYSQA?usp=sharing#scrollTo=K7NNR1Vg40Vo

        RPN = self.RPN_input
        prop_vars_temp = [var for var in RPN if var.type == TokenType.PROPVAR]
        prop_var_vals, prop_vars = [], []
        for prop_var in prop_vars_temp:
            if not prop_var.value in prop_var_vals:
                prop_vars.append(prop_var)
                prop_var_vals.append(prop_var.value)

        connects = [con for con in RPN if con.type in connectives]

        print(f"\nPropositional variables: {prop_vars}")

        num_prop_vars = len(prop_vars)
        num_connects = len(connects)

        # Populate the first columns with all possible permutations of initial truth assignments
        # Note that a dictionary is used since it's easier to refer to a specific column this way
        truth_table = {}
        for n, prop_const in enumerate(prop_vars):
            num_flips = 2**(n + 1)
            num_rows = 2**num_prop_vars
            bools = [Token(TokenType.TRUE), Token(TokenType.FALSE)]
            col_i = [bools[floor(num_flips/num_rows * x) % 2] for x in range(num_rows)]
            truth_table[prop_const.value] = col_i

        print(f"\nInitial truth assignment: {truth_table}")

        # So ideally - I should calculate the values in the truth table in this while loop which creates the uppermost rows containing the propositional formulas
        subformulas = []
        temp_RPN = RPN
        identifier = 0
        idx = 0
        while len(temp_RPN) > 1:
            temp_column = [] # Testing ???

            # Handle unary connectives
            if temp_RPN[idx].type in unary_connectives:
                if temp_RPN[idx - 1].type == TokenType.SUBSTVAR:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx - 1].value][n]))

                    subformulas.append([temp_RPN[idx]] + [subformulas[-1]])

                elif temp_RPN[idx - 1].type in symbol_types:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx-1].value][n]))

                    subformulas.append([temp_RPN[idx]] + [temp_RPN[idx - 1]])

                else:
                    subformulas.append([temp_RPN[idx]] + [temp_RPN[idx - 1]]) # default
                    print(f"Error, can't take '{temp_RPN[idx]}' of '{temp_RPN[idx - 1]}'")
                substvar = Token(TokenType.SUBSTVAR, identifier)
                temp_RPN = temp_RPN[:idx - 1] + [substvar] + temp_RPN[idx+1:]
                truth_table[substvar.value] = temp_column # Test
                identifier += 1
                idx -= 1 # We remove two characters and add one, so our index should go one back

            # Handle binary connectives 
            elif temp_RPN[idx].type in binary_connectives:
                print(f"\nTemp_RPN type idx1: {temp_RPN[idx-1].type}")
                print(f"Temp_RPN type idx2: {temp_RPN[idx-2].type}")

                if temp_RPN[idx - 1].type in symbol_types and temp_RPN[idx - 2].type in symbol_types:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx-2].value][n], truth_table[temp_RPN[idx-1].value][n]))

                    subformulas.append([temp_RPN[idx-2]] + [temp_RPN[idx]] + [temp_RPN[idx-1]])
                
                elif temp_RPN[idx - 1].type in symbol_types and temp_RPN[idx - 2].type == TokenType.SUBSTVAR:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx - 2].value][n], truth_table[temp_RPN[idx-1].value][n]))

                    subformulas.append([subformulas[-1]] + [temp_RPN[idx]] + [temp_RPN[idx-1]])

                elif temp_RPN[idx - 1].type == TokenType.SUBSTVAR and temp_RPN[idx - 2].type in symbol_types:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx-1].value][n], truth_table[temp_RPN[idx - 2].value][n]))

                    subformulas.append([temp_RPN[idx-2]] + [temp_RPN[idx]] + [subformulas[-1]])

                elif temp_RPN[idx - 1].type == TokenType.SUBSTVAR and temp_RPN[idx - 2].type == TokenType.SUBSTVAR:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx - 2].value][n], truth_table[temp_RPN[idx - 1].value][n]))

                    subformulas.append([subformulas[-2]] + [temp_RPN[idx]] + [subformulas[-1]])

                else:
                    subformulas.append([temp_RPN[idx-2]] + [temp_RPN[idx]] + [temp_RPN[idx-1]]) # default
                    print(f"Error, can't take '{temp_RPN[idx]}' of '{temp_RPN[idx - 1]}' and '{temp_RPN[idx - 2]}'")

                substvar = Token(TokenType.SUBSTVAR, identifier)
                temp_RPN = temp_RPN[:idx-2] + [substvar] + temp_RPN[idx+1:]
                print(f"temp_column: {temp_column}")
                truth_table[substvar.value] = temp_column # Test
                identifier += 1
                idx -= 2 # We remove three characters and add one, so our index should go two back

            idx += 1

        top_row = prop_vars + subformulas
        print(f"\nTop row: {top_row}")
        print(f"\nTruth table: {truth_table}")
        print(f"\nSubformulas: {subformulas}")
        # Table should be (2**num_prop_vars + 1) x (num_prop_vars + num_connectives)

        return truth_table, top_row

    def truth_table_converter(self, truth_table,  top_row="firstrow", convert_from=list, convert_to="latex"):
        """
        Args:
            truth_table (list, np.array): the truth table to convert
            top_row (str, list): list with the top row or string specifying the top row - the top row will act as a header
            convert_from (type, str): type of truth table to convert from e.g. list
            convert_to (type, str): type of truth table to convert to e.g. latex

        Returns (list, np.array, str):
            The type specified in the 'convert_to' parameter
        """

        headers = []
        if isinstance(top_row, (list, np.array)):
            headers = top_row
        elif top_row == "firstrow":
            headers = top_row

        if type(np.array()) in convert_from or list in convert_from:
            if convert_to == "latex":
                return tabulate(truth_table, headers=headers, tablefmt='latex')
            pass

        pass

    def minimal_truth_table(self, style="array"):
        # Could just run 'setup_truth_table' and then interpret the result
        pass

    def create_parse_tree(self) -> str:
        """
        https://stackoverflow.com/questions/7670280/tree-plotting-in-python
        """
        pass

    def tableau_method(self) -> str:
        # https://plotly.com/python/tree-plots/
        # https://github.com/JAEarly/latextable
        pass

    def check_tautology(self) -> bool:
        """
        Should maybe be a part of the 'tableau_method' method
        """
        pass










