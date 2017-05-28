#!/usr/bin/env python
import rospy
import sys
import math
sys.path.append('../../../tactics_py/scripts')
import tactic_factory
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import gr_Commands
sys.path.append('../../../plays_py/scripts/utils/')
from geometry import *
from config import *

class ObstacleCollisionError(Exception):
		def __init__(self, botId, oldpos, newpos, gr_robot_command):
				self.botId = botId
				self.oldpos = oldpos
				self.newpos = newpos
				self.gr_robot_command = gr_robot_command

class BotOutOfBoundsError(ObstacleCollisionError):
		def __init__(self, botId, oldpos, newpos, gr_robot_command):
				super(BotOutOfBoundsError, self).__init__(botId, oldpos, newpos, gr_robot_command)
		def __str__(self):
				return ("BotID {0} will be out of bounds of the field.\n"
				"Original Position of bot: 'x : {1}' 'y : {2}'\n"
				"Expected Position of bot: 'x : {6}' 'y : {7}'\n"
				"gr_robot_command recieved: 'veltangent : {3}' 'velnormal : {4}' 'velangular : {5}'"
				).format(self.botId, self.oldpos.x, self.oldpos.y,self.gr_robot_command.veltangent, self.gr_robot_command.velnormal, self.gr_robot_command.velangular, self.newpos.x, self.newpos.y)

class BotCollisionError(ObstacleCollisionError):
		def __init__(self, botId, oldpos, newpos, gr_robot_command, oppBotId, issameteam):
				super(BotCollisionError, self).__init__(botId, oldpos, newpos, gr_robot_command)
				self.oppBotId = oppBotId
				self.issameteam = issameteam
		def __str__(self):
				return ("BotID {0} will collide with BotID {8} of {9} team\n"
				"Original Position of bot: 'x : {1}' 'y : {2}'\n"
				"Expected Position of bot: 'x : {6}' 'y : {7}'\n"
				"gr_robot_command recieved: 'veltangent : {3}' 'velnormal : {4}' 'velangular : {5}'"
				).format(self.botId, self.oldpos.x, self.oldpos.y,self.gr_robot_command.veltangent, self.gr_robot_command.velnormal, self.gr_robot_command.velangular, self.newpos.x, self.newpos.y, self.oppBotId, "same" if self.issameteam else "opposite")


def can_collide(bot, obstacle, isbot = True):
	min_dist = BOT_RADIUS * (2 if isbot else 1)
	if (distbot.x - obstacle.x)**2 + (bot.y - obstacle.y)**2 <= min_dist**2:
		return True
	else:
		return False

def send_command(pub, state, gr_robot_command):
		"""
				team : 'True' if the team is yellow 
		"""

		# Check for validity of command
		# Constants need to be tuned
		botId = gr_robot_command.id
		oldpos = state.homePos[botId]
		theta = oldpos.theta
		botVel = Vector2D()

		# signs and trig fns might need adjustment
		botVel.x = gr_robot_command.veltangent*math.cos(theta) + gr_robot_command.velnormal*math.sin(theta)
		botVel.y = gr_robot_command.veltangent*math.sin(theta) - gr_robot_command.velnormal*math.cos(theta)
		dt = 1/30		# Needs to be adjusted

		# Currently using first order approximation (will change to second order approx later)
		newpos = Vector2D()
		newpos.x = oldpos.x + dt * botVel.x
		newpos.y = oldpos.y + dt * botVel.y

		for i, bot in enumerate(state.homePos):
			if i != botId:
				if can_collide(newpos, bot):
					raise BotCollisionError(botId, oldpos, newpos, gr_robot_command, i, True)

		for i, bot in enumerate(state.awayPos):
			if can_collide(newpos, bot):
				raise BotCollisionError(botId, oldpos, newpos, gr_robot_command, i, False)

		if ((-HALF_FIELD_MAXX < newpos.x < HALF_FIELD_MAXX) and (-HALF_FIELD_MAXY < newpos.y < HALF_FIELD_MAXY)) is False:
			raise BotOutOfBoundsError(botId, oldpos, newpos, gr_robot_command)

		# Conversion
		gr_robot_command.veltangent /= 1000
		gr_robot_command.velnormal  /= 1000

		# Creating the gr_Command to be published
		final_command = gr_Commands()
		final_command.timestamp      = rospy.get_rostime().secs
		final_command.isteamyellow   = state.isteamyellow
		final_command.robot_commands = gr_robot_command

		# Log the commands
		# print 'botId: {}: [{}]\n'.format(bot_id, final_command.timestamp)
		# print 'vel_x: {}\nvel_y: {}\nvel_w: {}\n'.format(v_x, v_y, v_w)
		# print 'kick_power: {}\nchip_power: {}\ndribble_speed:{}\n\n'.format(kick_power, chip_power, dribble)

		# Publish the command packet
		pub.publish(final_command)
