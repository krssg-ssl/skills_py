import skill_node
FRICTION_COEFF = 0.05
ACCN_GRAVITY = 9.80665
ANGLE_THRES =30.0
def execute(param, state, bot_id):
    point = Vector2D(param.DribbleTurnP.x, param.DribbleTurnP.y)
    botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
    radius = param.DribbleTurnP.turn_radius
    ob = Vector2D()
    finalSlope = ob.angle(point, ballPos)
    turnAngleLeft = ob.normalizeAngle(finalSlope - state.homePos[bot_id].theta)

    if turnAngleLeft>=-ANGLE_THRES*PI/180 and turnAngleLeft<=ANGLE_THRES*PI/180 :
        omega = ((turnAngleLeft)*180/ (ANGLE_THRES*PI)) * param.DribbleTurnP.max_omega
    else :
        omega=param.DribbleTurnP.max_omega*(-1 if turnAngleLeft < 0  else 1 )
        
    phi = ob.normalizeAngle(atan2(omega*omega*radius,FRICTION_COEFF*ACCN_GRAVITY))
   
    sphi=sin(phi)
    cphi=cos(phi)

    if omega >= 0 :
        v_x= omega*radius*sphi
        v_y= -omega*radius*cphi
    else :
        v_x= -omega*radius*sphi
        v_y= -omega*radius*cphi

        

        

    skill_node.send_command(state.isteamyellow, botID, v_x, v_y, omega, 0, True)