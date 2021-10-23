##### IMPORTS #####
import numpy as np
from tabulate import tabulate

from interpreter.definitions.truth_table import truth_table_dict
from interpreter.definitions.decomp_rules import decomp_rule_dict
from interpreter.definitions.tableaux_tree import Node
from interpreter.definitions.tokens import TokenType, Token
from math import floor
import time


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

        while len(evaluated) > 1 and ((time.time() - start_time) < run_time):
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
                - latex -> will print a string of latex code by creating a pdf (using 'tabulate')
        
        Returns (png file, str, pdf file):
            Depends on the 'style' you choose

        Note: I could just use `self.calculate_truth_assignment` on all permutations of truth assignments,
        but that would be a very ineffective solution since I would be calculating every truth value from
        the beginning every time - so this implementation is more effective.
        """

        RPN = self.RPN_input
        prop_vars_temp = [var for var in RPN if var.type == TokenType.PROPVAR]
        prop_var_vals, prop_vars = [], []
        for prop_var in prop_vars_temp:
            if not prop_var.value in prop_var_vals:
                prop_vars.append(prop_var)
                prop_var_vals.append(prop_var.value)

        connects = [con for con in RPN if con.type in connectives]
        num_connects = len(connects)
        num_prop_vars = len(prop_vars)

        # Populate the first columns with all possible permutations of initial truth assignments
        # Note that a dictionary is used since it's easier to refer to a specific column this way
        truth_table = {}
        for n, prop_const in enumerate(prop_vars):
            num_flips = 2**(n + 1)
            num_rows = 2**num_prop_vars
            bools = [Token(TokenType.TRUE), Token(TokenType.FALSE)]
            col_i = [bools[floor(num_flips/num_rows * x) % 2] for x in range(num_rows)]
            truth_table[prop_const.value] = col_i

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
                if temp_RPN[idx - 1].type in symbol_types and temp_RPN[idx - 2].type in symbol_types:

                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx-2].value][n], truth_table[temp_RPN[idx-1].value][n]))

                    subformulas.append([temp_RPN[idx-2]] + [temp_RPN[idx]] + [temp_RPN[idx-1]])
                
                # Is this case even possible ???
                elif temp_RPN[idx - 1].type in symbol_types and temp_RPN[idx - 2].type == TokenType.SUBSTVAR:
                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx-1].value][n], truth_table[temp_RPN[idx - 2].value][n]))

                    subformulas.append([subformulas[-1]] + [temp_RPN[idx]] + [temp_RPN[idx-1]])

                elif temp_RPN[idx - 1].type == TokenType.SUBSTVAR and temp_RPN[idx - 2].type in symbol_types:
                    for n in range(2**num_prop_vars):
                        temp_column.append(truth_table_dict[temp_RPN[idx].type](truth_table[temp_RPN[idx - 2].value][n], truth_table[temp_RPN[idx-1].value][n]))

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
                truth_table[substvar.value] = temp_column # Test
                identifier += 1
                idx -= 2 # We remove three characters and add one, so our index should go two back

            idx += 1

        top_row = prop_vars + subformulas
        
        ret_truth_table = []
        num_substvar = 0
        for header in top_row:
            if type(header) == list:
                ret_truth_table.append([subformulas[num_substvar]] + truth_table[num_substvar])
                num_substvar += 1
            elif header.type == TokenType.PROPVAR:
                ret_truth_table.append([[header]] + truth_table[header.value])
            else:
                print(f"\nError, could not convert/identify {header}")

        # Transpose the truth table - https://stackoverflow.com/a/6473727/13096923
        ret_truth_table = np.array(ret_truth_table).T.tolist()
        return ret_truth_table

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
        # https://stackoverflow.com/questions/7670280/tree-plotting-in-python
        pass

    def tableau_method(self, assump=True) -> str:         
        # https://plotly.com/python/tree-plots/#create-text-inside-the-circle-via-annotations
        
        RPN = self.RPN_input
        prefix = RPN[::-1] # Note this isn't exactly prefix - the order of symbols are swapped! This is important and is reflected in some assymeytries in the code - like 'node 1' having the truth value 'True'

        # class Node: 
        #     # Initialize the attributes of Node
        #     def __init__(self, formula=None, truth=None, decomp_rule=None):
        #         self.left = None # Left Child
        #         self.right = None # Right Child
        #         self.idx = None # The index of the formula
        #         self.formula = formula # Node Data
        #         self.truth = truth # The truth of the formula
        #         self.decomp_rule = decomp_rule # The decomposition rule used to get this node

        #     def __repr__(self):
        #         right_str = f"\n\n Right: \n\t {self.right}" if self.right else ""
        #         left_str = f"\n\n Left: \n\t {self.left}" if self.left else ""

        #         return f"Idx: [{self.idx}] - Formula: {self.formula}: {self.truth}{left_str}{right_str}"

        # Creates the tree recursively <3
        def setup_tree(prefix, truth=True):
            skip_total = 1
            root = Node(truth=truth)
            token = prefix[0]

            if token.type in symbol_types:
                root.formula = [token]

            elif token.type in unary_connectives:
                _, bool_val = decomp_rule_dict[token.type](truth)[0]
                node, skip_add = setup_tree(prefix[1:], bool_val)
                skip_total += skip_add
                root.formula = [token, Token(TokenType.LPAREN)] + node.formula + [Token(TokenType.RPAREN)]
                root.left = node

            elif token.type in binary_connectives:
                decomp = decomp_rule_dict[token.type](truth)
                if len(decomp) == 1:
                    _, bool_val_1, bool_val_2 = decomp[0]
                    node_1, skip_add = setup_tree(prefix[1:], truth=bool_val_2)
                    skip_total += skip_add
                    node_2, skip_add = setup_tree(prefix[skip_total:], truth=bool_val_1)
                    skip_total += skip_add
                    root.formula = [Token(TokenType.LPAREN)] + node_2.formula + [token] + node_1.formula + [Token(TokenType.RPAREN)]
                    if bool_val_1 != None and bool_val_2 != None:
                        root.left = [node_2, node_1]
                    elif bool_val_1 != None and bool_val_2 == None:
                        root.left = node_1
                    elif bool_val_1 == None and bool_val_2 != None:
                        root.left = node_2 

                if len(decomp) == 2:
                    skip_total_extra = skip_total
                    (_, bool_val_1, bool_val_2), (_, bool_val_3, bool_val_4) = decomp[0], decomp[1]

                    node_1, skip_add = setup_tree(prefix[1:], truth=bool_val_2)
                    skip_total += skip_add
                    node_2, skip_add = setup_tree(prefix[skip_total:], truth=bool_val_1)
                    skip_total += skip_add

                    node_3, skip_add = setup_tree(prefix[1:], truth=bool_val_4)
                    skip_total_extra += skip_add
                    node_4, skip_add = setup_tree(prefix[skip_total_extra:], truth=bool_val_3)
                    skip_total_extra += skip_add

                    root.formula = [Token(TokenType.LPAREN)] + node_2.formula + [token] + node_1.formula + [Token(TokenType.RPAREN)]

                    if bool_val_1 != None and bool_val_2 != None:
                        root.left = [node_2, node_1]
                    elif bool_val_1 != None and bool_val_2 == None:
                        root.left = node_2
                    elif bool_val_1 == None and bool_val_2 != None:
                        root.left = node_1

                    if bool_val_3 != None and bool_val_4 != None:
                        root.right = [node_4, node_3]
                    elif bool_val_3 != None and bool_val_4 == None:
                        root.right = node_4
                    elif bool_val_3 == None and bool_val_4 != None:
                        root.right = node_3
            
            return root, skip_total

        tree, _ = setup_tree(prefix)
        return tree


                


    def check_tautology(self) -> bool:
        """
        Should maybe be a part of the 'tableau_method' method
        """
        pass

    def CLI_printer(self, truth_table, headers="firstrow"):
        print(tabulate(truth_table, headers=headers))

    def RPN_to_Infix(self, RPN):
        pass








