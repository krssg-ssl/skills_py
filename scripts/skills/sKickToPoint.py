import skill_node
import maths
import sGoToBall
import sTurnToPoint
def execute(param, state, bot_id):
    botPos=Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    ballPos=Vector2D(state.ballPos.x, state.ballPos.y)
    destPoint=Vector2D(param.KickToPointP.x, param.KickToPointP.y)
    ob = Vector2D()

    finalSlope = ob.angle(destPoint, botPos)
    turnAngleLeft = ob.normalizeAngle(finalSlope - state.homePos[bot_id].theta)  #Angle left to turn
    dist = ob.dist(ballPos, botPos)

    if dist > BOT_BALL_THRESH :
        sGoToBall.execute(param,state,bot_id)

    if math.fabs(turnAngleLeft) > SATISFIABLE_THETA/2 : # SATISFIABLE_THETA in config file
        paramt=Sparam()
        paramt.TurnToPointP.x = destPoint.x
        paramt.TurnToPointP.y = destPoint.y
        paramt.TurnToPointP.max_omega = MAX_BOT_OMEGA*3
        sTurnToPoint.execute(paramt, state, bot_id)

    skill_node.send_command(state.isteamyellow, bot_id ,0, 0, 0, param.KickToPointP.power, False)


    
      
     
    