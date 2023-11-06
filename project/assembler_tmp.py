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
        self.block = None
        self.location = None
        self.object_code = ""

    def __str__(self) -> str:
        return f"({self.format}, {self.symbol}, {self.mnemonic}, {self.operand}, {self.block}, {self.location}, {self.object_code})"


class Symbol:
    def __init__(self, block, location) -> None:
        self.block = block
        self.location = location

    def __str__(self) -> str:
        return f"({self.block}, {self.location})"


class Section:
    def __init__(self) -> None:
        self.instructions = []
        self.__extdef_table = {}
        self.__extref_table = {}
        self.__modified_record = {}
        self.__blocks_length = {}
        self.__literal_table = []
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
        # print each block's length
        print("Length{")
        for b in self.__blocks_length:
            print("\t", b, self.__blocks_length[b])
        print("}\n")
        # print instruction
        print("Instructions:")
        for insruction in self.instructions:
            print("\t", insruction)
        return ""

    def _pass1(self) -> None:
        cur_block = ""
        default_block = ""
        for instrction in self.instructions:
            if instrction.mnemonic == "START" or instrction.mnemonic == "CSECT":
                cur_block = instrction.symbol
                if instrction.symbol != "":
                    default_block = cur_block
                instrction.block = cur_block
                instrction.location = (
                    0 if instrction.operand != "" else int(instrction.operand)
                )
                self.__symbol_table[cur_block] = Symbol(cur_block, instrction.location)
                self.__blocks_length[cur_block] = instrction.location
            elif instrction.mnemonic == "USE":
                cur_block = instrction.symbol
                if cur_block == "":
                    cur_block = default_block
                if cur_block not in self.__blocks_length:
                    self.__blocks_length[cur_block] = 0
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
            elif instrction.mnemonic == "EXTDEF":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                for symbol in instrction.operand.split(","):
                    self.__extdef_table[symbol] = None
            elif instrction.mnemonic == "EXTREF":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                for symbol in instrction.operand.split(","):
                    self.__extref_table[symbol] = None
            elif instrction.mnemonic == "LTORG" or instrction.mnemonic == "END":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                for literal in self.__literal_table:
                    if literal[0] == "C":
                        self.__blocks_length[cur_block] += len(literal) - 3
                    elif literal[0] == "X":
                        self.__blocks_length[cur_block] += (len(literal) - 3) // 2
                    self.__symbol_table[literal] = Symbol(
                        cur_block, instrction.location
                    )
                self.__literal_table = []
            elif instrction.mnemonic == "RESW":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                self.__blocks_length[cur_block] += 3 * int(instrction.operand)
                self.__symbol_table[instrction.symbol] = Symbol(
                    cur_block, instrction.location
                )
            elif instrction.mnemonic == "RESB":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                self.__blocks_length[cur_block] += int(instrction.operand)
                self.__symbol_table[instrction.symbol] = Symbol(
                    cur_block, instrction.location
                )
            elif instrction.mnemonic == "BYTE":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                if instrction.operand[0] == "C":
                    self.__blocks_length[cur_block] += len(instrction.operand) - 3
                elif instrction.operand[0] == "X":
                    self.__blocks_length[cur_block] += (
                        len(instrction.operand) - 3
                    ) // 2
                self.__symbol_table[instrction.symbol] = Symbol(
                    cur_block, instrction.location
                )
            elif instrction.mnemonic == "WORD":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                self.__blocks_length[cur_block] += 3
            elif instrction.mnemonic == "EQU":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
            elif instrction.mnemonic == "BASE":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
            elif instrction.mnemonic == "ORG":
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                if instrction.operand.isdigit():
                    self.__blocks_length[cur_block] = int(instrction.operand)
                else:
                    for symbol in self.__symbol_table:
                        if symbol == instrction.operand:
                            instrction.operand = instrction.operand.replace(
                                symbol, str(self.__symbol_table[symbol].location)
                            )
                        else:
                            raise "Can't support ORG forward reference"
                    self.__blocks_length[cur_block] = eval(instrction.operand)
            elif instrction.mnemonic in opcode_table:
                instrction.block = cur_block
                instrction.location = self.__blocks_length[cur_block]
                self.__blocks_length[cur_block] += instrction.format

            if instrction.operand != "" and instrction.operand[0] == "=":
                self.__literal_table.append(instrction.operand)

            if instrction.symbol != "":
                self.__symbol_table[instrction.symbol] = Symbol(
                    cur_block, self.__blocks_length[cur_block]
                )

        pre_block_size = ""
        for block in self.__blocks_length:
            if block == default_block:
                pre_block_size = self.__blocks_length[block]
                self.__blocks_length[block] = 0
            else:
                tmp = self.__blocks_length[block]
                self.__blocks_length[block] = pre_block_size
                pre_block_size = tmp

    def _pass2(self) -> None:
        for instruction in self.instructions:
            if instruction.mnemonic == "WORD":
                if instruction.operand.isdigit():
                    instruction.object_code = int(instruction.operand)
                elif instruction.operand != "" and instruction.operand[0] == "*":
                    self.__symbol_table[instruction.symbol] = Symbol(
                        instruction.block, instruction.location
                    )
                else:
                    for symbol in self.__symbol_table:
                        if symbol == instruction.operand:
                            instruction.operand = instruction.operand.replace(
                                symbol, str(self.__symbol_table[symbol].location)
                            )

                    self.__symbol_table[instruction.symbol] = Symbol(
                        instruction.block, eval(instruction.operand)
                    )
            elif instruction.mnemonic == "EQU":
                if instruction.operand.isdigit():
                    instruction.object_code = int(instruction.operand)
                elif instruction.operand != "" and instruction.operand[0] == "*":
                    self.__symbol_table[instruction.symbol] = Symbol(
                        instruction.block, instruction.location
                    )
                else:
                    for symbol in self.__symbol_table:
                        if symbol == instruction.operand:
                            instruction.operand = instruction.operand.replace(
                                symbol, str(self.__symbol_table[symbol].location)
                            )
                    self.__symbol_table[instruction.symbol] = Symbol(
                        instruction.block, eval(instruction.operand)
                    )
            elif instruction.mnemonic == "BASE":
                if instruction.operand.isdigit():
                    instruction.object_code = int(instruction.operand)
                elif instruction.operand != "" and instruction.operand[0] == "*":
                    instruction.operand = int(instruction.location)
                else:
                    for symbol in self.__symbol_table:
                        if symbol == instruction.operand:
                            instruction.operand = instruction.operand.replace(
                                symbol, str(self.__symbol_table[symbol].location)
                            )
                    instruction.operand = eval(instruction.operand)

    def _pass3(self) -> None:
        for instruction in self.instructions:
            if instruction.mnemonic in opcode_table:
                if instruction.format == 1:
                    instruction.object_code = opcode_table[instruction.mnemonic]["obj"]
                elif instruction.format == 2:
                    register1 = self.register_table[instruction.operand.split(",")[0]]
                    register2 = self.register_table[instruction.operand.split(",")[1]]
                    instruction.object_code = f'{opcode_table[instruction.mnemonic]["obj"]}{register1}{register2}'
                elif instruction.format == 3:
                    n, i, x, b, p, e = 0, 0, 0, 0, 0, 0
                    opcode = opcode_table[instruction.mnemonic]["obj"]
                    if opcode_table[instruction.mnemonic]["isSIC"] == True:
                        n, i = 0, 0

    def assemble(self) -> None:
        self._pass1()
        self._pass2()
        self._pass3()

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

                instruction = Instruction()

                if len(line) == 0 or "." in line[0]:
                    continue

                if "+" in line[0]:
                    instruction.format = 4
                    line[0] = line[0].replace("+", "")
                elif "+" in line[1]:
                    instruction.format = 4
                    line[1] = line[1].replace("+", "")

                if line[0] in opcode_table or line[0] in directive_table:
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
