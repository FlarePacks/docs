# Items

Flare provides a powerful, fully-typed `item` class for constructing and managing Minecraft items with advanced data components natively in Python. 

## Basic Usage

The `item` class is imported directly from `flare`. It takes the base item ID (e.g. `minecraft:stone`) and allows you to append any of the natively supported Minecraft data components as Python kwargs.

::: code-group

```python [Flare]
from flare import item, selector

# Define a simple item
my_stick = item("minecraft:stick")

# Give it to a player
@a.give_item(my_stick, count=5)
```

```mcfunction [__init__.mcfunction]
give @a minecraft:stick 5
```

:::

## Data Components

Flare supports **all 80+ Minecraft Data Components** (such as `item_name`, `custom_data`, `enchantments`, `unbreakable`, etc.).

Instead of manually crafting complex SNBT strings, you can pass arguments directly into the `item()` constructor. Flare will automatically convert and serialize them.

### Boolean Components

For boolean flags (like `unbreakable`, `glider`, `jukebox_playable`), Flare translates them natively into component format.

```python
# -> minecraft:elytra[!glider,unbreakable]
broken_elytra = item("minecraft:elytra", glider=False, unbreakable=True)
```

### Text Components

For text-based components like `item_name`, `custom_name`, and `lore`, Flare integrates directly with its internal `style()` system (used by `print()`).

This allows you to construct richly formatted names dynamically!

```python
from flare import item, style

# Construct an epic named sword
epic_sword = item(
    "minecraft:diamond_sword",
    item_name=style("Blade of Flare", color="gold", bold=True, italic=False),
    unbreakable=True,
    max_damage=2000
)

# You can even use translation keys or custom hover events!
my_apple = item(
    "minecraft:apple",
    item_name=style(translate("item.minecraft.apple"), color="red")
)
```

### Advanced Components

You can also pass Python dictionaries and lists for complex data components. Flare will natively serialize them into the correct JSON/SNBT layout for you.

```python
# Custom Model Data and attributes
magic_wand = item(
    "minecraft:blaze_rod",
    custom_model_data=1001,
    custom_data={"magic": True, "mana": 50},
    enchantment_glint_override=True
)
```

## Integration with Give Command

Once you have defined your item, it integrates perfectly with the entity `selector` object!

::: code-group

```python [Flare]
from flare import item, selector

my_boat = item("minecraft:oak_boat", item_name=style("Super Boat", color="blue"))

# Give the boat to all players
@a.give_item(my_boat, count=1)
```

```mcfunction [__init__.mcfunction]
give @a minecraft:oak_boat[item_name={"color":"blue","text":"Super Boat"}]
```

:::

## Dynamic Item & Component Manipulation

In Minecraft 1.20.5+, item components can be inspected and mutated directly on entities or players. Flare provides intuitive properties on selectors (`@s.mainhand`, `@s.offhand`, `@s.inventory[i]`):

### Modifying Components on Held Items

You can mutate components dynamically using standard Python syntax:

::: code-group

```python [Flare]
from flare import selector, score, style, item

s = selector("@s")

# Mutate custom data compound
s.mainhand.custom_data.player_level = score(5)

# Increment damage component in-place
s.mainhand.damage += 1

# Set custom name component
s.mainhand.custom_name = style("Excalibur", color="gold")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set #0 __pack__temp__ 5
execute store result entity @s SelectedItem.components."minecraft:custom_data".player_level int 1 run scoreboard players get #0 __pack__temp__
execute store result score #add0 __pack__temp__ run data get entity @s SelectedItem.components."minecraft:damage"
scoreboard players add #add0 __pack__temp__ 1
execute store result entity @s SelectedItem.components."minecraft:damage" int 1 run scoreboard players get #add0 __pack__temp__
data modify entity @s SelectedItem.components."minecraft:custom_name" set value "{\"color\": \"gold\", \"text\": \"Excalibur\"}"
```

:::

### Replacing Items and Modifying Inventory Slots

Assigning an item directly to a slot executes an `item replace` command, and specific inventory slots can be accessed via `inventory[index]`:

::: code-group

```python [Flare]
from flare import selector, item

s = selector("@s")

# Replace mainhand with a new item
s.mainhand = item("diamond_sword", damage=10)

# Mutate damage in inventory slot 0
s.inventory[0].damage += 5

# Replace offhand
s.offhand.replace(item("shield"))
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
item replace entity @s weapon.mainhand with diamond_sword[damage=10]
execute store result score #add0 __pack__temp__ run data get entity @s Inventory[{Slot: 0b}].components."minecraft:damage"
scoreboard players add #add0 __pack__temp__ 5
execute store result entity @s Inventory[{Slot: 0b}].components."minecraft:damage" int 1 run scoreboard players get #add0 __pack__temp__
item replace entity @s weapon.offhand with shield
```

:::

