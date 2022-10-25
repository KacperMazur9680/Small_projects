class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        def consume(r, t):
            print(r , t)
            if r == "":
                return True
            if r == "$" and t == "":
                return True
            if r == "$" and t != "":
                return False
            if t == "":
                return False
            if r[0] != "." and r[0] != t[0]:
                return False 
            return consume(r[1:], t[1:])        
            
        def invoke_check(r, t): 
            if r.startswith("^"):
                r = r.replace("^", "")   
                if r[0] != t[0]:
                    return False
                for i in range(0, len(t) + len(r)):
                    # print(i)
                    if consume(r , t[i:]):
                        return True
                else:
                    return False

            elif r.endswith("$"):
                for i in range(0, len(t) + len(r)):
                    # print(i)
                    if consume(r, t[i:]):
                        return True
                else:
                    return False
            
            else:                  
                for i in range(0, len(t) - len(r) + 1):
                    # print(i)
                    if consume(r , t[i:]):
                        return True
                else:
                    return False

        self.out = invoke_check(self.regex, self.terminal_input)
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