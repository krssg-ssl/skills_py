import skill_node
import math

def execute(param, state, botID):
    pCopy = copy(param)
    ballInitialpos=Vector2D()
    botPos=Vector2D(int(state.homePos[botID].x), int(state.homePos[botID].y))
    ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
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


    for i,bot in enumerate(state.homePos):
      if state.homeDetected[i] and i != botID:
        obs.append(Obstacle(bot.x, bot.y, 0, 0, 2*BOT_RADIUS))

    for i in xrange (len(state.awayDetected)):
      x = state.awayPos[i - len(state.homeDetected)].x;
      y = state.awayPos[i - len(state.homeDetected)].y;
      radius = 3.3 * BOT_RADIUS;
      obs.append(Obstacle(x,y,0,0,radius))


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
      profileFactor = MIN_BOT_SPEED
    v_x = profileFactor * math.sin(theta)
    v_y = profileFactor * math.cos(theta)

    if(dist < BOT_BALL_THRESH):
      skill_node.send_command(state.isteamyellow, botID, 0, 0, 0, 0, False)	
    else:
      skill_node.send_command(state.isteamyellow, botID, v_x, v_y, v_t, 0, False)
