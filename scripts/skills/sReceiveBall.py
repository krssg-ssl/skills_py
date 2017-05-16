import skill_node

def execute(param, state, bot_id):
     ballInitialpos=Vector2D()
     ballFinalpos=Vector2D()
     currentBotpos = Vector2D(state.homePos, botDestination)
     if(execute.framecount == 1):
       ballInitialpos = state.ballPos
       return
     elif((execute.framecount % 10) == 0):
       execute.framecount = 1
       ballFinalpos = state.ballPos
     else:
       execute.framecount+=1
       return

     a = ballFinalpos.x - ballInitialpos.x;
     b = ballFinalpos.y - ballFinalpos.y;
     c1 = currentBotpos.y*(-b) + currentBotpos.x*(-a);
     c2 = ballFinalpos.x*ballInitialpos.y - ballFinalpos.y*ballInitialpos.x;

     botDestination_x = -(a*c1 + b*c2)/(a*a + b*b)
     botDestination_y = (a*c2 - b*c1)/(a*a + b*b)
     param.GoToPointP.x = botDestination_x
     param.GoToPointP.y = botDestination_y
     param.GoToPointP.finalslope = 0
     param.GoToPointP(param)
     
     skill_node.send_command(state.isteamyellow, bot_ID, 0, 0, 0, 0, False)
	
execute.framecount=1
