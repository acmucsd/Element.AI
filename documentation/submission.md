# Element.AI Submission and Evaluation

## Submission
To submit, make sure to be in the same directory as your main.py file. You can use the `cd` command to change directories until main.py is in the same directory (run `ls` to check what files are in the current directory).

Then run `tar -cvzf submission.tar.gz *` to create a **submission.tar.gz** file that forms your submission. **Remember to remove the previous one if you ran this before**.

The submission portal is available at [http://128.54.69.222:3000/competitions/Element.AI](http://128.54.69.222:3000/competitions/Element.AI).

To submit, you must
1. log into your ACM AI account (only one team member needs to do this)
2. click register and register yourself if you haven't already
3. go to the [teams page](http://128.54.69.222:3000/competitions/Element.AI/teams) and create yourself a team with a unique team name (you can't change this!)
4. from here you can check the current [leaderboard](http://128.54.69.222:3000/competitions/Element.AI/leaderboard), your team, and submit your bot's submission.tar.gz file.

On the [submission page](http://128.54.69.222:3000/competitions/Element.AI/upload), you can add a description (recommended! name your bot here) and upload the bot. To upload, click `click to add file` and find your submission.tar.gz file. Then click `Submit` at the bottom and wait until you get the "Submission Uploaded Succesfully" message at the top. It will then autoredirect you to the main page.

Once submitted, it can take a few minutes before its verified, and then starts running its first matches. To watch replays of your bot playing against others, you can go to the [teams page](http://128.54.69.222:3000/competitions/Element.AI/teams), click your team's card and then click the submission at the bottom. It will then open up submission details for that submission including ranking information, any errors that were raised, and matches. 

To watch a match, download the replay, double click to unzip, and run `python replay/replay.py replay.json` to create a watchable video of the match.

## Evaluation

During the competition when submissions are open, we will run a live, trueskill ranked leaderboard that uses every team's latest verified submission. After 6:30PM we will use the leaderboard to seed a double elimination knockout bracket and crown winners based on the results of that.

The knockout bracket will use your **latest verified or unverified submission**, so make sure you are absolutely certain that your latest submission is the one you want to use! If it fails you will lose your knockout games. So make sure to submit your agent to the leaderboard early to test it!