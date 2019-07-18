#MAGES. engine script cleaner  
###cleaning and seperating scripts for machine learning purposes

####usage:
Extract the scripts from the game using [sc3ntist/SCXParser](https://github.com/CommitteeOfZero/sc3ntist) (for Steins;Gate 0 or Chaos;Child) or [SciADVnet/ProjectAmadeus](https://github.com/CommitteeOfZero/SciAdv.Net) (For the original Steins;Gate Steam)  
Move the .txt files to a seperate, dedicated folder for each game.  
Then, to seperate the character's lines from each other, download this repository and execute in the repository folder:
```use
python3 prep_scripts.py path_to_folder_with_scripts outputfolder
if you want to seperate the e-mails as well:
python3 prep_scripts.py path_to_folder_with_scripts outputfolder path_to_emailtextfile
```
Have fun!