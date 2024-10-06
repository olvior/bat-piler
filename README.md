# Bat-piler

A little compiler written in python that translates a simple language into the Bat asm for minecraft.

Simple language is documented at `LANGUAGE_README.md`

## Usage

Make sure to have python installed

Download the code and unzip it  

Open the folder with the code in your terminal

Run

```sh
python main.py input_file.hb output.as
```

With the input files and output files names accordingly.

## How does it work

It is quite simple, going through the input file line by line and matching the command with a function

The way it works in assembly is that each variable holds a spot in memory, and whenever you use that variable it loads it into a register and uses that to do math or whatever is needed, then puts it back into memory.
