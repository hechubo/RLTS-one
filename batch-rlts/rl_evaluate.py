from rl_env_inc_one import TrajComp
#from rl_env_inc_skip import TrajComp
from rl_brain_upgraded import PolicyGradient
import matplotlib.pyplot as plt

def evaluate(elist): # Evaluation
    effectiveness = []
    for episode in elist:
        #print('online episode', episode)
        buffer_size = int(ratio*len(env.ori_traj_set[episode]))
        if buffer_size < 3:
            continue
        steps, observation = env.reset(episode, buffer_size)
        for index in range(buffer_size, steps):
            if index == steps - 1:
                done = True
            else:
                done = False
            action = RL.quick_time_action(observation) #matrix implementation for fast efficiency when the model is ready
            observation_, _ = env.step(episode, action, index, done, 'V') #'T' means Training, and 'V' means Validation
            observation = observation_
        env_output_error , _ =env.output(episode, 'V')
        effectiveness.append(env_output_error) #'T' means Training, 'V' means Validation, and 'V-VIS' for visualization on Validation
    return sum(effectiveness)/len(effectiveness)

def evaluate_skip(elist):
    effectiveness = []
    total_len = []
    skip_pts = 0
    step_pts = 0
    for episode in elist:
        #print('online episode', episode)
        total_len.append(len(env.ori_traj_set[episode]))
        buffer_size = int(ratio*len(env.ori_traj_set[episode]))
        if buffer_size < 3:
            continue
        steps, observation = env.reset(episode, buffer_size)
        step_pts = step_pts + steps - buffer_size
        for index in range(buffer_size, steps):
            if index == steps - 1:
                done = True
            else:
                done = False
            if index < env.INX:
                #print('test skip')
                skip_pts = skip_pts + 1
                continue
            action = RL.quick_time_action(observation) #matrix implementation for fast efficiency when the model is ready
            observation_, _ = env.step(episode, action, index, done, 'V') #'T' means Training, and 'V' means Validation
            observation = observation_
        env_output_error,_=env.output(episode, 'V')
        effectiveness.append(env_output_error) #'T' means Training, 'V' means Validation, and 'V-VIS' for visualization on Validation
    return sum(effectiveness)/len(effectiveness)

if __name__ == "__main__":
    # building subtrajectory env
    traj_path = '/root/geo/Geolife_out_1/'
    test_amount = 1000
    elist = [i for i in range(1000, 1000 + test_amount - 1)]
    a_size = 3 #RLTS 3, RLTS-Skip 5
    s_size = 3 #RLTS 3, RLTS-Skip 5
    ratio = 0.1
    env = TrajComp(traj_path, 2000, a_size, s_size)
    RL = PolicyGradient(env.n_features, env.n_actions)
    RL.load('/root/RLTS-one/batch-rlts/save/3.2949985227000175e-05_ratio_0.1/') #your_trained_model your_trained_model_skip
    effectiveness = evaluate(elist) #evaluate evaluate_skip
    print("%e" %effectiveness)