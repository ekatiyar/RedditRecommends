class Num:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return self.value%2

    def __repr__(self):
        return str(self.value)

print(set([Num(x) for x in range(10)]))