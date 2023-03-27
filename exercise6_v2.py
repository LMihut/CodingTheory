import pyfinite
from pyfinite import ffield


class FiniteField:

    def __init__(self, n):
        self.n = 2**n
        self.F = ffield.FField(n)
        print(f"> irreducible polynomial: {self.F.ShowPolynomial(self.F.generator)}")

    def logarithm(self, alpha, x):
        a = alpha
        k = 1

        while a != x:
            k += 1
            a = self.F.DoMultiply(a, alpha)
        
        return k

    def exponentation(self, x, k):
        result = 1
        for _ in range(k):
            result = self.F.DoMultiply(result, x)

        return result

    def calculate_all_generators(self, verbose=False):
        generators = []
        for alpha in range(2, self.n):
            a = alpha
            k = 1

            while a != 1:
                k += 1
                a = self.F.DoMultiply(a, alpha)

            if k == self.n - 1:
                if verbose:
                    print(f">> found generator: {self.F.ShowPolynomial(alpha)}")

                generators.append(alpha)

        print(f"> found {len(generators)} generators", generators)
        return generators

    def p(self, x):
        coefficients = self.F.ShowCoefficients(self.F.generator)
        exponents = [k for k, c in enumerate(coefficients[::-1]) if c]

        result = 0
        for k in exponents:  
            result = self.F.Add(result, self.exponentation(x, k))

        return result 

    def roots(self, verbose=False):
        generators = self.calculate_all_generators()
        roots = []
        for a in generators:
            if self.p(a) == 0:
                if verbose:
                    print(f">> found root of p for a = {self.F.ShowPolynomial(a)}")
                roots.append(a)
        minroot = min(roots)
        # print(f"> found {len(roots)} roots", roots)
        return minroot

    def show_polynomial(self, x):
        return self.F.ShowPolynomial(x)

    
if __name__ == "__main__":
    F = FiniteField(3)
    roots = F.roots()
    print(f">> root: {F.show_polynomial(roots)}")
