

class Node: 
    # Initialize the attributes of Node
    def __init__(self, formula=None, truth=None, decomp_rule=None):
        self.left = None # Left Child
        self.right = None # Right Child
        self.idx = None # The index of the formula
        self.formula = formula # Node Data
        self.truth = truth # The truth of the formula
        self.decomp_rule = decomp_rule # The decomposition rule used to get this node

    def __repr__(self):
        right_str = f"\n\n Right: \n\t {self.right}" if self.right else ""
        left_str = f"\n\n Left: \n\t {self.left}" if self.left else ""

        return f"Idx: [{self.idx}] - Formula: {self.formula}: {self.truth}{left_str}{right_str}"

