# Entity Selectors

Selectors in Flare are powerful proxy objects. They work both as execute context managers and as NBT path proxies.

## As Context Managers

Use any selector directly in a `with` statement:

::: code-group

```python [Flare]
with @a:
    say Hello to all players!

with @a[distance="..10"]:
    say You're close!
```

```mcfunction [__init__.mcfunction]
execute as @a run say Hello to all players!
execute as @a[distance="..10"] run say You're close!
```

:::

## Terminal Commands on Selectors

Call arbitrary Minecraft commands directly on a selector as a method:

```python
@a[distance="..10"].kill()
@s.teleport(10, 20, 30)
```

## Iterating Selectors

Loop through a selector using a `for` loop. The loop variable acts as a proxy for `@s`:

::: code-group

```python [Flare]
for s in @a:
    s.kill()
    s.tp(@p)
```

```mcfunction [__init__.mcfunction]
execute as @a run function pack:___init__/with_0
```

```mcfunction [___init__/with_0.mcfunction]
kill @s
tp @s @p
```

:::

## Selector as NBT Path

Any attribute access on a selector that is **not** called as a method automatically evaluates as an **NBT data path** on that entity:

```python
inv = @s.Inventory         # NBT path: 'Inventory' on @s
@s.Inventory[0].Count = 10  # Flare infers 'Count' is a Byte automatically!
@s.Pos[1] = 20.5
```

### Generic Typed Selectors

By default, an untyped `selector("@a")` acts as a union of all possible entity properties in the game. Flare dynamically builds a fallback schema that merges all entity properties together, allowing standard properties (like `Health` or `foodLevel`) to be statically typed as shorts/ints respectively, even without explicit typing.

For precision, you can cast your selector to a specific entity struct using Python type hints, simply by instantiating the struct class directly with a target string:

::: code-group

```python [Flare]
from flare.nbt import Player, Zombie

# Strictly typed to the Player struct
sp = Player(@a)
sp.foodLevel = 20

# Strictly typed to the Zombie struct
sz = Zombie(@e[type=zombie])
sz.IsBaby = True
```

```mcfunction [__init__.mcfunction]
data modify entity @a foodLevel set value 20
data modify entity @e[type=zombie] IsBaby set value Trueb
```

:::

If you access an invalid or unknown property on a selector, Flare gracefully falls back to an untyped `NBTType.Unknown`, preserving dynamic flexibility.

For entirely custom NBT data paths that Flare's schema isn't aware of, you can still use inline typecasting:

::: code-group

```python [Flare]
storage my_data test[int] = 10
```

```mcfunction [__init__.mcfunction]
data modify storage my_data test set value 10
```

:::

## Tagging Selectors

You can dynamically manage entity tags using the `.add_tag()` and `.remove_tag()` methods directly on any selector:

::: code-group

```python [Flare]
# Add a tag to all players within distance 5
close_players = selector("@a[distance=..5]")
close_players.add_tag("my_custom_tag")

# Target them later using the standard selector syntax
kill @a[tag=my_custom_tag]

# Remove the tag when done
close_players.remove_tag("my_custom_tag")
```

```mcfunction [__init__.mcfunction]
tag @a[distance=..5] add my_custom_tag
kill @a[tag=my_custom_tag]
tag @a[distance=..5] remove my_custom_tag
```

:::

## Selector Relations (`on`)

Use the `on` (or `applyon`) modifier to switch context via entity relations:

::: code-group

```python [Flare]
with on("attacker"):
    say I attacked you!

# Or using selector method syntax:
with @s.attacker():
    say Got you!
```

```mcfunction [__init__.mcfunction]
execute on attacker run say I attacked you!
execute as @s on attacker run say Got you!
```

:::

## Advancements

You can easily grant or revoke advancements from entities using the `grant_advancement` and `revoke_advancement` methods directly on a selector:

::: code-group

```python [Flare]
# Granting
@a.grant_advancement("my_namespace:my_advancement") # only my_advancement
@a.grant_advancement("my_namespace:my_advancement", criterion="my_crit") # only my_advancement my_crit
@a.grant_advancement("my_namespace:my_advancement", mode="from") # from my_advancement
@a.grant_advancement(mode="everything") # everything

# Revoking
@a.revoke_advancement("my_namespace:my_advancement") # only my_advancement
@a.revoke_advancement("my_namespace:my_advancement", mode="until") # until my_advancement
```

```mcfunction [__init__.mcfunction]
advancement grant @a only my_namespace:my_advancement
advancement grant @a only my_namespace:my_advancement my_crit
advancement grant @a from my_namespace:my_advancement
advancement grant @a everything
advancement revoke @a only my_namespace:my_advancement
advancement revoke @a until my_namespace:my_advancement
```

:::

## Entity Actions & Gameplay Helpers

Selectors provide high-level, Pythonic methods for core Minecraft gameplay actions:

::: code-group

```python [Flare]
p = @s

# Potion effects
p.effect.give("speed", duration=30, amplifier=1, show_particles=True)
p.effect.clear("slowness")

# Damage
p.damage(10, damage_type="magic", by="@e[type=zombie,limit=1]")

# Sounds & Gamemode
p.playsound("entity.experience_orb.pickup", channel="player", volume=1.0, pitch=1.2)
p.gamemode("adventure")

# Experience
p.xp.add(100)
p.xp.add_levels(5)

# Entity mounting & riding
p.ride.mount("@e[type=horse,limit=1]")
p.ride.dismount()
```

```mcfunction [__init__.mcfunction]
effect give @s speed 30 1 false
effect clear @s slowness
damage @s 10 magic by @e[type=zombie,limit=1]
playsound entity.experience_orb.pickup player @s ~ ~ ~ 1.0 1.2
gamemode adventure @s
experience add @s 100 points
experience add @s 5 levels
ride @s mount @e[type=horse,limit=1]
ride @s dismount
```

:::
