# RLSwitchingNetworks

Switching Networks Environment
An environment that simulates a switching network from the paper titled "A Formal Analysis of AlphaGo Zero with Application to Switch Scheduling"

## Parameters:

lambda_i_j = n x n arrival/matching matrix, input i -> output j // T be

## Observations:  

Q_n : n x n the number and type of packet in each input queue, in order

## Actions:

[n length binary vector] = Each entry corresponds to which output the input queue is subtracting from

Validity check:

There is something that can go to output queue
There are no repeats in action queue  

## Transition:

Subtract 1 from the column for Else: Don't remove the element

Reward: -sum(Q_n) after taking action  
## Example:  
<pre>

n = 2 
lambda matrix:  
[0.2 0.3   
0.4 0.5]

Observation:                
         outputs    
inputs A [2 3   
       B  4 5]  

Action = [2,1] 

Observation:
         outputs   
inputs A [1 3  
       B  4 4]  

Reward: -11

</pre>

