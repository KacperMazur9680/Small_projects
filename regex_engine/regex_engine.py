class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        def recursive_regex(r, t):
            if r == "":
                return True
            if len(r) != len(t):
                return False
            if r[0] != "." and r[0] != t[0]:
                return False
            
            return recursive_regex(r[1:], t[1:])

        self.out = recursive_regex(self.regex, self.terminal_input)
        return self.out

    def output(self):
        print(f"Input: '{self.regex}|{self.terminal_input}'\tOutput: {self.out}")


def main():
    regex_input = input()

    engine = Regex_Engine(regex_input)
    engine.compare()
    engine.output()
    
    
if __name__ == "__main__":
    main()