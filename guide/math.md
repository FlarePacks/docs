# Advanced Math

Flare features a complete suite of advanced mathematical primitives, enabling calculations far beyond standard integer scoreboards.

## Floating Point (`float32` & `float64`)

Flare fully implements **IEEE 754** floating-point standards natively in Minecraft using raw bit-manipulation. Perform decimal arithmetic without manually managing fixed-point scaling:

::: code-group

```python [Flare]
from flare.variables import float32, float64

# Native 32-bit floating point arithmetic
a = float32(1.5)
b = float32(2.25)
c = a * b

# Need more precision? Use 64-bit floats
d = float64(3.14159)
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __flare_stdlib__ dummy
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_4096 __pack__constant__ 4096
scoreboard players set #_2 __pack__constant__ 2
scoreboard players set #_2048 __pack__constant__ 2048
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_a_s __pack__vars__ 1
scoreboard players set pack_a_e __pack__vars__ 0
scoreboard players set pack_a_m __pack__vars__ 12582912
scoreboard players set pack_b_s __pack__vars__ 1
scoreboard players set pack_b_e __pack__vars__ 1
scoreboard players set pack_b_m __pack__vars__ 9437184
scoreboard players operation pack_c_s __pack__vars__ = pack_a_s __pack__vars__
scoreboard players operation pack_c_e __pack__vars__ = pack_a_e __pack__vars__
scoreboard players operation pack_c_m __pack__vars__ = pack_a_m __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_a_s __flare_stdlib__ = pack_c_s __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_a_e __flare_stdlib__ = pack_c_e __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_a_m __flare_stdlib__ = pack_c_m __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_b_s __flare_stdlib__ = pack_b_s __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_b_e __flare_stdlib__ = pack_b_e __pack__vars__
scoreboard players operation #__flare_stdlib_____float32_mul_b_m __flare_stdlib__ = pack_b_m __pack__vars__
function __flare_stdlib__:__float32_mul
scoreboard players operation pack_c_s __pack__vars__ = #__flare_stdlib_____float32_mul_res_s __flare_stdlib__
scoreboard players operation pack_c_e __pack__vars__ = #__flare_stdlib_____float32_mul_res_e __flare_stdlib__
scoreboard players operation pack_c_m __pack__vars__ = #__flare_stdlib_____float32_mul_res_m __flare_stdlib__
scoreboard players set pack_d_s __pack__vars__ 1
scoreboard players set pack_d_e __pack__vars__ 1
scoreboard players set pack_d_mh __pack__vars__ 105414268
scoreboard players set pack_d_ml __pack__vars__ 1803886
```

```mcfunction [__float32_mul.mcfunction]
scoreboard players operation #loc_a_0_s __flare_stdlib__ = #__flare_stdlib_____float32_mul_a_s __flare_stdlib__
scoreboard players operation #loc_a_0_e __flare_stdlib__ = #__flare_stdlib_____float32_mul_a_e __flare_stdlib__
scoreboard players operation #loc_a_0_m __flare_stdlib__ = #__flare_stdlib_____float32_mul_a_m __flare_stdlib__
scoreboard players operation #loc_b_1_s __flare_stdlib__ = #__flare_stdlib_____float32_mul_b_s __flare_stdlib__
scoreboard players operation #loc_b_1_e __flare_stdlib__ = #__flare_stdlib_____float32_mul_b_e __flare_stdlib__
scoreboard players operation #loc_b_1_m __flare_stdlib__ = #__flare_stdlib_____float32_mul_b_m __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_s __flare_stdlib__ = #loc_a_0_s __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_s __flare_stdlib__ *= #loc_b_1_s __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_e __flare_stdlib__ = #loc_a_0_e __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_e __flare_stdlib__ += #loc_b_1_e __flare_stdlib__
scoreboard players operation #a_hi __flare_stdlib__ = #loc_a_0_m __flare_stdlib__
scoreboard players operation #a_hi __flare_stdlib__ /= #_4096 __pack__constant__
scoreboard players operation #a_lo __flare_stdlib__ = #loc_a_0_m __flare_stdlib__
scoreboard players operation #a_lo __flare_stdlib__ %= #_4096 __pack__constant__
scoreboard players operation #b_hi __flare_stdlib__ = #loc_b_1_m __flare_stdlib__
scoreboard players operation #b_hi __flare_stdlib__ /= #_4096 __pack__constant__
scoreboard players operation #b_lo __flare_stdlib__ = #loc_b_1_m __flare_stdlib__
scoreboard players operation #b_lo __flare_stdlib__ %= #_4096 __pack__constant__
scoreboard players operation #__flare_stdlib_____float32_mul_res_m __flare_stdlib__ = #a_hi __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_m __flare_stdlib__ *= #b_hi __flare_stdlib__
scoreboard players operation #__flare_stdlib_____float32_mul_res_m __flare_stdlib__ *= #_2 __pack__constant__
scoreboard players operation #temp1 __flare_stdlib__ = #a_hi __flare_stdlib__
scoreboard players operation #temp1 __flare_stdlib__ *= #b_lo __flare_stdlib__
scoreboard players operation #temp2 __flare_stdlib__ = #a_lo __flare_stdlib__
scoreboard players operation #temp2 __flare_stdlib__ *= #b_hi __flare_stdlib__
scoreboard players operation #temp1 __flare_stdlib__ += #temp2 __flare_stdlib__
scoreboard players operation #temp1 __flare_stdlib__ /= #_2048 __pack__constant__
scoreboard players operation #__flare_stdlib_____float32_mul_res_m __flare_stdlib__ += #temp1 __flare_stdlib__
scoreboard players set #shift __flare_stdlib__ 1
execute if score #shift __flare_stdlib__ matches 1 run scoreboard players operation #__flare_stdlib_____float32_mul_res_m __flare_stdlib__ /= #_2 __pack__constant__
execute if score #shift __flare_stdlib__ matches 1 run scoreboard players add #__flare_stdlib_____float32_mul_res_e __flare_stdlib__ 1
```

:::

> [!WARNING]
> **Performance Impact**: `float32` and `float64` are fully software-emulated using arrays of 32-bit scoreboards. Because Minecraft lacks native floating point math, operations like multiplication, division, and transcendental math (`sin`, `exp`, etc.) on these types generate extremely large numbers of commands. They are provided as proof-of-concepts for when true arbitrary precision is absolutely necessary. For general game logic and performance-sensitive code, it is highly recommended to use `fixed` points or standard scaled `score`s instead.

## The `math` Standard Library

Flare comes bundled with a highly-optimized math framework that seamlessly hooks into standard Python modules. Because the Flare compiler automatically patches the built-in modules behind the scenes, you don't even need a special import! You can just use `import math` or `from math import sin` like normal:

```python
import math
from flare.variables import float32

x = float32(0.5)

# Trigonometry natively in Minecraft!
y = math.sin(x)
z = math.cos(y)

# Min/max natively support score comparisons
highest = max(x, y)

# Logarithms, exponents, roots, and more
log_val = math.log(x)
sqrt_val = math.sqrt(y)
pow_val = math.pow(x, 3)
```

### Supported Functions

| Category                  | Functions                                                              |
|---------------------------|------------------------------------------------------------------------|
| **Rounding & Bounds**     | `floor(x)`, `ceil(x)`, `round(x, ndigits)`, `min(*args)`, `max(*args)` |
| **Roots & Exponents**     | `sqrt(x)`, `exp(x)`, `pow(x, y)`                                       |
| **Logarithms**            | `log(x, base)`                                                         |
| **Trigonometry**          | `sin(x)`, `cos(x)`, `tan(x)`                                           |
| **Inverse Trig**          | `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)`                         |
| **Reciprocal Trig**       | `csc(x)`, `sec(x)`, `cot(x)`, `acsc(x)`, `asec(x)`, `acot(x)`          |
| **Hyperbolic**            | `sinh(x)`, `cosh(x)`, `tanh(x)`, `asinh(x)`, `acosh(x)`, `atanh(x)`    |
| **Reciprocal Hyperbolic** | `csch(x)`, `sech(x)`, `coth(x)`, `acsch(x)`, `asech(x)`, `acoth(x)`    |

> [!NOTE]
> **Dynamic Fallbacks**: Flare's math functions are designed to use specialized dunder methods (e.g., `__tan__`) if the target variable implements them. If a specific function is not implemented natively for that type, the math library dynamically falls back to established mathematical identities. For example, `tan(x)` seamlessly defaults to `sin(x) / cos(x)`, and `sinh(x)` defaults to `(exp(x) - exp(-x)) / 2`.

## Big Integers (`bigscore`)

For numbers larger than the 32-bit Minecraft limit (`2,147,483,647`), use `bigscore`. It transparently chains multiple scoreboard objectives to represent arbitrarily large numbers:

::: code-group

```python [Flare]
from flare import bigscore

# 64-bit integer by combining two 32-bit limbs
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

## Fixed Precision (`fixed`)

For simple fixed-point decimal arithmetic, use `fixed[n]` where `n` is the number of decimal places (precision = `1e-n`):

::: code-group

```python [Flare]
from flare import fixed

a = fixed[5](1.5)   # Stored as 150000 on the scoreboard
b = fixed[5](2.0)
c = a * b           # Scaling is handled automatically
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

## Type Promotion & Arithmetic Interoperability

Flare's type lattice seamlessly promotes arithmetic operands between numeric representations:

- `score` (rank 10)
- `fixed` (rank 20)
- `bigscore` (rank 30)
- `float32` (rank 40)
- `float64` (rank 50)

When performing binary operations between two different types, Flare finds the least upper bound (LUB) and promotes the lower-ranked value automatically:

::: code-group

```python [Flare]
from flare import score, fixed

s = score(10)
f = fixed(2.5)

# Automatic promotion: 's' is converted to 'fixed' before addition
res = s + f
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set #_10000 __pack__constant__ 10000
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_s __pack__vars__ 10
scoreboard players set pack_f __pack__vars__ 25000
scoreboard players operation pack_res __pack__vars__ = pack_f __pack__vars__
scoreboard players operation #add0 __pack__temp__ = pack_s __pack__vars__
scoreboard players operation #add0 __pack__temp__ *= #_10000 __pack__constant__
scoreboard players operation pack_res __pack__vars__ += #add0 __pack__temp__
```

:::

## Random Generation (`flrand`)


Flare provides a module for generating random numbers and selecting random elements natively in Minecraft, mirroring Python's standard `random` module.

```python
from flare import flrand
from flare.variables import score, nbtlist

# Generate a random integer score between 1 and 10
lucky_number = flrand.randint(1, 10)

# The bounds can also be dynamic scores!
min_val = score(5)
max_val = score(50)
dynamic_rand = flrand.randint(min_val, max_val)

# Choose a random element from an NBT sequence
my_list = nbtlist(["apple", "banana", "cherry"])
random_fruit = flrand.choice(my_list)

# Generate a random fixed-point decimal between 0.0 and 1.0
chance = flrand.random()
```

> **Note**: For advanced users, `flrand.random(type=MyClass)` provides custom hooks to generate complex random structures via `__random__` and `__rrandom__` dunder methods. See the [Internals](internals.md#random-and-rrandom-—-custom-random-generation) guide for details.

## 3D Spatial Vector Math (`vec3`)

Flare includes a native `vec3` type for 3D coordinate arithmetic, physics, and entity motion manipulation:

::: code-group

```python [Flare]
from flare import vec3

# 1. Coordinate instantiation and arithmetic
v1 = vec3(10, 20, 30)
v2 = vec3(1, 2, 3)

v3 = v1 + v2
scaled = v1 * 2

# 2. Vector operations
dot_product = v1.dot(v2)
cross_product = v1.cross(v2)
dist = v1.distance_to(v2)

# 3. Synchronizing with Entity Pos / Motion
pos = vec3.from_entity("@s", "Pos")
pos.y += 2
pos.apply_to("@s", "Pos")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard objectives add __pack__vars__ dummy
scoreboard players set #_2 __pack__constant__ 2
```

```mcfunction [__init__.mcfunction]
scoreboard players set #v0_x __pack__temp__ 10
scoreboard players set #v0_y __pack__temp__ 20
scoreboard players set #v0_z __pack__temp__ 30
scoreboard players set #v1_x __pack__temp__ 1
scoreboard players set #v1_y __pack__temp__ 2
scoreboard players set #v1_z __pack__temp__ 3
scoreboard players operation #v2_x __pack__temp__ = #v0_x __pack__temp__
scoreboard players operation #v2_x __pack__temp__ += #v1_x __pack__temp__
scoreboard players operation #v2_y __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation #v2_y __pack__temp__ += #v1_y __pack__temp__
scoreboard players operation #v2_z __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation #v2_z __pack__temp__ += #v1_z __pack__temp__
scoreboard players operation #v3_x __pack__temp__ = #v0_x __pack__temp__
scoreboard players operation #v3_x __pack__temp__ *= #_2 __pack__constant__
scoreboard players operation #v3_y __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation #v3_y __pack__temp__ *= #_2 __pack__constant__
scoreboard players operation #v3_z __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation #v3_z __pack__temp__ *= #_2 __pack__constant__
scoreboard players operation pack_dot_product __pack__vars__ = #v0_x __pack__temp__
scoreboard players operation pack_dot_product __pack__vars__ *= #v1_x __pack__temp__
scoreboard players operation pack_dot_product_4 __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation pack_dot_product_4 __pack__temp__ *= #v1_y __pack__temp__
scoreboard players operation pack_dot_product __pack__vars__ += pack_dot_product_4 __pack__temp__
scoreboard players operation pack_dot_product_5 __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation pack_dot_product_5 __pack__temp__ *= #v1_z __pack__temp__
scoreboard players operation pack_dot_product __pack__vars__ += pack_dot_product_5 __pack__temp__
scoreboard players operation #v6_x __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation #v6_x __pack__temp__ *= #v1_z __pack__temp__
scoreboard players operation #v6_x_7 __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation #v6_x_7 __pack__temp__ *= #v1_y __pack__temp__
scoreboard players operation #v6_x __pack__temp__ -= #v6_x_7 __pack__temp__
scoreboard players operation #v6_y __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation #v6_y __pack__temp__ *= #v1_x __pack__temp__
scoreboard players operation #v6_y_8 __pack__temp__ = #v0_x __pack__temp__
scoreboard players operation #v6_y_8 __pack__temp__ *= #v1_z __pack__temp__
scoreboard players operation #v6_y __pack__temp__ -= #v6_y_8 __pack__temp__
scoreboard players operation #v6_z __pack__temp__ = #v0_x __pack__temp__
scoreboard players operation #v6_z __pack__temp__ *= #v1_y __pack__temp__
scoreboard players operation #v6_z_9 __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation #v6_z_9 __pack__temp__ *= #v1_x __pack__temp__
scoreboard players operation #v6_z __pack__temp__ -= #v6_z_9 __pack__temp__
scoreboard players operation #v10_x __pack__temp__ = #v0_x __pack__temp__
scoreboard players operation #v10_x __pack__temp__ -= #v1_x __pack__temp__
scoreboard players operation #v10_y __pack__temp__ = #v0_y __pack__temp__
scoreboard players operation #v10_y __pack__temp__ -= #v1_y __pack__temp__
scoreboard players operation #v10_z __pack__temp__ = #v0_z __pack__temp__
scoreboard players operation #v10_z __pack__temp__ -= #v1_z __pack__temp__
scoreboard players set #v11_x __pack__temp__ 0
scoreboard players set #v11_y __pack__temp__ 0
scoreboard players set #v11_z __pack__temp__ 0
execute store result score #v11_x __pack__temp__ run data get entity @s Pos[0]
execute store result score #v11_y __pack__temp__ run data get entity @s Pos[1]
execute store result score #v11_z __pack__temp__ run data get entity @s Pos[2]
scoreboard players add #v11_y __pack__temp__ 2
execute store result entity @s Pos[0] double 1.0 run scoreboard players get #v11_x __pack__temp__
execute store result entity @s Pos[1] double 1.0 run scoreboard players get #v11_y __pack__temp__
execute store result entity @s Pos[2] double 1.0 run scoreboard players get #v11_z __pack__temp__
```

:::

