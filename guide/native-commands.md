# Native Minecraft Commands

Flare includes a smart preprocessor that lets you write literal Minecraft commands **directly** inside your Python script without wrapping them in strings or needing special calls.

```python
from flare import namespace, score

namespace("my_pack")

# Write raw commands natively! Flare translates them automatically.
say Hello World!
/tp @a ~ ~ ~
execute as @a run particle flame ~ ~ ~

# Standard Python logic works alongside commands!
health = score(20)
if health < 10:
    title @a title "Low Health!"
```

## Variable Interpolation

You can effortlessly interpolate Python variables and expressions directly into commands using `$var` and `${expr}` syntax. Flare automatically resolves local variables and their in-game addresses:

::: code-group

```python [Flare]
i = 10
tp @a ~$i ~ ~   # Compiles to: tp @a ~10 ~ ~

x = score(5)
scoreboard players set @s my_score $x   # Injects the scoreboard expression

say I have ${2 + 5} apples!   # Evaluates arbitrary Python expressions
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
tp @a ~10 ~ ~   # Compiles to: tp @a ~10 ~ ~
scoreboard players set pack_x __pack__vars__ 5
execute store result storage flare:macro arg_0 int 1 run scoreboard players get pack_x __pack__vars__
function pack:macro_0 with storage flare:macro
say I have 7 apples!   # Evaluates arbitrary Python expressions
```

```mcfunction [macro_0.mcfunction]
$scoreboard players set @s my_score $(arg_0)   # Injects the scoreboard expression
```

:::

## Multi-line Commands

Flare natively supports multi-line commands without needing quotes. The preprocessor tracks your bracket indentation:

::: code-group

```python [Flare]
summon cow ~ ~ ~ {
    "CustomName": '"Bessie"',
    "Invulnerable": 1b
}
```

```mcfunction [__init__.mcfunction]
summon cow ~ ~ ~ { "CustomName": '"Bessie"', "Invulnerable": 1b }
```

:::

## Native NBT Suffix Literals & SNBT Objects (`nbt{}` & `snbt`)

Flare natively supports Minecraft NBT type suffixes directly on numeric literals (`1b`, `1B`, `500s`, `1000000L`, `3.5f`, `2.0d`), inline `nbt{...}` compound literals with unquoted keys, and standard Python dictionaries and lists. Suffix numbers automatically evaluate to `snbt` instances, supporting full compile-time arithmetic (e.g. `1b + 3b` -> `4b`), comparisons, and formatting directly into unescaped SNBT:

::: code-group

```python [Flare]
i = 10
infinite_invisibility = {"Id": 14b, "Duration": 999999, "Amplifier": 1b + 0b, "ShowParticles": 0b}

summon chicken ~$i ~ ~ {
    Tags: [f"quack{i}"],
    IsChickenJockey: true,
    Passengers: [{
        id: "minecraft:zombie",
        IsBaby: true,
        ActiveEffects: [infinite_invisibility]
    }]
}

item_nbt = nbt{display: {Name: '"My Item"'}, CustomModelData: 7}
say {item_nbt}
```

```mcfunction [__init__.mcfunction]
summon chicken ~10 ~ ~ {Tags: ["quack10"], IsChickenJockey: true, Passengers: [{id: "minecraft:zombie", IsBaby: true, ActiveEffects: [{Id: 14b, Duration: 999999, Amplifier: 1b, ShowParticles: 0b}]}]}
data modify storage pack:vars pack_item_nbt set value {display:{Name:"\"My Item\""},CustomModelData:7}
say {item_nbt}
```

:::

::: tip NBT Smart Lexer
Flare's lexer understands Minecraft data types and compound structures natively. You don't need to quote NBT keys inside commands or `nbt{...}` compounds (`Tags:` instead of `"Tags":`), and Python variables or expressions inside `{...}` will be evaluated and formatted into minified SNBT automatically.
:::
