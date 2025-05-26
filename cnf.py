from typing import NamedTuple, Self


class Cnf(NamedTuple):
    clauses: list[list[int]]
    num_variables: int
    num_clauses: int

    def test(self, bits: str | list[int]) -> list[int]:
        _bits: list[int]
        if type(bits) is str:
            _bits = list(map(int, bits))
        else:
            _bits = bits

        return all(
            any((_bits[abs(literal) - 1] > 0) == (literal > 0) for literal in clause)
            for clause in self.clauses
        )

    def test_all(self):
        pass

    @classmethod
    def from_dimacs(cls, dimacs: str | list[str]) -> Self:
        clauses = []
        has_header = False
        for line in dimacs.splitlines():
            line = line.strip()
            tokens = line.split()
            if line == "" or tokens[0] == "c":
                pass
            elif tokens[0] == "p":
                assert not has_header
                assert tokens[1] == "cnf"
                has_header = True
                num_variables = int(tokens[2])
                num_clauses = int(tokens[3])
            else:
                clause = [int(x) for x in tokens[:-1]]
                clauses.append(clause)

        return Cnf(clauses, num_variables, num_clauses)

    @classmethod
    def from_dimacs_file(cls, file_path: str) -> Self:
        with open(file_path, "r") as file:
            return cls.from_dimacs(file.read())
