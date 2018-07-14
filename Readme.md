Questions / Notes:
1. - AgentPlayer should be negatively rewarded for making and invalid move, correct?
- If so, does it lose a turn, and the environment goes ahead makes its move

2. - We discussed that essentially the agent's opponent is the environment itself.
Do we even need to keep track of the 'currentPlayer?'. We would if, for instance, 
the Agent is playing against a human player.

- If we do keep track of the current player in the context of an Agent vs Human game, where would
we prompt the human for input for a move? I'd imagine in the step function? The human would
essentially be the 'environment' and our Agent would still be reacting to it?

3. -Player1 needs to always be an Agent. Player 2 must be a Bot or a human.

- I guess we will save the Agent v Human scenario until the Agent is fully trained?

4. - Placing a piece. The Game needs to signal that the move just placed has caused score(s) 
to occur (we do this by supplying a return value to the Game.make_move method) for example,
make_move returns bool_valid_move, int_p1_point_scored, int_p2_point_scored

5. Here are some scenarios where we think about how rewards are calculated:

REWARDS:
1) Agent moves and scores. Bot makes subsequent move and scores as well. What are the rewards?
2) Agent moves and scores. Bot makes subsequent move but does not score. Rewards?

Should we give the agent 1 point but then subtract 1 from it when the Bot scores and returns
an observation (net zero), or should we give agent 2 points and then subtract 1 if Bot scores?

What if the agent makes an invalid move and then the bot subsquently scores on its next move?
-2 should be the reward, right?
