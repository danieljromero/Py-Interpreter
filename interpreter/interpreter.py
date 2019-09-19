from interpreter.stacks import Environment, Item, Func


def extract(file_name: str) -> None:
    """Gets instructions from a .txt file.

    Opens and reads a text file to extract the instructions within.

    Args:
        :param file_name: .txt file
    Raises:
        :raise: FileNotFoundError: Incorrect file type used.
        :raise: TypeError: Empty file type used.
    """
    if not file_name.endswith('.txt'):
        raise TypeError('extract() only opens .txt files.')
    else:
        file = open(file_name, 'r')
        instructions = [line.rstrip() for line in file]
        file.close()
        if not instructions:
            raise TypeError('extract() only opens non-empty .txt file.')
        return instructions


def print_results(results: list, output: str):
    """Writes results of execution to an output file."""
    with open(output, 'w') as file:
        for item in results[::-1]:
            if type(item) == bool:
                if item == True:
                    file.write("%s\n" % ":true:")
                elif item == False:
                    file.write("%s\n" % ":false:")
            elif type(item) == int:
                file.write("%s\n" % str(item))
            elif type(item) == Item:
                file.write("%s\n" % item.name)
            elif type(item) == Func:
                file.write("%s\n" % item.fname)
            elif item == ":error:":
                file.write("%s\n" % item)
            elif item == ":unit:":
                file.write("%s\n" % item)
            elif type(item) == str:
                file.write("%s\n" % item.strip("\""))
    file.close()


def interpreter(input: str, output: str):
    """Evaluates expressions from an input file and writes results to an output file."""
    instructions = extract(input)
    env = Environment()
    env.stream(instructions)
    main_stack = env.stacks.pop()
    print_results(main_stack.items, output)
