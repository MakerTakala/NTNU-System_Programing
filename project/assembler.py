import json

opcode_table = json.load(open("table/opcode.json", "r"))
directive_table = json.load(open("table/directive.json", "r"))
register_table = json.load(open("table/register.json", "r"))


class Instruction:
    def __init__(self) -> None:
        # 0:directive, 1:format1, 2:format2, 3:format3 4:format4
        self.format = None
        self.symbol = ""
        self.mnemonic = ""
        self.operand = ""
        self.location = None
        self.object_code = ""

    def __init__(self, format: int, symbol: str, mnemonic: str, operand: str) -> None:
        self.format = format
        self.symbol = symbol
        self.mnemonic = mnemonic
        self.operand = operand
        self.location = None
        self.object_code = ""

    def __str__(self) -> str:
        return f"({self.format}, {self.symbol}, {self.mnemonic}, {self.operand}, {self.location}, {self.object_code})"


class Section:
    def __init__(self) -> None:
        self.instructions = []
        self.__extdef_table = {}
        self.__extref_table = {}
        self.__modified_record = {}
        self.__symbol_table = {}

    def __str__(self) -> str:
        print("Symbol{")
        for symbol in self.__symbol_table:
            print("\t", symbol, self.__symbol_table[symbol])
        print("}\n")
        # print each extdef
        print("Extdef{")
        for d in self.__extdef_table:
            print("\t", d, self.__extdef_table[d])
        print("}\n")
        # print each extref
        print("Extref{")
        for r in self.__extref_table:
            print("\t", r, self.__extref_table[r])
        print("}\n")
        # print each modified record
        print("Modified{")
        for m in self.__modified_record:
            print("\t", m, self.__modified_record[m])
        print("}\n")
        # print instruction
        print("Instructions:")
        for insruction in self.instructions:
            print("\t", insruction)
        return ""

    def _calcualte(self, operand: str, cur_location: int = 0) -> str:
        if operand == "*":
            operand = str(cur_location)
            return operand
        for symbol in self.__symbol_table:
            if symbol in operand and self.__symbol_table[symbol] != None:
                operand = operand.replace(symbol, str(self.__symbol_table[symbol]))
        for symbol in self.__extdef_table:
            if symbol in operand and self.__extdef_table[symbol] != None:
                operand = operand.replace(symbol, str(self.__extdef_table[symbol]))
        try:
            result = eval(operand)
            return result
        except:
            return None

    def sorting(self) -> None:
        defalut_block = ""
        blocks = {}
        cur_block = None
        for instruction in self.instructions:
            if instruction.mnemonic == "START":
                defalut_block = instruction.symbol
                blocks[instruction.symbol] = []
                cur_block = instruction.symbol
            if instruction.mnemonic == "CSECT":
                blocks[instruction.symbol] = []
                cur_block = instruction.symbol
            elif instruction.mnemonic == "USE":
                if instruction.oprand == "":
                    cur_block = defalut_block
                elif instruction.operand in blocks:
                    cur_block = instruction.operand
                else:
                    blocks[instruction.operand] = []
                    cur_block = instruction.operand
                continue
            blocks[cur_block].append(instruction)

        self.instructions = []
        for block in blocks:
            for instruction in blocks[block]:
                self.instructions.append(instruction)

    def slove_literal(self) -> None:
        literal_table = []
        literal_count = 1

        for index, instruction in enumerate(self.instructions):
            if instruction.operand != "":
                if instruction.mnemonic == "*" and instruction.operand[0] == "=":
                    instruction.symbol = "literal" + str(literal_count)
                    instruction.mnemonic = "BYTE"
                    literal_count += 1
                    instruction.operand = instruction.operand[1:]
                elif instruction.operand[0] == "=":
                    literal_table.append(
                        {
                            "name": "literal" + str(literal_count),
                            "data": instruction.operand[1:],
                        }
                    )
                    instruction.operand = "literal" + str(literal_count)
                    literal_count += 1
            if instruction.mnemonic == "LTORG" or instruction.mnemonic == "END":
                for literal in literal_table:
                    literal_instrcution = Instruction(
                        0, literal["name"], "BYTE", literal["data"]
                    )

                    self.instructions.insert(index, literal_instrcution)
                literal_table = []

    def set_symbol(self) -> None:
        for instruction in self.instructions:
            if instruction.symbol != "":
                print(instruction.symbol)
                self.__symbol_table[instruction.symbol] = None
            if instruction.mnemonic == "EXTDEF":
                for symbol in instruction.operand.split(","):
                    self.__extdef_table[symbol] = 0
            if instruction.mnemonic == "EXTREF":
                for symbol in instruction.operand.split(","):
                    self.__extref_table[symbol] = None

        while True:
            finished = True
            for symbol in self.__symbol_table:
                if self.__symbol_table[symbol] == None:
                    finished = False
                    break
            if finished:
                break

            cur_location = 0

            for instruction in self.instructions:
                if instruction.symbol != "":
                    self.__symbol_table[instruction.symbol] = cur_location
                    if instruction.symbol in self.__extdef_table:
                        self.__extdef_table[instruction.symbol] = cur_location

                if instruction.mnemonic == "START" or instruction.mnemonic == "CSECT":
                    cur_location = int(instruction.operand)
                    self.__symbol_table[instruction.symbol] = int(instruction.operand)
                elif instruction.mnemonic == "CSECT":
                    cur_location = 0
                    self.__symbol_table[instruction.symbol] = 0
                elif instruction.mnemonic == "RESW":
                    self.__symbol_table[instruction.symbol] = cur_location
                    cur_location += 3 * int(instruction.operand)
                elif instruction.mnemonic == "RESB":
                    self.__symbol_table[instruction.symbol] = cur_location
                    cur_location += int(instruction.operand)
                elif instruction.mnemonic == "BYTE":
                    self.__symbol_table[instruction.symbol] = cur_location
                    if instruction.operand[0] == "C":
                        cur_location += len(instruction.operand) - 3
                    elif instruction.operand[0] == "X":
                        cur_location += (len(instruction.operand) - 3) // 2
                elif instruction.mnemonic == "WORD":
                    result = self._calcualte(instruction.operand, cur_location)
                    if result != None:
                        self.__symbol_table[instruction.symbol] = result
                    cur_location += 3
                elif instruction.mnemonic == "EQU":
                    result = self._calcualte(instruction.operand, cur_location)
                    if result != None:
                        self.__symbol_table[instruction.symbol] = result
                elif instruction.mnemonic == "ORG":
                    result = self._calcualte(instruction.operand, cur_location)
                    if result != None:
                        instruction.operand = result
                        cur_location = int(result)
                    else:
                        raise Exception("ORG can't support forward reference")
                elif instruction.mnemonic == "BASE":
                    result = self._calcualte(instruction.operand, cur_location)
                    if result != None:
                        instruction.operand = result

                else:
                    cur_location += int(instruction.format)

    def set_location(self) -> None:
        cur_location = 0
        for instruction in self.instructions:
            instruction.location = cur_location
            cur_location += int(instruction.format)
            if instruction.mnemonic == "START" or instruction.mnemonic == "CSECT":
                cur_location = int(instruction.operand)
            elif instruction.mnemonic == "RESW":
                cur_location += 3 * int(instruction.operand)
            elif instruction.mnemonic == "RESB":
                cur_location += int(instruction.operand)
            elif instruction.mnemonic == "BYTE":
                if instruction.operand[0] == "C":
                    cur_location += len(instruction.operand) - 3
                elif instruction.operand[0] == "X":
                    cur_location += (len(instruction.operand) - 3) // 2
            elif instruction.mnemonic == "WORD":
                cur_location += 3
            elif instruction.mnemonic == "ORG":
                result = self._calcualte(instruction.operand)
                cur_location = int(result)

    def set_object_code(self) -> None:
        base = 0
        for instruction in self.instructions:
            if instruction.mnemonic == "BYTE":
                if instruction.operand[0] == "C":
                    instruction.object_code = f"{instruction.operand[2:-1]}"
                elif instruction.operand[0] == "X":
                    instruction.object_code = f"{instruction.operand[2:-1]}"
            elif instruction.mnemonic == "WORD":
                instruction.object_code = f"{int(instruction.operand):06X}"
            elif instruction.mnemonic == "BASE":
                base = self._calcualte(instruction.operand)

            elif instruction.mnemonic in opcode_table:
                pass

    def assemble(self) -> None:
        self.sorting()
        self.slove_literal()
        self.set_symbol()
        self.set_location()
        self.set_object_code()

    def write(self, file) -> None:
        pass


class Assembler:
    def __init__(self) -> None:
        self.__instructions = []
        self.__sections = []

    def clear(self) -> None:
        self.__instructions = []
        self.__sections = []

    def preprocessing(self, path: str) -> None:
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip().replace("\t", " ").split(" ")
                line += [""] * (3 - len(line))

                instruction = Instruction(0, "", "", "")

                if len(line) == 0 or "." in line[0]:
                    continue

                if "+" in line[0]:
                    instruction.format = 4
                    line[0] = line[0].replace("+", "")
                elif "+" in line[1]:
                    instruction.format = 4
                    line[1] = line[1].replace("+", "")

                if (
                    line[0] in opcode_table
                    or line[0] in directive_table
                    or line[0] == "*"
                ):
                    line[2] = line[1]
                    line[1] = line[0]
                    line[0] = ""

                instruction.symbol = line[0]
                instruction.mnemonic = line[1]
                instruction.operand = line[2]

                if instruction.format != 4 and instruction.mnemonic in opcode_table:
                    instruction.format = opcode_table[instruction.mnemonic]["format"]
                elif instruction.format != 4:
                    instruction.format = 0

                self.__instructions.append(instruction)

        self.__sections.append(Section())
        for instruction in self.__instructions:
            if instruction.mnemonic == "CSECT":
                self.__sections.append(Section())
            self.__sections[-1].instructions.append(instruction)

    def assemble(self) -> None:
        for section in self.__sections:
            section.assemble()
            print(section)

    def write_file(self, path: str) -> None:
        with open(path, "w") as f:
            for section in self.__sections:
                section.write(f)

    def parser(self, input_path: str, output_path: str) -> None:
        self.clear()
        self.preprocessing(input_path)
        self.assemble()
        self.write_file(output_path)
