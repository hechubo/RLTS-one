from rl_env_inc_one import TrajComp
from rl_brain_one import PolicyGradient
import matplotlib.pyplot as plt
import time

def run_online(elist): # Validation
    eva = []
    total_len = []
    for episode in elist:
        #print('online episode', episode)
        total_len.append(len(env.ori_traj_set[episode]))
        buffer_size = int(ratio*len(env.ori_traj_set[episode]))
        # if buffer_size < 3:
        #     continue
        steps, observation = env.reset(episode, buffer_size)
        for index in range(buffer_size, steps):
            if index == steps - 1:
                done = True
            else:
                done = False
            action = RL.fix_choose_action(observation)
            #action = RL.quick_time_action(observation) #use it when your model is ready for efficiency
            observation_, _ = env.step(episode, action, index, done, 'V') #'T' means Training, and 'V' means Validation
            observation = observation_
        env_out_put_err,_=env.output(episode, 'V')
        eva.append(env_out_put_err) #'T' means Training, 'V' means Validation, and 'V-VIS' for visualization on Validation
    return eva
        
def run_comp(): #Training
    check = 999999
    training = []
    validation = []
    Round = 10
    while Round!=0:
        Round = Round - 1
        for episode in range(0, traj_amount):
            #print('training', episode)
            buffer_size = int(ratio*len(env.ori_traj_set[episode]))
            # extreme cases
            # if buffer_size < 3:
            #     continue
            steps, observation = env.reset(episode, buffer_size)
            for index in range(buffer_size, steps):
                #print('index', index)
                if index == steps - 1:
                    done = True
                else:
                    done = False
                
                # RL choose action based on observation
                action = RL.pro_choose_action(observation)
                #print('action', action)
                # RL take action and get next observation and reward
                observation_, reward = env.step(episode, action, index, done, 'T') #'T' means Training, and 'V' means Validation
                
                RL.store_transition(observation, action, reward)
                
                if done:
                    vt = RL.learn()
                    break
                # swap observation
                observation = observation_
            train_e = env.output(episode, 'T') #'T' means Training, 'V' means Validation, and 'V-VIS' for visualization on Validation
            show = 50
            if episode % show == 0:
                 eva = run_online([i for i in range(traj_amount, traj_amount + valid_amount - 1)])
                 #print('eva', eva)
                 res = sum(eva)/len(eva)
                 training.append(train_e)
                 validation.append(res)
                 print('Training error: {}, Validation error: {}'.format(sum(training[-show:])/len(training[-show:]), res))
                 RL.save('./save/'+ str(res) + '_ratio_' + str(ratio) + '/trained_model.ckpt')
                 print('Save model at round {} episode {} with error {}'.format(10 - Round, episode, res))
                 if res < check:
                     check = res
                 print('==>current best model is {} with ratio {}'.format(check, ratio))
    return training, validation

if __name__ == "__main__":
    # building subtrajectory env
    traj_path = '/root/geo/Geolife_out_1/'
    # traj_path = '../TrajData/Geolife_out_2/'
    traj_amount = 1000
    valid_amount = 100
    a_size = 3
    s_size = 3
    ratio = 0.1
    env = TrajComp(traj_path, traj_amount + valid_amount, a_size, s_size)
    RL = PolicyGradient(env.n_features, env.n_actions)
    # RL.load('./save/0.00048138837096097745_ratio_0.1/')
    start = time.time()
    training, validation = run_comp()
    print("Training elapsed time = %s", float(time.time() - start))