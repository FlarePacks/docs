# Scores

A `score` represents a Minecraft scoreboard objective. Flare handles allocating and managing temporary scoreboards automatically.

## Basic Usage

::: code-group

```python [Flare]
from flare import score

x = score(100)
y = score(50)
z = x + y  # Generates: scoreboard players operation ...
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 100
scoreboard players set pack_y __pack__vars__ 50
scoreboard players operation pack_z __pack__vars__ = pack_x __pack__vars__
scoreboard players operation pack_z __pack__vars__ += pack_y __pack__vars__
```

:::

All standard Python arithmetic operators are supported:

| Operator                   | Minecraft equivalent                           |
|----------------------------|------------------------------------------------|
| `+`, `-`, `*`, `//`        | `scoreboard players operation ... +=/-=/*=//=` |
| `+=`, `-=`, `*=`, `//=`    | In-place scoreboard operations                 |
| `<`, `<=`, `>`, `>=`, `==` | `execute if score ... matches`                 |

## Fixed Precision (`fixed`)

Minecraft scoreboards can only store integers. To work with decimal numbers, Flare scales values automatically. Use the `fixed` class to specify decimal precision:

::: code-group

```python [Flare]
from flare import fixed

# fixed[5] means 5 decimal places of precision (multiplier of 1e-5)
# So 1.5 in Python is stored as 150000 on the scoreboard.
a = fixed[5](1.5)
b = fixed[5](2.0)
c = a * b  # Flare handles all scaling math for you!
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_100000 __pack__constant__ 100000
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_a __pack__vars__ 150000
scoreboard players set pack_b __pack__vars__ 200000
scoreboard players operation pack_c __pack__vars__ = pack_a __pack__vars__
scoreboard players operation pack_c __pack__vars__ *= pack_b __pack__vars__
scoreboard players operation pack_c __pack__vars__ /= #_100000 __pack__constant__
```

:::

## Big Integers (`bigscore`)

If you need numbers larger than the 32-bit Minecraft limit (`2,147,483,647`), use `bigscore`. It transparently chains multiple scoreboard objectives together:

::: code-group

```python [Flare]
from flare import bigscore

# 64-bit integer using two 32-bit limbs
x = bigscore(10_000_000_000, size=2)
x *= 5
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_10000 __pack__constant__ 10000
```

```mcfunction [__init__.mcfunction]
scoreboard players set _0 __pack__vars__ 0
scoreboard players set _1 __pack__vars__ 0
scoreboard players set #big0_0 __pack__temp__ 5
scoreboard players set #big0_1 __pack__temp__ 0
scoreboard players set #C_0 __pack__temp__ 0
scoreboard players set #C_1 __pack__temp__ 0
scoreboard players set #C_2 __pack__temp__ 0
scoreboard players set #C_3 __pack__temp__ 0
scoreboard players operation #mul __pack__temp__ = _0 __pack__vars__
scoreboard players operation #mul __pack__temp__ *= #big0_0 __pack__temp__
scoreboard players operation #C_0 __pack__temp__ += #mul __pack__temp__
scoreboard players operation #mul __pack__temp__ = _0 __pack__vars__
scoreboard players operation #mul __pack__temp__ *= #big0_1 __pack__temp__
scoreboard players operation #C_1 __pack__temp__ += #mul __pack__temp__
scoreboard players operation #mul __pack__temp__ = _1 __pack__vars__
scoreboard players operation #mul __pack__temp__ *= #big0_0 __pack__temp__
scoreboard players operation #C_1 __pack__temp__ += #mul __pack__temp__
scoreboard players operation #mul __pack__temp__ = _1 __pack__vars__
scoreboard players operation #mul __pack__temp__ *= #big0_1 __pack__temp__
scoreboard players operation #C_2 __pack__temp__ += #mul __pack__temp__
scoreboard players set #carry __pack__temp__ 0
scoreboard players operation #C_0 __pack__temp__ += #carry __pack__temp__
scoreboard players operation #carry __pack__temp__ = #C_0 __pack__temp__
scoreboard players operation #carry __pack__temp__ /= #_10000 __pack__constant__
scoreboard players operation #C_0 __pack__temp__ %= #_10000 __pack__constant__
scoreboard players operation #C_1 __pack__temp__ += #carry __pack__temp__
scoreboard players operation #carry __pack__temp__ = #C_1 __pack__temp__
scoreboard players operation #carry __pack__temp__ /= #_10000 __pack__constant__
scoreboard players operation #C_1 __pack__temp__ %= #_10000 __pack__constant__
scoreboard players operation #C_2 __pack__temp__ += #carry __pack__temp__
scoreboard players operation #carry __pack__temp__ = #C_2 __pack__temp__
scoreboard players operation #carry __pack__temp__ /= #_10000 __pack__constant__
scoreboard players operation #C_2 __pack__temp__ %= #_10000 __pack__constant__
scoreboard players operation #C_3 __pack__temp__ += #carry __pack__temp__
scoreboard players operation #carry __pack__temp__ = #C_3 __pack__temp__
scoreboard players operation #carry __pack__temp__ /= #_10000 __pack__constant__
scoreboard players operation #C_3 __pack__temp__ %= #_10000 __pack__constant__
scoreboard players operation _0 __pack__vars__ = #C_0 __pack__temp__
scoreboard players operation _1 __pack__vars__ = #C_1 __pack__temp__
```

:::

## Avoiding Copies with `ref`

By default, assigning one Flare variable to another (`y = x`) emits a Minecraft command to physically copy the value:

::: code-group

```python [Flare]
from flare import score, ref

x = score(10)

z = x       # COPIES the value. Emits a command to map 'z' and copy 'x'.
y = ref(x)  # NO COPY. 'y' is a Python reference to the same address as 'x'.

x += 5      # Modifies 'x' (now 15). 'y' is also 15 (same address). 'z' stays 10.
y += 5      # Modifies 'x' again (now 20).

print(x, y, z)  # Output: 20 20 10
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 10
scoreboard players operation pack_z __pack__vars__ = pack_x __pack__vars__
scoreboard players add pack_x __pack__vars__ 5
scoreboard players add pack_x __pack__vars__ 5
tellraw @a [{"score": {"name": "pack_x", "objective": "__pack__vars__"}}, {"text": " "}, {"score": {"name": "pack_x", "objective": "__pack__vars__"}}, {"text": " "}, {"score": {"name": "pack_z", "objective": "__pack__vars__"}}]
```

:::

Use `ref()` whenever you want to pass a variable around in Python *without* emitting a copy command.

`ref()` can also be used to store mathematical operations lazily! If you wrap a math operation in `ref()`, Flare will remember the operation instead of immediately generating commands for it. The commands will only be generated when the reference is actually used or assigned:

```python
# No commands are generated here!
double_x = ref(x * 2)

# Now Flare generates the operations to calculate x * 2 and print it
print(double_x)
```
## Reassigning Variables (`__iset__`)

Thanks to Flare's AST preprocessor, assigning to an already-existing variable automatically updates its value in-place without creating a new variable:

::: code-group

```python [Flare]
x = score(10)
y = score(20)

# Since y already exists, Flare detects this and safely updates
# y's existing scoreboard address to match x (using __iset__).
y = x
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 10
scoreboard players set pack_y __pack__vars__ 20
scoreboard players operation pack_y __pack__vars__ = pack_x __pack__vars__
```

:::

You do **not** need to use slice notation or manually manage addresses when updating a variable.

## Manual Objective Management (`Objective`)

If you want to explicitly declare a scoreboard objective in your code (perhaps with a specific display name or type other than `dummy`), you can use the `Objective` class:

::: code-group

```python [Flare]
from flare import Objective, selector

# Emits: scoreboard objectives add my_obj dummy {"text": "My Obj"}
# Automatically prevents the compiler from emitting an internal 'dummy' objective of the same name.
my_obj = Objective("my_obj", type="dummy", display='{"text": "My Obj"}')

# You can access scores on this objective using standard Python indexing:
my_score = my_obj[@s]
named_score = my_obj["my_fake_player"]

my_score += 10
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add my_obj dummy {"text": "My Obj"}
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players operation pack_my_score __pack__vars__ = @s my_obj
scoreboard players operation pack_named_score __pack__vars__ = my_fake_player my_obj
scoreboard players add pack_my_score __pack__vars__ 10
```

:::

*Note: Flare automatically hoists `Objective` declarations into the global `#minecraft:load` tag, so they only run once at startup, even if you define them inside a tick function!*

### Assuming Existing Objectives (`add=False`)

If you want to manipulate an objective that already exists in the world (e.g. from a different datapack or built-in game mechanic), you can pass `add=False`. This registers the objective in Flare's internal compiler to prevent it from emitting creation commands, but doesn't emit any `scoreboard objectives add` command itself:

```python
kills = Objective("player_kills", type="playerKillCount", add=False)
```

### Direct Score Access

If you prefer, you can also bypass `Objective` entirely and access a score by explicitly defining the `addr` property:

::: code-group

```python [Flare]
my_score = score(addr="@s my_obj")
my_score += 10

# Dynamic targets via f-strings
target = "@p"
dynamic_score = score(addr=f"{target} my_obj")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add my_obj dummy
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players operation pack_my_score __pack__vars__ = @s my_obj
scoreboard players add pack_my_score __pack__vars__ 10
scoreboard players operation pack_dynamic_score __pack__vars__ = @p my_obj
```

:::

## Type Promotion & Casting

Flare features a dynamic type lattice that automatically promotes operands in mixed-type arithmetic:

- `score` (rank 10) + `fixed` (rank 20) $\rightarrow$ automatically promotes to `fixed`!
- Lower-ranked values are scaled or widened to the least upper bound (LUB) without manual conversion.

::: code-group

```python [Flare]
from flare import score, fixed, nbtint

s = score(5)
f = fixed(1.5)

# Automatic promotion: s is scaled to fixed precision before addition
result = s + f

# Explicit casting
s_as_fixed = s.cast(fixed)
s_as_nbt = s.cast(nbtint)
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_10000 __pack__constant__ 10000
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_s __pack__vars__ 5
scoreboard players set pack_f __pack__vars__ 15000
scoreboard players operation pack_result __pack__vars__ = pack_f __pack__vars__
scoreboard players operation #add0 __pack__temp__ = pack_s __pack__vars__
scoreboard players operation #add0 __pack__temp__ *= #_10000 __pack__constant__
scoreboard players operation pack_result __pack__vars__ += #add0 __pack__temp__
scoreboard players operation #0 __pack__temp__ = pack_s __pack__vars__
scoreboard players operation #0 __pack__temp__ *= #_10000 __pack__constant__
scoreboard players operation pack_s_as_fixed __pack__vars__ = #0 __pack__temp__
execute store result storage flare:temp t1 int 1 run scoreboard players get pack_s __pack__vars__
data modify storage pack:vars pack_s_as_nbt set from storage flare:temp t1
```

:::

## String to Score Parsing (`parse_int`)

Flare can dynamically parse strings into integer scoreboards at runtime using `parse_int`:

::: code-group

```python [Flare]
from flare import nbtstr, parse_int, score

user_str = nbtstr("-1234")
num = parse_int(user_str)
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_10 __pack__constant__ 10
scoreboard players set #_n1 __pack__constant__ -1
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_user_str set value "-1234"
data modify storage flare:temp parse_curr_1 set from storage pack:vars pack_user_str
execute store result score #parse_len_1 __pack__temp__ run data get storage flare:temp parse_curr_1
scoreboard players set #parse_neg_1 __pack__temp__ 0
scoreboard players set pack_num __pack__vars__ 0
execute if score #parse_len_1 __pack__temp__ matches 1.. run function pack:___init__/parse_int_loop_0
execute if score #parse_neg_1 __pack__temp__ matches 1 run scoreboard players operation pack_num __pack__vars__ *= #_n1 __pack__constant__
```

```mcfunction [___init__/parse_int_loop_0.mcfunction]
data modify storage flare:temp parse_char_1 set string storage flare:temp parse_curr_1 0 1
data modify storage flare:temp parse_curr_1 set string storage flare:temp parse_curr_1 1
scoreboard players remove #parse_len_1 __pack__temp__ 1
execute if data storage flare:temp {"parse_char_1": "-"} run scoreboard players set #parse_neg_1 __pack__temp__ 1
scoreboard players set #parse_dig_1 __pack__temp__ -1
execute if data storage flare:temp {"parse_char_1": "0"} run scoreboard players set #parse_dig_1 __pack__temp__ 0
execute if data storage flare:temp {"parse_char_1": "1"} run scoreboard players set #parse_dig_1 __pack__temp__ 1
execute if data storage flare:temp {"parse_char_1": "2"} run scoreboard players set #parse_dig_1 __pack__temp__ 2
execute if data storage flare:temp {"parse_char_1": "3"} run scoreboard players set #parse_dig_1 __pack__temp__ 3
execute if data storage flare:temp {"parse_char_1": "4"} run scoreboard players set #parse_dig_1 __pack__temp__ 4
execute if data storage flare:temp {"parse_char_1": "5"} run scoreboard players set #parse_dig_1 __pack__temp__ 5
execute if data storage flare:temp {"parse_char_1": "6"} run scoreboard players set #parse_dig_1 __pack__temp__ 6
execute if data storage flare:temp {"parse_char_1": "7"} run scoreboard players set #parse_dig_1 __pack__temp__ 7
execute if data storage flare:temp {"parse_char_1": "8"} run scoreboard players set #parse_dig_1 __pack__temp__ 8
execute if data storage flare:temp {"parse_char_1": "9"} run scoreboard players set #parse_dig_1 __pack__temp__ 9
execute if score #parse_dig_1 __pack__temp__ matches 0.. run scoreboard players operation pack_num __pack__vars__ *= #_10 __pack__constant__
execute if score #parse_dig_1 __pack__temp__ matches 0.. run scoreboard players operation pack_num __pack__vars__ += #parse_dig_1 __pack__temp__
execute if score #parse_len_1 __pack__temp__ matches 1.. run function pack:___init__/parse_int_loop_0
```

:::

