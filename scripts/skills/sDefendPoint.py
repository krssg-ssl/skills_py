import skill_node
import math
import sys
sys.path.insert(0, '../../../navigation_py/scripts/navigation')
import obstacle
def execute(param, state, bot_id):
    DEFEND_RADIUS = 50.0
    ob=Vector2D()
    botPos=Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    point_ball_angle = atan2(state.ballPos.y-param.DefendPointP.y,state.ballPos.x-param.DefendPointP.x)
    dpoint =Vector2D(param.DefendPointP.x + (param.DefendPointP.radius)*cos(point_ball_angle) , param.DefendPointP.y + (param.DefendPointP.radius)*sin(point_ball_angle))
    obs = []
    for i,bot in enumerate(state.homePos):
        if state.homeDetected[i]:
            obs.append(Obstacle(bot.x, bot.y, 0, 0, 3*BOT_RADIUS))


    for j,bot1 in enumerate(state.awayPos):
        if state.awayDetected[j]:
            obs.append(Obstacle(bot1.x, bot1.y, 0, 0, 3*BOT_RADIUS))

    point=Vector2D()
    nextWP = Vector2D()
    nextNWP =Vector2D()
    # calling of pathplanner has to be noticed later
    pathPlanner=MergeSCurve() 
    pathPlanner.plan(botPos,dpoint,nextWP,nextNWP,obs,len(state.homeDetected) + len(state.awayDetected),bot_id,True)
    motionAngle = ob.angle(nextWP, botPos)
    if nextNWP.valid() is True :    # this has to be checked 
        finalSlope = ob.angle(nextNWP, nextWP)
    else :
        finalSlope = ob.angle(nextWP, botPos)

    finalSlope=point_ball_angle

    turnAngleLeft = ob.normalizeAngle(finalSlope - state.homePos[bot_id].theta)
    omega = turnAngleLeft * MAX_BOT_OMEGA / (2 * PI)    #Speedup turn
    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA :
        if omega < 0 :
            omega = -MIN_BOT_OMEGA
        else : 
            omega = MIN_BOT_OMEGA
    dist = ob.dist(nextWP, botPos)  # Distance of next waypoint from the bot
    theta =  motionAngle - state.homePos[bot_id].theta   #Angle of dest with respect to bot's frame of reference
    profileFactor = (dist * 2 / MAX_FIELD_DIST) * MAX_BOT_SPEED

    if profileFactor < MIN_BOT_SPEED :
        profileFactor = MIN_BOT_SPEED
    elif profileFactor > MAX_BOT_SPEED :
		profileFactor = MAX_BOT_SPEED

    if dist < BOT_POINT_THRESH :
        if (turnAngleLeft) > -DRIBBLER_BALL_ANGLE_RANGE  and (turnAngleLeft) < DRIBBLER_BALL_ANGLE_RANGE :
            skill_node.send_command(state.isteamyellow, bot_id, 0, 0, 0, 0, True) # previous comment here was kick , needs be checked 
        else :
            skill_node.send_command(state.isteamyellow, bot_id, 0, 0, omega, 0, True)
    else :
        skill_node.send_command(state.isteamyellow , bot_id,profileFactor * sin(-theta) , profileFactor * cos(-theta), omega, 0, False)


