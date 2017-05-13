import skill_node

def execute(param, state, bot_id):
	point = Vector2D(param.DribbleTurnP.x, param.DribbleTurnP.y)
	skill_node.send_command(state.isteamyellow, bot_id, 0, 0, 0, 0, True)	

print(1)