import skill_node
import math

POINTPREDICTIONFACTOR = 2

#some constants yet to be defined

def execute(param,state,bot_id):
    obs = []
    for i in range(0,len(state.homeDetected)):
        if state.homeDetected[i]:
            o = obstacle()     
            o.x=state.homePos[i].x
            o.y=state.homePos[i].y
            o.radius=2.5*BOT_RADIUS
            obs.append(o)

    for j in range(0,len(state.awayDetected)):
        if state.awayDetected[j]:
            o = obstacle()
            o.x=state.awayPos[j].x
            o.y=state.awayPos[j].y
            o.radius=2.5*BOT_RADIUS
            obs.append(o)


    pointPos = Vector2D()
    pointPos.x = param.GoToPointP.x
    pointPos.y = param.GoToPointP.y
    point = Vector2D()
    nextWP = Vector2D()
    nextNWP = Vector2D()

    pathplanner = MergeSCurve()

    botPos = Vector2D(state.homePos[bot_id].x,state.homePos[bot_id].y)

    pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id,True)

    v = Vector2D()
    dist = v.dist(botPos,pointPos)
    maxDisToTurn = dist - 3.5 * BOT_BALL_THRESH
    angleToTurn = v.normalizeAngle((param.GoToPointP.finalslope)-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_OMEGA
    maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    speed = 0.0
    omega = angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

    if maxDisToTurn > 0:
        if minTurnTime > maxReachTime:
            speed = MIN_BOT_SPEED
        elif minReachTime > maxTurnTime:
            speed = MAX_BOT_SPEED
        elif minReachTime < minTurnTime:
            speed =  maxDisToTurn / minTurnTime
        elif minTurnTime < minReachTime:
            speed = MAX_BOT_SPEED
    else:
        speed = dist / MAX_FIELD_DIST * MAX_BOT_SPEED


    vec = Vector2D()
    motionAngle = vec.angle(nextWP,botPos)
    theta  = motionAngle - state.homePos[bot_id].theta

    if param.GoToPointP.align == False:
        if dist < DRIBBLER_BALL_THRESH:
            if dist < BOT_BALL_THRESH:
                skill_node.send_command(bot_id, 0, 0, 0, 0, True)
            else:
                skill_node.send_command(bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, True)

        else:
            skill_node.send_command(bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, False)

    else:
        if dist > BOT_BALL_THRESH:
            skill_node.send_command(bot_id, speed * math.sin(-theta), speed * math.cos(-theta), 0, 0, False)
        else:
            skill_node.send_command(bot_id, 0, 0, 0, 0,True)

