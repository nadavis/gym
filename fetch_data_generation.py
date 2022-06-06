import gym
import time
import random
import numpy as np

"""Data generation for the case of a single block with Fetch Arm pick and place"""

ep_returns = []
actions = []
observations = []
rewards = []
infos = []

def main():
    env = gym.make('FetchPickAndPlace-v1')
    numItr = 100
    initStateSpace = "random"

    env.reset()
    print("Reset!")
    time.sleep(1)

    action = [0, 0, 0, 0]
    obs = env.reset()
    obsDataNew, reward, done, info = env.step(action)
    env.render()

    action = [0, 0, 0, 1]
    obsDataNew, reward, done, info = env.step(action)
    env.render()

    action = [2, 0, 0, 1]
    obsDataNew, reward, done, info = env.step(action)
    env.render()

    action = [0, 2, 0, 1]
    obsDataNew, reward, done, info = env.step(action)
    env.render()

    action = [0, 0, 2, 1]
    obsDataNew, reward, done, info = env.step(action)
    env.render()

    while len(actions) < numItr:
        obs = env.reset()
        #env.render()
        print("Reset!")
        print("ITERATION NUMBER ", len(actions))
        goToGoal(env, obs)
        

    fileName = "data_fetch"

    fileName += "_" + initStateSpace

    fileName += "_" + str(numItr)

    fileName += ".npz"
    
    np.savez_compressed(fileName, acs=actions, obs=observations, info=infos)

def goToGoal(env, lastObs):

    #goal = self.sampleGoal()
    goal = lastObs['desired_goal']

    #objectPosition
    objectPos = lastObs['observation'][3:6]
    gripperPos = lastObs['observation'][:3]
    gripperState = lastObs['observation'][9:11]
    object_rel_pos = lastObs['observation'][6:9]

    #print("relative position ", object_rel_pos)
    #print("Goal position ", goal)
    #print("gripper Position ", gripperPos)
    #print("Object Position ", objectPos)
    #print("Gripper state  ", gripperState)

    episodeAcs = []
    episodeObs = []
    episodeInfo = []

    object_oriented_goal = object_rel_pos.copy()
    object_oriented_goal[2] += 0.03
    
    print("Max episode steps ", env._max_episode_steps)

    timeStep = 0

    episodeObs.append(lastObs)
    
    action = [0, 0, 0, 0]
    while np.linalg.norm(object_oriented_goal) >= 0.005 and timeStep <= env._max_episode_steps:
        env.render()

        print("action", action)
        print("object_oriented_goal", object_oriented_goal)

        action = [0, 0, 0, 0]

        object_oriented_goal = object_rel_pos.copy()
        object_oriented_goal[2] += 0.03

        for i in range(len(object_oriented_goal)):
            action[i] = object_oriented_goal[i]*6

        action[len(action)-1] = 0.05

        obsDataNew, reward, done, info = env.step(action)
        timeStep += 1

        episodeAcs.append(action)
        episodeInfo.append(info)
        episodeObs.append(obsDataNew)

        objectPos = obsDataNew['observation'][3:6]
        gripperPos = obsDataNew['observation'][:3]
        gripperState = obsDataNew['observation'][9:11]
        object_rel_pos = obsDataNew['observation'][6:9]

    while np.linalg.norm(object_rel_pos) >= 0.005 and timeStep <= env._max_episode_steps :
        env.render()
        action = [0, 0, 0, 0]

        for i in range(len(object_rel_pos)):
            action[i] = object_rel_pos[i]*6

        action[len(action)-1] = -0.005

        obsDataNew, reward, done, info = env.step(action)
        timeStep += 1

        episodeAcs.append(action)
        episodeInfo.append(info)
        episodeObs.append(obsDataNew)

        objectPos = obsDataNew['observation'][3:6]
        gripperPos = obsDataNew['observation'][:3]
        gripperState = obsDataNew['observation'][9:11]
        object_rel_pos = obsDataNew['observation'][6:9]


    while np.linalg.norm(goal - objectPos) >= 0.01 and timeStep <= env._max_episode_steps :
        env.render()
        action = [0, 0, 0, 0]

        for i in range(len(goal - objectPos)):
            action[i] = (goal - objectPos)[i]*6

        action[len(action)-1] = -0.005

        obsDataNew, reward, done, info = env.step(action)
        timeStep += 1

        episodeAcs.append(action)
        episodeInfo.append(info)
        episodeObs.append(obsDataNew)

        objectPos = obsDataNew['observation'][3:6]
        gripperPos = obsDataNew['observation'][:3]
        gripperState = obsDataNew['observation'][9:11]
        object_rel_pos = obsDataNew['observation'][6:9]

    while True:
        env.render()
        action = [0, 0, 0, 0]

        action[len(action)-1] = -0.005

        obsDataNew, reward, done, info = env.step(action)
        timeStep += 1

        episodeAcs.append(action)
        episodeInfo.append(info)
        episodeObs.append(obsDataNew)


        objectPos = obsDataNew['observation'][3:6]
        gripperPos = obsDataNew['observation'][:3]
        gripperState = obsDataNew['observation'][9:11]
        object_rel_pos = obsDataNew['observation'][6:9]

        if timeStep >= env._max_episode_steps: break

    #print("Toatal timesteps taken ", timeStep)

    actions.append(episodeAcs)
    observations.append(episodeObs)
    infos.append(episodeInfo)

if __name__ == "__main__":
    main()
