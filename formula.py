import random
import string

from sympy.parsing.latex import parse_latex
from texteller import load_model, load_tokenizer, img2latex

class Formula():
    def __init__(self):
        model     = load_model(use_onnx=False)
        tokenizer = load_tokenizer()

        self.model = model
        self.tokenizer = tokenizer

    def get_random_filename(self, len: int = 8):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=len))
        
        return filename

    def detect_latex(self, img):
        latex = img2latex(
            self.model, 
            self.tokenizer, 
            img
        )[0]

        return latex
    
    def convert_latex_to_formula(self, ltx):
        latex = ltx.strip()
        if latex.startswith(r'\[') and latex.endswith(r'\]'):
            latex = latex[2:-2].strip()

        expr_eq  = parse_latex(latex)
        expr_att = dir(expr_eq)

        if 'lhs' in expr_att and 'rhs' in expr_att:
            return f"{expr_eq.lhs} = {expr_eq.rhs}"
        
        return str(expr_eq)

    def detect_formula(self, img: list):
        latex   = self.detect_latex(img)
        formula = self.convert_latex_to_formula(latex)
        
        return formula