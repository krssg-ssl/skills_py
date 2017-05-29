import skill_node

def execute(param, state, bot_id, pub):
	skill_node.send_command(pub, state, get_command(bot_id, 0, 0, 0, 0, False))
