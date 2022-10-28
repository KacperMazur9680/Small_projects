import sys

class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        def consume(r, t):
            print(r, t) #-- shows the elimination process
            if r == "":
                return True
            
            if "?" in r or "*" in r or "+" in r:
                if r[1:2] == "?" and r[0] != "\\" and (r[0] != t[0] or r[0] == "."):
                    r = r.replace(r[0:2], "")
                    return consume(r[1:], t[1:])

                if r[1:2] == "?" and r[0] != "\\" and r[0] == t[0]: 
                    r = r.replace(r[1], "")
                    return consume(r[1:], t[1:])

                if r[1:2] == "*" and r[0] != "\\" and (r[0] == "." or r[0] != t[0]):
                    r = r.replace(r[0:2], "")
                    t = t[-1:]
                    return consume(r, t)

                if (r[1:2] == "*" or r[1:2] == "+") and r[0] != "\\" and r[0] == t[0]:
                    r = r.replace(r[1], "")
                    i = 0
                    for char in t:
                        if char == r[0]:
                            i += 1
                    t = t[i-1:]
                    return consume(r[1:], t[1:])

                if r[1:2] == "+" and r[0] != "\\" and r[0] == "." and len(t) > 1:
                    r = r.replace(r[0:2], "")
                    i = 0
                    for char in t:
                        if char == t[0]:
                            i += 1
                    t = t[i:]

                    return consume(r, t)                    

                if r[0] == "\\":
                    r = r.replace("\\", "")
                
                if r == "?" or r == "+" or r == "*" or r == ".":
                    return True

                if r[0:1] != "." and r[0:1] != t[0:1]:
                    return False

                return consume(r[1:], t[1:])

            if r[0] == "\\":
                r = r.replace("\\", "")
            if r == ".":
                return True
            if r[0:1] != "." and r[0:1] != t[0:1]:
                return False
            return consume(r[1:], t[1:])
            
        def invoke_check(r, t):
            len_r = len(r) - 1
            if r == "\\\\":
                return True
                
            if r.startswith("^") and r.endswith("$"):
                if len(t) != len(r[1:-1]) and "+" not in r and "*" not in r:
                    return False
                if r[-2] != t[-1]:
                    return False
                return consume(r[1:-1], t)

            if r.startswith("^"):
                return consume(r[1:], t[:len_r])

            if r.endswith("$"):
                return consume(r[:-1], t[-len_r:])

            if r in t or r == ".":
                return True
            return consume(r, t)

        self.out = invoke_check(self.regex, self.terminal_input)
        return self.out

    def output(self):
        print(self.out)


def main():
    sys.setrecursionlimit(10000)
    regex_input = input()

    engine = Regex_Engine(regex_input)
    engine.compare()
    engine.output()
    
    
if __name__ == "__main__":
    main()