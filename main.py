#imports
import keyboard, shutil, os, stat, time, configparser, json

#functions
def on_rm_error(func, path, excinfo):
	os.chmod(path, stat.S_IWRITE)
	os.rmdir(path)

def pick_skin(skin, skinNum):
	shutil.rmtree(osuFolder+"\\Skins\\SkinCycle", onerror = on_rm_error)
	shutil.copytree(osuFolder+"\\Skins\\"+skin, osuFolder+"\\Skins\\SkinCycle")
	print(skin)
	global currentSkin
	currentSkin = skinNum
	keyboard.press('ctrl+alt+shift+s')
	time.sleep(0.05)
	keyboard.release('ctrl+alt+shift+s')

#load vars from config
config = configparser.ConfigParser()
config.read('config.ini')

osuFolder = config.get('DEFAULT','osu!directory')
skinList = json.loads(config.get('DEFAULT','skins'))
currentSkin = 0

#setup
if(osuFolder == "" or (not skinList)):
	print("Missing osu! directory or skins: Did you declare them in config.ini?")
	print("press space to continue...")
	keyboard.wait('space')
else:
	if(len(skinList) > 9):
		for x in range(9, len(skinList), 1):
			del skinList[x]

	if(not os.path.exists(osuFolder+"\\Skins\\SkinCycle")):
		os.mkdir(osuFolder+"\\Skins\\SkinCycle")
	
	#hotkey setup
	for x in range(1,len(skinList)+1,1):
		keyboard.add_hotkey('alt+'+str(x), pick_skin, args=[skinList[x-1],x-1])
	
	#listen for hotkey press and go to next skin
	while True:
		keyboard.wait('alt+s')
		currentSkin+=1
		if(currentSkin >= len(skinList)):
			currentSkin = 0
		#clear active skin folder and copy new skin files over
		shutil.rmtree(osuFolder+"\\Skins\\SkinCycle", onerror = on_rm_error)
		shutil.copytree(osuFolder+"\\Skins\\"+skinList[currentSkin], osuFolder+"\\Skins\\SkinCycle")
		#let me know
		print(skinList[currentSkin])
		keyboard.press('ctrl+alt+shift+s')
		time.sleep(0.05)
		keyboard.release('ctrl+alt+shift+s')