import skill_node

def execute(param, state, bot_id):
    point = Vector2D(param.TurnToPointP.x, param.TurnToPointP.y)
    botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    ballPos = Vector2D(state.ballPos.x, state.ballPos.y)

    vec = Vector2D()
    finalslope = vec.angle(point, botPos)
    turnAngleLeft = vec.normalizeAngle(finalslope - state.homePos[bot_id].theta)  #Angle left to turn
    omega = 2.8 * turnAngleLeft * param.TurnToPointP.max_omega / (2 * math.pi)  #Speedup turn

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA


    v_x = omega * BOT_BALL_THRESH * 1.5
    dist = vec.dist(ballPos, botPos)

    if dist < DRIBBLER_BALL_THRESH * 4:
        return skill_node.send_command(bot_id, v_x, 0, omega, 0, True)
    else:
        return skill_node.send_command(bot_id, 0, 0, omega, 0, False)
