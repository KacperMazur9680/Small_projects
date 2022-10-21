class Regex_Engine:
    def __init__(self, regex_input):
        regex, terminal_input = regex_input.split("|")
        self.regex = regex
        self.terminal_input = terminal_input
        self.out = bool()

    def compare(self):
        if self.regex == "" or self.regex == ".":
            value = True
        elif self.regex == self.terminal_input:
            value = True
        else: 
            value = False
        self.out = value
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