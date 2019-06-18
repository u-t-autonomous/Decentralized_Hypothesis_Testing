from gridworld import *
from mdp import MDP
# from tqdm import tqdm
nrows = 10
ncols = 10
goodtargets = {0}
initial = [33,40,7,80]
moveobstacles = []
targets = [[0],[9],[20],[95]]
obstacles = []


regionkeys = {'pavement','gravel','grass','sand','deterministic'}
regions = dict.fromkeys(regionkeys,{-1})
regions['pavement']= range(nrows*ncols)
# regions_det = dict.fromkeys(regionkeys,{-1})
# regions_det['deterministic'] = range(nrows*ncols)

gwg = Gridworld(initial, nrows, ncols, len(initial), targets, obstacles,moveobstacles,regions)
# det_gw = Gridworld(initial, nrows, ncols, len(initial), targets, obstacles,moveobstacles,regions_det)
gwg.render(multicolor=True)
gwg.draw_state_labels()
# gwg.save('Examples/example_7x5.png')
#
states = range(gwg.nstates)
alphabet = [0,1,2,3] # North, south, west, east
transitions = []
for s in states:
    for a in alphabet:
        for t in np.nonzero(gwg.prob[gwg.actlist[a]][s])[0]:
            p = gwg.prob[gwg.actlist[a]][s][t]
            transitions.append((s, alphabet.index(a), t, p))

mdp = MDP(states, set(alphabet),transitions)

# V, goodpolicy = mdp.max_reach_prob(goodtargets, epsilon=0.0001)
# V, badpolicy = mdp.max_reach_prob(badtargets, epsilon=0.0001)
randomness = 0
policy = []
for k in targets:
    R = dict([(s,a,next_s),0.0] for s in mdp.states for a in mdp.available(s) for next_s in mdp.post(s,a) )
    R.update([(s,a,next_s),1.0] for s in mdp.states  for a in mdp.available(s) for next_s in mdp.post(s,a) if next_s in set(k) and s in set(k))
    V,goodpolicy =  mdp.T_step_value_iteration(R,40)
    policy.append(goodpolicy)
# MC = mdp.MC_Probability(initial,goodpolicy,2)
# obs = mdp.observation(goodpolicy,27,initial,2)

gwg.play(True,policy,mdp)
# bad_MC = mdp.construct_MC(badpolicy,'Examples/7x5_bad.txt')

# Construct product mdp
# states = [(s1,s2) for s1 in gwg.states for s2 in gwg.states]
# product_trans = []
# for s1 in states:
#     for s2 in states:
#         for a in alphabet:
#             p1 = gwg.prob[gwg.actlist[a]][s1[0]][s2[0]]
#             p2 = bad_MC[(s1[1],s2[1])]
#             if p1*p2>0:
#                 product_trans.append((s1,a,s2,p1*p2))
#
# product_mdp = MDP(states, set(alphabet),product_trans)
# # product_pomdp = POMDP(product_mdp,gwg)
# product_mdp.write_to_file('Examples/7x5_productmdp_bad',(30,4))
# # product_pomdp.write_to_file('Examples/7x5_productpomdp_bad',(30,4))

# # Construct product mdp
# states = [(s1,s2) for s1 in gwg.states for s2 in gwg.states]
# product_trans2 = []
# for s1 in states:
#     for s2 in states:
#         for a in alphabet:
#             p1 = gwg.prob[gwg.actlist[a]][s1[0]][s2[0]]
#             p2 = good_MC[(s1[1],s2[1])]
#             if p1*p2>0:
#                 product_trans2.append((s1,a,s2,p1*p2))
#
# product_mdp2 = MDP(states, set(alphabet),product_trans2)
# # product_pomdp2 = POMDP(product_mdp2,gwg)
# product_mdp2.write_to_file('Examples/7x5_productmdp_good',(30,4))
# # product_pomdp2.write_to_file('Examples/7x5_productpomdp_good',(30,4))
#
