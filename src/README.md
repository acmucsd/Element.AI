# [Gym API](https://www.gymlibrary.dev/api/core/#core)

## gym.Env

[`gym.Env.step()`](https://www.gymlibrary.dev/api/core/#gym.Env.step)

- Run one timestep of the environment's dynamics
- When end of episode is reached, you are responsible for calling `reset()` to reset this environment's state
- Accepts an action and returns either a tuple `(observation, reward, terminated, truncated, info)`

[`gym.Env.reset()`](https://www.gymlibrary.dev/api/core/#gym.Env.reset)

- Resets the environment to an initial state and returns the initial observation

[`gym.Env.render()`](https://www.gymlibrary.dev/api/core/#gym.Env.render)

- Compute the render frames as specified by `render_mode` attribute during initialization of the environment
- `None` (default) = no render is computed
- `human` = render returns `None`. The environment is continuously rendered in the current display or terminal. Usually for human consumption.
- `rgb_array` = return a single frame representing the current state of the environment. A frame is a numpy.ndarray with shape `(h, w, 3)` representing RGB values for an h-by-w pixel image.

## Attributes

[`Env.action_space`](https://www.gymlibrary.dev/api/core/#gym.Env.action_space)

- gives the format of valid actions

[`Env.observation_space`](https://www.gymlibrary.dev/api/core/#gym.Env.observation_space)

- gives the format of valid observations

[`Env.reward_range`](https://www.gymlibrary.dev/api/core/#gym.Env.reward_range)

- tuple corresponding to min and max possible rewards