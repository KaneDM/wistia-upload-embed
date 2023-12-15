Used to create an HTML dump that can be pasted into a WordPress Post (or other HTML-based CMS) for a new video. Also creates a timestamp dump for a YouTube video description.

Pulls timestamps and descriptions from `timestamps.txt` and `questions.txt` to create lists of each that will link to that time in the video. The script assumes the following format for pulling the minutes and seconds appropriately, but can be changed on **line 22**:  
EXPLANATION OF THE TIMESTAMP (01:02)

Pulls the most recent file in the folder specified on **line 37**, assuming that will be the video you want to upload.

You will be asked to specify a title for the video. The file will be uploaded to Wistia, using the API key specified in **line 66** and under the project specified in **line 67**, with the title you provide. A thumbnail will be generated based upon the first frame of the video.  
**WARNINGS: THE VIDEO TITLE MUST BE UNIQUE. THE VIDEO WILL STILL UPLOAD, BUT THE SCRIPT WILL NOT ASSIGN THE CORRECT THUMBNAIL OR PULL THE CORRECT URL.**  
**YOU WILL NEED TO OCCASIONALLY GO INTO WISTIA TO SUBCATEGORIZE VIDEOS AND FLUSH THUMBNAIL FILES.**

The HTML dump will be copied to the clipboard. Once you've pasted the HTML dump to wherever it's going, press ENTER to copy the YouTube description dump to the clipboard. The script will then close automatically.

There's no error handling in this script, so I highly recommend running it via the provided `tvid.bat` file after you fix the file path going to the script. That way, if it crashes, you'll have a chance to read the log before the window closes.
