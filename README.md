# Helix
__Attention!__
This document is pre-draft and will be unstable until compiler becomes MVP status. 

## Syntax

### Functions

Minimal function declaration:
```
def func1() {}
```

Function with arguments and return type:
```
def func2(a: Int, b: Int): Bool {
    return false;
}
```
If return type is not specified - its considered as void

### Variables
Two variable of type `Int`.
First - immutable(initializes once, cannot be reassigned).
Second - mutable.
```
let a: Int = 1;
var b: Int = 2;

a = 3; // Error: variable `a` is immutable
b = 4; // Ok
```

## Data types

Signed integers:

| Bits | Signed  | Range                   |
|------|---------|-------------------------|
| 8    | `Byte`  | -128..127               |
| 16   | `Short` | -32768..32767           |
| 32   | `Int`   | -2147483648..2147483647 |
| 64   | `Long`  | -9223372036854775808..  |
|      |         | +9223372036854775807    |

Unsigned integers:

| Bits | Type    | Range                   | 
|------|---------|-------------------------|
| 8    | `UByte` | 0..255                  |
| 16   | `UShort`| 0..65535                |
| 32   | `UInt`  | 0..4294967295           |
| 64   | `ULong` | 0..18446744073709551615 |

Floating point:

| Bits | Type     | Min/Max             | 
|------|----------|---------------------|
| 32   | `Float`  | 1.2e-38 / 3.4e+38   |
| 64   | `Double` | 2.3e-308 / 1.7e+308 |
