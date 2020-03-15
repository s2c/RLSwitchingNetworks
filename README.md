# RLSwitchingNetworks

Switching Networks Environment
An environment that simulates a switching network from the paper titled "A Formal Analysis of AlphaGo Zero with Application to Switch Scheduling"

## Parameters:

lambda_i_j = n x n arrival/matching matrix, input i -> output j 

## Observations:  

Q_n : n x n matrix that corresponds to the input and output queues

## Actions:

[n x n] Binary matrix. Each positive entry in row corresponds to which output the queue will send to

Validity check:

There is something that can go to output queue

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

