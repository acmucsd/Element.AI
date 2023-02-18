# Actions and Observations

Please refer to the [Graphic Documentation]() for a more in-depth explanation of game rules with visuals. Notably, the [Graphic Documentation]() does not include the following information about action and observation structure/logic.

Please refer to the `README.md`'s in the root directory, the replay directory, and each kit for usage instructions.

## Observations

- the difference between `iter` and `curr_step` **(very important)** are defined in the [Graphic Documentation]()
- `rewards` is a dictionary where each `rewards['player_[num]']` returns the total points for that player so far
- `obs` is the observation, which tells you the state of the environment. It is structured as follows:


### Python Kit
```
{
    'player_[num]': {
        'player_num': int,
        'resetting': bool,
        'head': [x,y],
        'direction': [-1, 0] or [1, 0] or [0, 1] or [0, -1] (or [-1, -1] if resetting)
        'energy': int,
        'speed': int,
    }
    ...
    [repeat for each player]
    ...
    'board': {
        'board_state': nxn array,
        'players_state': nxn array,
    }
}
```

### Java Kit
```
{
    'player_[num]': [Player object] // See element/Player.java in the Java kit
    ...
    [repeat for each player]
    ...
}
```
NOTE: The Java Kit does *not* include `board`. In the Java kit, both nxn arrays are stored as class variables, `boardState` and `playersState`.

### Identifying Spaces

Take point `(x,y)`.

If you are using a python kit, say you defined:
```
boardState = obs['board']['board_state']
playersState = obs['board']['players_state']
```

If you are using a Java kit, the above are defined for you. Note both kits have the following values predefined:
```
TEMP = -1
UNOCCUPIED = 0
TAIL = 1
TERRITORY = 2
BOMB = 3
BOOST = 4
```

Then, we have the following checks:
```
if (boardState[x][y] == UNOCCUPIED):
    # it is unoccupied

if (boardState[x][y] == TAIL):
    # it is the tail of the player with playerNum == playersState[x][y]

if (boardState[x][y] == TERRITORY):
    # it is the territory of the player with playerNum == playersState[x][y]

if (boardState[x][y] == BOMB):
    if (playersState[x][y] != TEMP):
        # this is a bomb in the territory of the player with playerNum == playersState[x][y]
    else:
        # this is a regular bomb

if (boardState[x][y] == BOOST):
    if (playersState[x][y] != TEMP):
        # this is a boost in the territory of the player with playerNum == playersState[x][y]
    else:
        # this is a regular boost
```

## Actions
All valid actions are of the following form:
```
{
    'turn': -1, 0, or 1
}
```
`-1` means move left, `0` means move straight, `1` means move right. Both kits have a `formatAction(turn: int)` function.

Note that the Python kit returns a dict, while the java kit returns a formatted string. If you do not use `formatAction()`, please be aware of this difference.