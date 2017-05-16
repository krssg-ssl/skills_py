import skill_node
import math

def execute(param, state, bot_id):
     point = Vector2D(param.DribbleToPointP.x, param.DribbleToPointP.y)
     botPos = Vector2D(state.homePos[botID].x, state.homePos[botID].y)
     ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
     ballSlope = ballPos.angle(botPos)
     ballDist  = ballPos.dist(botPos)
     ballTheta = math.fabs(ballDist.normalizeAngle(state.homePos[botID].theta - ballSlope));
     #   if(ballDist > BOT_BALL_THRESH || ballTheta > DRIBBLER_BALL_ANGLE_RANGE):
     #     return goToBall(param, state, botID) # No python equivalent found

     obs=[]
     o=obstacle()
     for i in xrange (len(state.homeDetected)):
	o.x = state.homePos[i].x
	o.y = state.homePos[i].y
	o.radius = 3 * BOT_RADIUS
	obs.append(o)

     for i in xrange(len(state.homeDetected)):
        o.x = state.awayPos[i - len(state.homeDetected)].x
        o.y = state.awayPos[i - len(state.homeDetected)].y
        o.radius = 3 * BOT_RADIUS
        obs.append(o)
        
        
     nextWP=Vector2D(); nextNWP=Vector2D

     pathplanner = MergeSCurve()
     pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),botID,True)

     if (nextWP.valid()):
      pass
      # comm.addCircle(nextWP.x, nextWP.y, 50)
      # comm.addLine(state.homePos[botID].x, state.homePos[botID].y, nextWP.x, nextWP.y)  #Python equivalent for comm not found
      
     if (nextNWP.valid()):
      pass
      # comm.addCircle(nextNWP.x, nextNWP.y, 50)
      # comm.addLine(nextWP.x, nextWP.y, nextNWP.x, nextNWP.y)
  
      # rospy.loginfo("Dribbling\n")
     dist = nextWP.dist(botPos)
     #  angle = nextWP.angle(botPos)
     angle = param.DribbleToPointP.finalslope;
     theta = nextWP(normalizeAngle(state.homePos[botID].theta - angle))
     profileFactor = 2 * dist * MAX_BOT_SPEED / MAX_FIELD_DIST
     if(math.fabs(profileFactor) < MIN_BOT_SPEED ):
       if(profileFactor < 0 ):
         profileFactor = - MIN_BOT_SPEED
       else:
         profileFactor = MIN_BOT_SPEED
         
     v_y = profileFactor * math.cos(theta)
     v_x = profileFactor * math.sin(theta)
     romega = theta / ( 2 * math.pi) * MAX_BOT_OMEGA
     if(v_y < - MAX_BACK_DRIBBLE_V_Y):
 	   v_x /= (v_y / -MAX_BACK_DRIBBLE_V_Y)
 	   v_y = -MAX_BACK_DRIBBLE_V_Y
     elif (v_y > MAX_FRONT_DRIBBLE_V_Y):
		v_x /= (v_y / MAX_FRONT_DRIBBLE_V_Y)
		v_y = MAX_FRONT_DRIBBLE_V_Y
		  
     if(v_x > MAX_DRIBBLE_V_X):
       v_y /= (v_x / MAX_DRIBBLE_V_X)
       v_x = MAX_DRIBBLE_V_X
     elif (v_x < -MAX_DRIBBLE_V_X):
 		v_y /= (v_x / -MAX_DRIBBLE_V_X)
 		v_x = -MAX_DRIBBLE_V_X
  
     if (math.fabs(theta)> SATISFIABLE_THETA):
       if(math.fabs(romega < MIN_BOT_OMEGA)):
         if(romega > 0):
           romega = MIN_BOT_OMEGA
         else:
          romega = -MIN_BOT_OMEGA;
       elif (fabs(romega) > MAX_DRIBBLE_R):
        if(romega > 0):
          romega = MAX_DRIBBLE_R
        else:
          romega = -MAX_DRIBBLE_R
     else:
       romega = 0
      
     if(dist < BOT_BALL_THRESH ):
         skill_node.send_command(state.isteamyellow, bot_id, 0, 0, 0, 0, True)	
     else:
         skill_node.send_command(state.isteamyellow, bot_id, v_x, v_y, -romega, 0, True)