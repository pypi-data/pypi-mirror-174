class Latex:
    delimiter = '$$'

    def __init__(self, latex):
        self.latex = latex

    def _repr_latex_(self):
        return ' {} {} {} '.format(
            self.delimiter, self.latex, self.delimiter
        )

    def __add__(self, other):
        if isinstance(other, str):
            other = Latex(other)
        return Latex(self.latex + ' ' + other.latex)

    def __radd__(self, other):
        return Latex(other + ' ' + self.latex)


class LatexInline(Latex):
    delimiter = '$'


class Text(Latex):
    delimiter = '$'

    def __init__(self, text):
        self.latex = r'\mbox{%s}' % text


class Output:

    def __init__(self):
        self.lines = []

    def _to_latex(self, text):
        if isinstance(text, str):
            return Latex(text)
        return text

    def append(self, text):
        self.lines.append(self._to_latex(text))

    def _repr_latex_(self):
        out = ''
        for line in self.lines:
            out += line._repr_latex_()
        return out