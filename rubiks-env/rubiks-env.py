from PIL import Image
import gym
from gym import spaces, wrappers
import numpy as np

import cube

def fig_to_array(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = numpy.fromstring(fig.canvas.tostring_argb(), dtype=numpy.uint8)
    buf.shape(w,h,4)
    buf = np.roll(buf,3,axis=2)
    return buf

def turn_cube(action: int, cubeEnv: gym.Env):

    if action == 1:
        cubeEnv.cube.move("U", 0, 1)
    elif action == 2:
	    cubeEnv.cube.move("U", 0, -1)
    elif action == 3:
	    cubeEnv.cube.move("D", 0, 1)
    elif action == 4:
	    cubeEnv.cube.move("D", 0, -1)
    elif action == 5:
	    cubeEnv.cube.move("F", 0, 1)
    elif action == 6:
	    cubeEnv.cube.move("F", 0, -1)
    elif action == 7:
	    cubeEnv.cube.move("B", 0, 1)
    elif action == 8:
	    cubeEnv.cube.move("B", 0, -1)
    elif action == 9:
	    cubeEnv.cube.move("R", 0, 1)
    elif action == 10:
        cubeEnv.cube.move("R", 0, -1)
    elif action == 11:
	    cubeEnv.cube.move("L", 0, 1)
    elif action == 12:
	    cubeEnv.cube.move("L", 0, -1)

    obs = observation_from_cube(cubeEnv.cube)
    reward = reward_from_cube(cubeEnv.cube)
    if reward:
	    done = True
    else:
	    done = False
    info = {}
    return obs, reward, done, info

def observation_from_cube(c: cube.Cube):
    return c.stickers

def reward_from_cube(c: cube.Cube):
    solved_cube = cube.Cube(3)
    solved_stickers =  solved_cube.stickers
    if np.array_equal(c.stickers, solved_stickers):
	    r = 1
    else:
        r = 0
    return r

class gymEnv(gym.Env):

    def __init__(self):
        self.cube = cube.Cube(3)
        self.action_space = spaces.Discrete(12)
        self.observation_space = spaces.MultiDiscrete(self.cube.stickers.shape)
        self.current_step = 0
        self.moves = []

    def step(self, action):
        move_dict = { 1:"U", 2:"U'",
                      3:"D", 4:"D'",
                      5:"F", 6:"F'",
                      7:"B", 8:"B'",
                      9:"R", 10:"R'",
                      11:"L", 12:"L'"}
        self.moves.append(move_dict[action + 1])
        obs, done, reward, info = turn_cube(action, self)
        return obs, done, reward, info

    def reset(self):
        self.current_step = 0
        for e in range(20):
            self.step(self.action_space.sample())
        self.shuffle = self.moves
        self.moves = []
        return observation_from_cube(self.cube)

    def render(self, mode="rgb_array"):
        print("rendering")
        print("".join(self.moves))
        f = self.cube.render()
        f.suptitle("".join(self.shuffle))
        num_moves = len(self.moves)

        print(self.moves.count("\n"))
        if num_moves > 30 and num_moves < 60:
            if self.moves.count("\n") < 1:
                 self.moves.insert(30, "\n")

        elif num_moves > 60 and num_moves < 90:
            if self.moves.count("\n") < 2:
                  self.moves.insert(60, "\n")
        elif num_moves > 90:
            if self.moves.count("\n") < 3:
                self.moves.insert(90, "\n")
        f.text(0, 0, "".join(self.moves))

        self.current_step += 1

        return fig_to_array(f)
