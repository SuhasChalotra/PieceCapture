Bug List:
=========
(mm.dd.yyyy) - (bug no.) - description

07.22.2018 - 000.00 - While debugging, game progresses until remaining empty spot
where the debugger reports: x is out of range, x= -1 and game will not end.
Status: resolved - 07.22.2018

07.22.2018 - 001.00 - when playing Bot v Bot, the final move always seems to be [5,5]
however the previous 4 moves are not the same sequence. The final move shouldn't always be 
the same spot.
Status: resolved - 07.22.2018 - 

07.22.2018 - 002.00 - AI generally buggy. The scoring is too high. It should be more stalemate
Resolution: moved the env.alternate_player() method until after the env.step(action) call

Status: tenatively resolved -
