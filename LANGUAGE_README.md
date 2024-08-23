# Language Documentation

In general:
+ indentation is irrelevant
+ ...

## Variables

In the language you work with variables

They are assigned like this:
```hb
var my_variable_name = 24
```

The only type is an integer

You can then change the value of a variable like so:
```hb
var player_y = 0
var player_velocity_y = 6

set player_velocity_y = 20
set player_y = player_y + player_velocity_y
```

You can either assign a variable to a literal, a variable, or to an expression (more details about those below).

The included ones are:
1. +, addition
2. -, subtraction
3. AND/&&, bitwise and
4. XOR/^ bitwise xor
5. NOR, bitwise nor

## Expressions

Expressions can now be of an arbitrary length, however they are always evaluated from right to left.

```hb
var player_y = other_variable + velocity + 4 - friction
```

Is perfectly valid, but the use of parentheses will just break the compiler and not change the order of operations.

## Conditionals

You can declare an if statement like so:
```hb
if is_touching_groud == 1
    set player_y = ground_y
endif
```

The `if` and `endif` are what matters.

## Loops

Proper loops such as for and while are not yet supported, but you can make a loop like so:
```hb
// define an address
.loop_start
    set counter = counter + 1
    ... do stuff
    
    if counter < 10
        goto .loop_start
    endif
```

## Functions

You can call functions just like in the asm language:
```hb
call .my_func

halt


.my_func
    return
```

## IO

Store to a port like so (default value is 0):

```hb
output SCREEN_SET_PIXEL_X 240
output SCREEN_SET_PIXEL_Y 240
output SCREEN_DRAW_PIXEL
output SCREEN_PUSH
```

Load like so:

```hb
input LOAD_RNG my_random_variable
```

These are the port names:
```py
SCREEN_SET_PIXEL_X = 240
SCREEN_SET_PIXEL_Y = 241
SCREEN_DRAW_PIXEL = 242
SCREEN_CLEAR_PIXEL = 243
SCREEN_LOAD_PIXEL = 244
SCREEN_PUSH = 245
SCREEN_CLEAR = 246

CHAR_WRITE = 247
CHAR_PUSH = 248
CHAR_CLEAR = 249

NUMBER_SHOW = 250
NUMBER_CLEAR = 251
NUMBER_SET_SIGNED = 252
NUMBER_SET_UNSIGNED = 253

LOAD_RNG = 254
LOAD_CONTROLLER = 255
```
