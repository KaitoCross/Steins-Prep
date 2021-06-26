import re
import os
import sys
import unicodedata
from os import listdir
from os.path import isfile, join
import pykakasi
import csv


def romanize(jpn_text):
	table = dict(zip(map(ord,u'。•、？'),map(ord,u'...,?')))
	return unicodedata.normalize('NFKC',conv.do(jpn_text)).translate(table)

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
	chapterfile = filename.split('.')[0]
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
	if not characterId or not c_line:
		print(characterId)
		print(c_line)
		print(sliced_line)
		print(line)
		print("Something has gone wong!")
	return {"name": character, "line": c_line, "chapter": chapter, "chapterfile": chapterfile, "audioId": audioId, "characterId": characterId, "og": is_OG_SG}
	
linedict = {}
audioCsvLineDict = {}
fileList = []
mypath = os.path.dirname(os.path.abspath(__file__))
#scriptpath = mypath + "/dialoguescripts"
scriptpath = sys.argv[1]
audioidpath = sys.argv[2]
newpath = sys.argv[3]
fileList.sort()
fullOkabe = "fullOkabe"
currChapter="1"
oldChapter="0"
fullgame_name = ""
oggFilenames={}

kakasi = pykakasi.kakasi()
kakasi.setMode("H","a")
kakasi.setMode("K","a")
kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
kakasi.setMode("s", True) # add space, default: no separator
kakasi.setMode("C", True) # capitalize, default: no capitalize
conv = kakasi.getConverter()

AudioFilesCSV = csv.reader(open(audioidpath, "r"),delimiter=';')
for row in AudioFilesCSV:
	oggFilenames[row[1]]=row[0]

#print(oggFilenames)

if scriptpath and newpath:
	fileList = [f for f in listdir(scriptpath) if isfile(join(scriptpath, f)) and "SG" in f]
	for filename in fileList:
		file = open(scriptpath+"/"+filename,"r", encoding="utf8")
		if file:
			#print(filename)
			for line in file:
				cleaned_str = clean_str(line)
				line_props = lineclassify(cleaned_str,filename)
				audio_id = line_props["audioId"]
				if not audio_id:
					continue
				if line_props["characterId"] in audioCsvLineDict:
					audioCsvLineDict[line_props["characterId"]].append(line_props["line"]+"|"+romanize(line_props["line"])+"|"+oggFilenames[audio_id])
				else:
					audioCsvLineDict[line_props["characterId"]] = [line_props["line"]+"|"+romanize(line_props["line"])+"|"+oggFilenames[audio_id]]


if (scriptpath and newpath):
	for character in audioCsvLineDict:
		#print("LOL HIER KOMMEN FILES\n")
		#print(character)
		charfile = open(newpath+"/"+"character-"+character+".txt","w", encoding="utf-8") 
		for line in audioCsvLineDict[character]:
			charfile.write(line+"\n")
		charfile.close()
