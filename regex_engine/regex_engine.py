class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        def check_eq_len(r, t):
            if r == "":
                return True
            if t == "":
                return False
            if r[0] != "." and r[0] != t[0]:
                return False    
            return check_eq_len(r[1:], t[1:])        
            
        def invoke_check(r, t):
            for i in range(0, len(t) - len(r) + 1):
                if check_eq_len(r , t[i:]):
                    return True
            else:
                return False

        self.out = invoke_check(self.regex, self.terminal_input)
        return self.out

    def output(self):
        print(f"Input: '{self.regex}|{self.terminal_input}'\tOutput: {self.out}")


def main():
    regex_input = input("Enter a 'pattern|string_to_compare' input: ")

    engine = Regex_Engine(regex_input)
    engine.compare()
    engine.output()
    
    
if __name__ == "__main__":
    main()