import sys

class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        def consume(r, t):
            if r == "":
                return True
            if len(t) != len(r):
                return False
            if t == "":
                return False
            if r[0] != "." and r[0] != t[0]:
                return False 
            return consume(r[1:], t[1:])        
            
        def invoke_check(r, t):
            len_r = len(r) - 1
            if r.startswith("^") and r.endswith("$"):
                return consume(r[1:-1], t)
            if r.startswith("^"):
                return consume(r[1:], t[:len_r])
            if r.endswith("$"):
                return consume(r[:-1], t[-len_r:])

            return consume(r, t)

        self.out = invoke_check(self.regex, self.terminal_input)
        return self.out

    def output(self):
        print(f"Input: '{self.regex}|{self.terminal_input}'\tOutput: {self.out}")


def main():
    sys.setrecursionlimit(10000)
    regex_input = input()

    engine = Regex_Engine(regex_input)
    engine.compare()
    engine.output()
    
    
if __name__ == "__main__":
    main()