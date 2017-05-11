#!/usr/bin/env python
import rospy
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import gr_Commands

pub = rospy.Publisher('/bot_data', gr_Commands, queue_size=1000)
rospy.init_node('skills_node', anonymous=True)

gr_command = gr_Robot_Command()
final_command = gr_Commands()

def send_command(team, bot_id, v_x, v_y, v_w, kick_power, dribble, chip_power=0):
	"""
		team : 'True' if the team is yellow 
	"""
	
	# Set the command to each bot
	gr_command.id          = bot_id
	gr_command.wheelsspeed = 0
	gr_command.veltangent  = v_y
	gr_command.velnormal   = v_x
	gr_command.velangular  = v_w
	gr_command.kickspeedx  = kick_power
	gr_command.kickspeedz  = chip_power
	gr_command.spinner     = dribble

	final_command.timestamp      = rospy.get_rostime().secs
	final_command.isteamyellow   = team
	final_command.robot_commands = gr_command

	# Log the commands
	rospy.loginfo('[{}]: Sending robot command bot_id: {}\n'.format(final_command.timestamp, bot_id))
	rospy.loginfo('vel_x: {}\nvel_y: {}\nvel_w: {}\n'.format(v_x, v_y, v_w))
	rospy.loginfo('kick_power: {}\nchip_power: {}\ndribble_speed:{}\n\n'.format(kick_power, chip_power, dribble))

	# Publish the command packet
	pub.publish(final_command)
