name = '桌游瓜的局约皮特群 别瞎改爸爸'
status = ''

def __stop():
	status = ''

def handle(data):
	text = data['text']
	if len(text) >= 4 and text[:4] == '行动代号':
		if status == '行动代号':
			if text == '行动代号 结束':
				__stop()

	return json.dumps({'type': 'null'})