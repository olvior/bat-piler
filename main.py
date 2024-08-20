import parsing_helper
import memory_help as mh
import file_io as fio
import sys

class Variable():
    def __init__(self, name: str):
        self.name = name
        self.memory_addr = mh.allocate_memory()
        mh.variables_dict[self.name] = self
        

    def set_value_literal(self, value):
        self.value = value
        
        self.register = mh.allocate_register()
        mh.set_reg_imm(self.register, self.value)
        mh.move_reg_to_addr(self.register, self.memory_addr)
        mh.free_register(self.register)
        self.register = 0

    def reference(self):
        self.register = mh.allocate_register()
        mh.move_addr_to_reg(self.memory_addr, self.register)
    
    def undo_reference(self):
        mh.free_register(self.register)
        self.register = 0

    def kill(self):
        mh.free_memory(self.memory_addr)
        mh.variables_dict.pop(self.name)

def free_variable(args):
    var = mh.variables_dict[args[1]]
    var.kill()

def deal_with_set(args):
    variable_str = args[1]
    variable = mh.variables_dict[variable_str]

    set_var_value(args[2::], variable)

def deal_with_var(args):
    var_name = args[1]
    value_exp = args[2::]
    
    Variable(var_name)
    var = mh.variables_dict[var_name]

    set_var_value(value_exp, var)

def set_var_value(value_exp, var):
    if len(value_exp) == 1 and parsing_helper.is_literal(value_exp[0]):
        var.set_value_literal(int(value_exp[0]))
        return

    elif len(value_exp) == 1:
        other_var = mh.variables_dict[value_exp[0]]
        other_var.reference()
        mh.move_reg_to_addr(other_var.register, var.memory_addr)
        other_var.undo_reference()
        return
    
    reg = mh.allocate_register()

    evaluate_exp_to_reg(value_exp, reg)
    mh.move_reg_to_addr(reg, var.memory_addr)

    mh.free_register(reg)
    

def deal_with_plus(reg0: int, reg1: int, value_reg: int):
    fio.append_to_out(f"ADD r{reg0} r{reg1} r{value_reg}")

def deal_with_minus(reg0: int, reg1: int, value_reg: int):
    fio.append_to_out(f"SUB r{reg0} r{reg1} r{value_reg}")

def deal_with_nor(reg0: int, reg1: int, value_reg: int):
    fio.append_to_out(f"NOR r{reg0} r{reg1} r{value_reg}")

def deal_with_and(reg0: int, reg1: int, value_reg: int):
    fio.append_to_out(f"AND r{reg0} r{reg1} r{value_reg}")

def deal_with_xor(reg0: int, reg1: int, value_reg: int):
    fio.append_to_out(f"XOR r{reg0} r{reg1} r{value_reg}")

def deal_with_if(args, line_number):
    if_name = f".if_line_{line_number}"
    if_stack.append(if_name)

    parts = args[1::]
    
    regs = [mh.allocate_register(), mh.allocate_register()]
   
    move_unknown_to_reg(parts[0], regs[0])
    move_unknown_to_reg(parts[2], regs[1])
    
    comparison = parts[1]
    
    fio.append_to_out(f"CMP r{regs[0]} r{regs[1]}")
    fio.append_to_out(f"BRH {COMPARISON_DICT[comparison]} {if_name}_skip_jmp")
    fio.append_to_out(f"JMP {if_name}")
    fio.append_to_out(f"{if_name}_skip_jmp")

    for r in regs:
        mh.free_register(r)


MODIFIERS_DICT = {
    '+': deal_with_plus, 
    '-': deal_with_minus,
    'NOR': deal_with_nor,
    'AND': deal_with_and,
    '&&': deal_with_and,
    'XOR': deal_with_xor,
    '^': deal_with_xor,
}


def deal_with_output(args):
    port = args[1]

    if not port in mh.Ports.ports.keys():
        print(f"Port {port} not found") 
        raise ValueError

    reg = mh.allocate_register()
    move_unknown_to_reg(args[2], reg)
    mh.move_reg_to_addr(reg, mh.Ports.ports[port])
    mh.free_register(reg)

def deal_with_input(args):
    port = args[1]

    if not port in mh.Ports.ports.keys():
        print(f"Port {port} not found") 
        raise ValueError

    var: Variable = mh.variables_dict[args[2]]
    
    reg = mh.allocate_register()
    mh.move_addr_to_reg(mh.Ports.ports[port], reg)
    mh.move_reg_to_addr(reg, var.memory_addr)
    mh.free_register(reg)


def move_unknown_to_reg(unknown, reg):
    value_type = parsing_helper.get_exp_type(unknown)
    if value_type == parsing_helper.Exp.LITERAL:
        mh.set_reg_imm(reg, int(unknown))
    else:
        mh.move_addr_to_reg(mh.variables_dict[unknown].memory_addr, reg)
        

def evaluate_exp_to_reg(exp, reg):
    parts = exp
    part_types = []
    for part in parts:
        part_types.append(parsing_helper.get_exp_type(part))
    
    regs = [mh.allocate_register(), mh.allocate_register()]
   
    move_unknown_to_reg(parts[0], regs[0])
    move_unknown_to_reg(parts[2], regs[1])
    
    modifier = parts[1]
    MODIFIERS_DICT[modifier](regs[0], regs[1], reg)

    for r in regs:
        mh.free_register(r)

def negate(args):
    var: Variable = mh.variables_dict[args[1]]
    var.reference()
    fio.append_to_out(f"SUB r0 r{var.register} r{var.register}")
    mh.move_reg_to_addr(var.register, var.memory_addr)
    var.undo_reference()

def append_halt(args):
    global halted

    fio.append_to_out("HLT")
    halted = True

def append_return(args):
    fio.append_to_out("RET")

COMPARISON_DICT = {
    "==": "0",
    "!=": "1",
    ">=": "2",
    "<": "3",
}

KEYWORD_LIST = {
    "set": deal_with_set,
    "var": deal_with_var,
    "free": free_variable,
    "halt": append_halt,
    "HLT": append_halt,
    "return": append_return,
}

INBUILT_FUNCTIONS = {
    "output": deal_with_output,
    "input": deal_with_input,
    "negate": negate
}

if_stack: list[str] = []
halted = False

def main():
    argv = sys.argv

    if len(argv) < 3:
        print("Usage: python3 main.py path/to/file.hb path/to/output.as")
        return


    fio.in_file_path = argv[1]
    fio.out_file_path = argv[2]

    fio.create_out_file()
    fio.append_to_out("// Generated by an assembler I wrote in python")
    
    lines = fio.read_lines_from_in()

    for idx, line in enumerate(lines):
        interpret_line(line, idx)


def interpret_line(line, line_number):
    line = line.strip()
    line_by_spaces = line.split()

    if len(line_by_spaces) == 0:
        return

    if line[0] == "/":
        # we can skip the comment
        return

    start = line_by_spaces[0]
   
    if start in KEYWORD_LIST.keys():
        KEYWORD_LIST[start](line_by_spaces)

    elif start in INBUILT_FUNCTIONS.keys():
        INBUILT_FUNCTIONS[start](line_by_spaces)

    elif start == "if":
        deal_with_if(line_by_spaces, line_number)

    elif start == "endif":
        fio.append_to_out(if_stack.pop())

    elif start[0] == ".":
        fio.append_to_out(line)

    elif start == "goto":
        fio.append_to_out(f"JMP {line_by_spaces[1]}")

    elif start == "call":
        fio.append_to_out(f"CAL {line_by_spaces[1]}")



main()

if not halted:
    fio.append_to_out("HLT")
