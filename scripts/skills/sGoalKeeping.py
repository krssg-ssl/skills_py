import skill_node
import math

def execute(param, state, botID):
	 SParam pCopy = param
     ballInitialpos=Vector2D()
    gr_Robot_Command comm;
    botPos=Vector2D(state.homePos[botID].x, state.homePos[botID].y);
    ballPos=Vector2D(state.ballPos.x, state.ballPos.y);
    ballFinalpos=Vector2D(); botDestination=Vector2D(); point=Vector2D(); nextWP=Vector2D(); nextNWP=Vector2D()
    '''
    if(execute.framecount == 1):
			 ballInitialpos = ballPos;
	         execute.framecount+=1
	         return
    elif ((framecount % 5) == 0):
			execute.framecount = 1
			ballFinalpos = ballPos
    else:
		  execute.framecount+=1
		  return
      '''

    # if bot moves parallel to x axis (y is constant)
    botDestination_y = state.homePos[botID].y
    botDestination_x = ((botDestination.y - ballFinalpos.y) * (ballFinalpos.x - ballInitialpos.x) / (ballFinalpos.y - ballInitialpos.y)) + ballFinalpos.x

    # if bot moves parallel to y axis (x is constant)
    '''
    botDestination_x = state.homePos[botID].x
    botDestination_y = (ballFinalpos.y - ballInitialpos.y)/(ballFinalpos.x - ballInitialpos.x)*(botDestination.x - ballFinalpos.x) + ballFinalpos.y
    '''

    pCopy.GoalKeepingP.x = botDestination.x
    pCopy.GoalKeepingP.y = botDestination.y
    pCopy.GoalKeepingP.finalslope = 0
#  goToPointFast(pCopy)  # Python equivalent not found

    point.x = pCopy.GoalKeepingP.x;
    point.y = pCopy.GoalKeepingP.y;

    obs=[]
    o=obstacle()
    for i in xrange(len(state.homeDetected)):
      o.x = state.homePos[i].x
      o.y = state.homePos[i].y
      o.radius = 2 * BOT_RADIUS
      obs.append(o)

    for i in xrange (len(state.homeDetected), len(state.homeDetected) + len(state.awayDetected)):
      o.x = state.awayPos[i - state.homeDetected.size()].x;
      o.y = state.awayPos[i - state.homeDetected.size()].y;
      o.radius = 2 * BOT_RADIUS;
      obs.append(o);


    pathplanner = MergeSCurve()
    pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),botID,True)

    angle = nextWP.angle(botPos)
    dist = point.dist(botPos)
    theta = (state.homePos[botID].theta - angle)
    rot_theta = (state.homePos[botID].theta - pCopy.GoalKeepingP.finalslope) * (180 / math.pi);
    if(rot_theta > 0):
      if(rot_theta < DRIBBLER_BALL_ANGLE_RANGE):
        v_t = 0
      if(rot_theta < 45):
        v_t = -rot_theta / 10
      else:
		 v_t = -4.5
    profileFactor = MAX_BOT_SPEED
    if(profileFactor < MIN_BOT_SPEED):
      profileFactor = MIN_BOT_SPEED:
    v_x = profileFactor * math.sin(theta)
    v_y = profileFactor * math.cos(theta)

    if(dist < BOT_BALL_THRESH):
      skill_node.send_command(state.isteamyellow, botID, 0, 0, 0, 0, False)	
    else:
      skill_node.send_command(state.isteamyellow, botID, v_x, v_y, v_t, 0, False)
