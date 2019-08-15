# MAGES. engine script cleaner  
### cleaning and seperating scripts for machine learning purposes

#### usage:

Extract the scripts from the game using [SciAdvDotNET/Ungelify](https://github.com/CommitteeOfZero/SciAdv.Net) and convert them to readable .txt files using [SciAdvDotNET/SC3Tools (in transition branch of SciAdvDotNET)](https://github.com/CommitteeOfZero/SciAdv.Net/tree/transition) (for original Steins;Gate Steam, Steins;Gate 0 or Chaos;Child) or [SciAdvDotNET/ProjectAmadeus](https://github.com/CommitteeOfZero/SciAdv.Net) (For the original Steins;Gate Steam)
Move the .txt files to a seperate, dedicated folder for each game.  

Then, to seperate the character's lines from each other, download this repository and execute in the repository folder:
##### prep_scripts.py
```use
python3 prep_scripts.py path_to_folder_with_scripts outputfolder
if you want to seperate the e-mails as well:
python3 prep_scripts.py path_to_folder_with_scripts outputfolder path_to_emailtextfile
```
##### prep_scripts_for_voice.py
This is a script that helps generating text-voice-pairs for Tacotron2. To generate them, you also need to extract all voice files of the game. Currently, it generates these pairs for all main characters of Steins;Gate.
Currently this script only supports scripts taken from the original Steins;Gate VN that include the audio ID. My fork of [sc3ntist/SCXParser](https://github.com/KaitoCross/sc3ntist/tree/filterPerson) is capable of providing these using the filterPerson branch of the program.  
The python script uses pykakasi to convert all japanese characters into romaji. However, that conversion tends to be inaccurate with kanji. Also, the Textline-Voicefile-Association tends to be a little off when the game character is not Kurisu. To proofread and correct the results of this script, I have created [TacoTranscribe](https://github.com/KaitoCross/TacoTranscribe)
```use
python3 prep_scripts.py path_to_folder_with_scripts outputfolder path_to_all_extracted_voicefiles
```
How the generated files looks like:
```
日本語|Nihongo|audiofilename.ogg
```

Have fun!
