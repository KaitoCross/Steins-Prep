import re
import os
import sys
from os import listdir
from os.path import isfile, join
import pykakasi

voiceMap={"0":{"prefix":"CRS_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "1": {"prefix":"MAY_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "2": {"prefix":"MOE_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "3": {"prefix":"RUK_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "4": {"prefix":"SUZ_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},#startFile 2 if roof suzuha is seperate
		  "12": {"prefix":"SUZ_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0}, #Roof Suzuha
		  "5": {"prefix":"FEI_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "6": {"prefix":"OKA_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 27, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "7": {"prefix":"DAR_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "8": {"prefix":"TEN_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
		  "9": {"prefix":"MAR_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0}, # NAE
		  "10": {"prefix":"NAK_", "lowVoiceID":999999999, "highVoiceID": 0, "offset": 0, "startFile": 0, "amountLines": 0, "decrementAt": [], "carry": 0},
			} 
charPropMap={}

def clean_str(clearme):
	loopy = re.split('\[[0-9]+\]|\[color index="[0-9a-fA-F]+"\]|\[%p\]|\n|」|「|”|“|\[rubyBase\]|\[ruby\-base\]|\[center\]|\[rubyTextEnd\]|\[ruby\-text\-end\]|\[ruby\-text\-start\]|\[margin top="[A-Fa-f0-9]+"\]|\[margin top="\-[A-Fa-f0-9]+"\]|\[margin left="[A-Fa-f0-9]+"\]|\[margin left="\-[0-9]+"\]|\[%e\]|\[font size="[A-Fa-f0-9]+"\]|\[font size="\-[A-Fa-f0-9]+"\]|\[evaluate expr="[0-9a-fA-F]+"\]|\[linebreak\]|\[alt\-linebreak\]|『|』',clearme)
	empty_s = ""
	for subtext in loopy:
		if subtext:
			empty_s += subtext
	#print(empty_s)
	return empty_s
	
def lineclassify(line,filename):
	character = ""
	c_line = ""
	audioId=""
	characterId=""
	chapter = "0"
	is_OG_SG = True
	if "SG0_" in filename:
		is_OG_SG = False
	chapter_part = re.split('SG0|SG',filename)
	chapter_nrs = chapter_part[1].split('_')
	if is_OG_SG:
		chapter = chapter_nrs[0]
	else:
		chapter = chapter_nrs[1]
	#print(chapter_nrs)
	#print(filename)
	sliced_line = re.split('\[|\]',line)
	if len(sliced_line) > 1:
		for i in range(0,len(sliced_line)):
			if i > 1 and sliced_line[i-1] == "name":
				character += sliced_line[i]
				#if len(character) < 2:
					#print(sliced_line)
			if i > 1 and sliced_line[i-1] == "line":
				c_line += sliced_line[i]
			if "#characterId=" in sliced_line[i]:
				characterId += re.split("=",sliced_line[i])[1]
			if i > 1 and sliced_line[i-1] == "audioId":
				audioId += sliced_line[i]
				if not c_line:
					c_line = sliced_line[i-2]
	else:
		character = "Narrator"
		c_line = line
	if character == "???":
		character="unknown"
	if character == "Rintaro?":
		character="Rintaro"
	if character == "Maho?":
		character = "Maho"
	if characterId == "12":
		characterId = "4"
	if not characterId or not c_line:
		print(characterId)
		print(c_line)
		print(sliced_line)
		print(line)
		print("Something has gone wong!")
	if characterId in voiceMap.keys():
		if int(audioId) < int(voiceMap[characterId]["lowVoiceID"]):
			voiceMap[characterId]["lowVoiceID"] = int(audioId)
		if int(audioId) > int(voiceMap[characterId]["highVoiceID"]):
			voiceMap[characterId]["highVoiceID"] = int(audioId)
		voiceMap[characterId]["amountLines"]+=1
	return {"name": character, "line": c_line, "chapter": chapter, "audioId": audioId, "characterId": characterId}
	
linedict = {}
audioCsvLineDict = {}
fileList = []
mypath = os.path.dirname(os.path.abspath(__file__))
#scriptpath = mypath + "/dialoguescripts"
scriptpath = sys.argv[1]
newpath = sys.argv[2]
audiopath = sys.argv[3]
fileList.sort()
fullOkabe = "fullOkabe"
currChapter="1"
oldChapter="0"
fullgame_name = ""

kakasi = pykakasi.kakasi()
kakasi.setMode("H","a")
kakasi.setMode("K","a")
kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
kakasi.setMode("s", True) # add space, default: no separator
kakasi.setMode("C", True) # capitalize, default: no capitalize
conv = kakasi.getConverter()


if scriptpath and newpath:
	fileList = [f for f in listdir(scriptpath) if isfile(join(scriptpath, f)) and "SG" in f]
	for filename in fileList:
		file = open(scriptpath+"/"+filename,"r", encoding="utf8")
		if file:
			#print(filename)
			for line in file:
				cleaned_str = clean_str(line)
				line_props = lineclassify(cleaned_str,filename)
				if line_props["characterId"] in linedict:
					linedict[line_props["characterId"]].append(line_props["line"]+"|"+conv.do(line_props["line"])+"|"+line_props["audioId"])
				else:
					linedict[line_props["characterId"]] = [line_props["line"]+"|"+conv.do(line_props["line"])+"|"+line_props["audioId"]]

for characterInfo in voiceMap.keys():
	voiceMap[characterInfo]["expectedLines"] = 1+int(voiceMap[characterInfo]["highVoiceID"]) - int(voiceMap[characterInfo]["lowVoiceID"]) 
	voiceMap[characterInfo]["fileList"] = set([f for f in listdir(audiopath) if isfile(join(audiopath, f)) and voiceMap[characterInfo]["prefix"] in f])
	decBy = 0
	justDecced = False
	voiceMap[characterInfo]["vID-to-file"]={}
	for voiceid in range(voiceMap[characterInfo]["lowVoiceID"],voiceMap[characterInfo]["highVoiceID"]+1):
		lowid = int(voiceMap[characterInfo]["lowVoiceID"])
		start = int(voiceMap[characterInfo]["startFile"])
		file_prefix = voiceMap[characterInfo]["prefix"]
		file_suffix=".OGG"
		oggOrigFilename = file_prefix+str(voiceid - lowid + start - decBy).zfill(4)+file_suffix
		oggPrevAltFilename = file_prefix+str(voiceid - lowid + start -1 - decBy).zfill(4)+"_2"+file_suffix
		if oggPrevAltFilename in voiceMap[characterInfo]["fileList"] and not justDecced:
			voiceMap[characterInfo]["vID-to-file"][str(voiceid)] = oggPrevAltFilename
			decBy +=1
			justDecced = True
		else:
			if oggOrigFilename in voiceMap[characterInfo]["fileList"]:
				voiceMap[characterInfo]["vID-to-file"][str(voiceid)] = oggOrigFilename
			else:
				if oggOrigFilename not in voiceMap[characterInfo]["fileList"]:
					print(oggOrigFilename+" doesnt exist")
					decBy -=1
					oggOrigFilename = file_prefix+str(voiceid - lowid + start - decBy).zfill(4)+file_suffix
					voiceMap[characterInfo]["vID-to-file"][str(voiceid)] = oggOrigFilename
			justDecced = False
#print(voiceMap)

if scriptpath and newpath:
	fileList = [f for f in listdir(scriptpath) if isfile(join(scriptpath, f)) and "SG" in f]
	for filename in fileList:
		file = open(scriptpath+"/"+filename,"r", encoding="utf8")
		if file:
			#print(filename)
			for line in file:
				cleaned_str = clean_str(line)
				line_props = lineclassify(cleaned_str,filename)
				if line_props["characterId"] in voiceMap.keys():
					oggFilename = voiceMap[line_props["characterId"]]["vID-to-file"][str(line_props["audioId"])]
					if oggFilename not in voiceMap[line_props["characterId"]]["fileList"]:
						print("ERROR File not Found!")
						print(oggFilename)
					if line_props["characterId"] in audioCsvLineDict:
						audioCsvLineDict[line_props["characterId"]].append(line_props["line"]+"|"+conv.do(line_props["line"])+"|"+oggFilename)
					else:
						audioCsvLineDict[line_props["characterId"]] = [line_props["line"]+"|"+conv.do(line_props["line"])+"|"+oggFilename]


if (scriptpath and newpath):
	for character in linedict:
		#print("LOL HIER KOMMEN FILES\n")
		#print(character)
		charfile = open(newpath+"/"+"character-"+character+".txt","w", encoding="utf-8") 
		for line in linedict[character]:
			charfile.write(line+"\n")
		charfile.close()
		if character in voiceMap.keys():
			charfile = open(newpath+"/"+"character-audio-"+character+".txt","w", encoding="utf-8") 
			for line in audioCsvLineDict[character]:
				charfile.write(line+"\n")
			charfile.close()