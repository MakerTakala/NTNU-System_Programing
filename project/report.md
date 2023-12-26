# System programing Project

## Architecture

I write two file: main.py and Assembler.py

**main.py**: Solve the argument input and output

This is the program entry point, it will be responsbility to slove argument input and output path and file. You also can use -h argument to show the help.

**Assembler.py**: Defind all class in this file

This is define all class in this file, If anyone want to expending this assembler, he could use this file to expending.

**Class**: I also define lot of class with good architecture

-   **class-Assembler**: Slove preproscessing data, split control section and IO control

> A class in assembler.py, it will split the control section to Section class, and control all section processing such as assmebler and write. Besides, it will processing the input file and make the text to Instruciton class and push to section.

-   **class-Section**: Solve all instrucitons and change instructions to obj code

> A class in assembler.py, it will process the instruction to object code, it will do following work flow.

    -   solve_literal: Replace all literal to a symbol
    -   sorting_block: Sorting program block with same block to a group
    -   set_symbol: set all symbol to correct location
    -   set_location: set all instruction location
    -   set_exdef_location: set the exdef location
    -   sorting_index: Sorting the instuction to original position
    -   generate_object_code: Generate object code

> The result object will be save at Instruction class.

-   **class-Modification_record**: Store modification record

-   **class-Instruction**: Store each instruciton

## Learned and Experienced

Great architecture can help you write great code: At the first time, my architecture is messy, I hardly to debug. So I rebuild all project with great architecture and help me easy to debug.

Remember to commit the code: I have write a bad code result in my thought totally confusion. So I decide to rewrite that part. However, I forgot to commit my code record and I can't revert to code version to previous. It tells me git is a good tool to help you.

Deilemma:

-   How to slove forward reference:
    -   I use multi loop until all symbol are reslove, ensure all symbol can be set a location.
-   How to fulfill Arithmetic in programing:
    -   I use an package which can read arithmetic. I replace all symbol which knows location, and use package to calculate.
-   How to control program block and set them to correct place.
    -   In each instuction original location, I store an index in instruction calss and use it to resorting after program block change their position to ensure the instuctions location are correct.

## More than the Required

Basic requirement
Literals  
Symbol-defining Statements  
Program Blocks  
Control Sections

To prove work, we can see example code `./example/code3.asm` and get result with `code_output-1.txt` `code_output-2.txt` `code_output-3.txt`

## Information

Lang: python  
Version: 3.9.6  
Testing Environment: macOS M1

## Usage:

`python3 main.py [-h] [-o O] inputfile`

e.g. `python3 main.py input -o my_output`
output: myoutput-1

#### positional arguments:

inputfile: input file path

#### options:

-h, --help show this help message and exit  
-o O output file path

## Copyright Claim

MIT License

Copyright (c) 2023 Takala

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Any thing you would like to let G.H.Hwang know

I really like latter half semester teaching with actual operation, and see what happen in computer. It really help for operation with our lab server when I make junior project. Thanks for teacher theaching this semester.
