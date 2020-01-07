import re
import os
import sys
from os import listdir
from os.path import isfile, join

def clean_str(clearme):
	loopy = re.split('\[[0-9]+\]|\[color index="[0-9a-fA-F]+"\]|\[%p\]|\n|」|「|”|“|\[rubyBase\]|\[ruby\-base\]|\[center\]|\[rubyTextEnd\]|\[ruby\-text\-end\]|\[ruby\-text\-start\]|\[margin top="[A-Fa-f0-9]+"\]|\[margin top="\-[A-Fa-f0-9]+"\]|\[margin left="[A-Fa-f0-9]+"\]|\[margin left="\-[0-9]+"\]|\[%e\]|\[font size="[A-Fa-f0-9]+"\]|\[font size="\-[A-Fa-f0-9]+"\]|\[evaluate expr="[0-9a-zA-Z =]+"\]|\[linebreak\]|\[alt\-linebreak\]|『|』|\[auto\-forward\]|\[unk\-[a-fA-F0-9]+\]|\[auto\-forward\-1a\]|\[ruby\-center\-per\-char\]|\[parallel\]|\[%e\]|\[%18\]|\[hardcoded\-value index="[a-zA-Z0-9]+\]',clearme)
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
				if len(character) < 2:
					print(sliced_line)
			if i > 1 and sliced_line[i-1] == "line":
				c_line += sliced_line[i]
			if i > 1 and sliced_line[i-1] == "audioId":
				audioId += sliced_line[i]
			if "#characterId=" in sliced_line[i]:
				characterId += re.split("=")[1]
	else:
		character = "Narrator"
		c_line = line
	if character == "???":
		character="unknown"
	if character == "Rintaro?":
		character="Rintaro"
	if character == "Maho?":
		character = "Maho"
	if not character or not c_line:
		print(sliced_line)
		print(line)
	return {"name": character, "line": c_line, "chapter": chapter, "audioId": audioId, "characterId": characterId}
	
linedict = {"fullgame":[]}
fileList = []
mypath = os.path.dirname(os.path.abspath(__file__))
#scriptpath = mypath + "/dialoguescripts"
scriptpath = sys.argv[1]
newpath = sys.argv[2]
mailfile = sys.argv[3]
fileList.sort()
fullOkabe = "fullOkabe"
currChapter="1"
oldChapter="0"
fullgame_name = ""

if scriptpath and newpath:
	fileList = [f for f in listdir(scriptpath) if isfile(join(scriptpath, f))]
	for filename in fileList:
		file = open(scriptpath+"/"+filename,"r", encoding="utf8")
		if file:
			#print(filename)
			for line in file:
				cleaned_str = clean_str(line)
				line_props = lineclassify(cleaned_str,filename)
				if line_props["line"] == "...":
					continue
				if line_props["chapter"] != currChapter:
					for k, v in linedict.items():
						if len(linedict[k]) >= 1 and linedict[k][len(linedict[k])-1] != "<|endoftext|>":
							linedict[k].append("<|endoftext|>")
					oldChapter = currChapter
					currChapter = line_props["chapter"]
				if line_props["name"]=="Narrator":
					fullgame_name = "Rintaro's thought"
				else:
					fullgame_name = line_props["name"]
				linedict["fullgame"].append(fullgame_name+": "+line_props["line"])
				if line_props["name"] in linedict:
					if line_props["name"] == "Narrator" or line_props["name"] == "Okabe" or line_props["name"] == "Rintaro":
						if fullOkabe in linedict:
							linedict[fullOkabe].append(line_props["line"])
						else:
							linedict[fullOkabe] = [line_props["line"]]
						linedict[line_props["name"]].append(line_props["line"])
					else:
						linedict[line_props["name"]].append(line_props["line"])
				else:
					if line_props["name"] == "Narrator" or line_props["name"] == "Okabe" or line_props["name"] == "Rintaro":
						if fullOkabe in linedict:
							linedict[fullOkabe].append(line_props["line"])
						else:
							linedict[fullOkabe] = [line_props["line"]]
					linedict[line_props["name"]] = [line_props["line"]]
				#print(line_props["chapter"])
					#print(line_props["name"])
					#print(oldChapter)
					#print (filename)
			#print(lineclassify(cleaned_str))
			#print(linedict)


if mailfile:
	file = open(mailfile,"r", encoding="utf8")

	iter_mail = 0
	person = ""
	topic = "Topic: "
	topic_marker = "Topic: "
	content_m = ""
	for line in file:
		if iter_mail % 3 == 0:
			topic = clean_str(line)
		elif iter_mail % 3 == 1:
			person = clean_str(line) + "-mail"
		elif iter_mail % 3 == 2:
			content_m = clean_str(line)
			if topic:
				content_wt = topic_marker+topic+"\n"+content_m + "\n<|endoftext|>"
			else:
				content_wt = content_m + "\n<|endoftext|>"
			#if not content_m:
				#print(line)
			if person and person in linedict:
				linedict[person].append(content_wt)
			else:
				linedict[person]=[content_wt]
		else:
			print("LOL")
		iter_mail+=1

if (scriptpath and newpath) or mailfile:
	for character in linedict:
		#print("LOL HIER KOMMEN FILES\n")
		#print(character)
		charfile = open(newpath+"/"+character+".txt","w", encoding="utf-8") 
		for line in linedict[character]:
			charfile.write(line+"\n")
		charfile.close()