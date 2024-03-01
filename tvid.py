#! python3

# Used to create an HTML dump that can be pasted into a WordPress Post (or other HTML-based CMS) for a new video.
#   Also creates a timestamp dump for a YouTube video description.
# Pulls timestamps and descriptions from timestamps.txt and questions.txt to create lists of each
#   that will link to that time in the video.
# Pulls the most recent file in the specified folder, assuming that will be the video you want to upload.
# Specify a title for the video. The file will be uploaded to Wistia under the specified project
#   with the specified title. A thumbnail will be generated based upon the first frame of the video.
#       YOU WILL NEED TO OCCASIONALLY GO INTO WISTIA TO SUBCATEGORIZE VIDEOS AND FLUSH THUMBNAILS.
# The HTML dump will be copied to the clipboard. Once you've pasted the HTML dump to wherever it's going,
#   press ENTER to copy the YouTube description dump to the clipboard. The script will then close automatically.

# WARNING: VIDEO TITLE MUST BE UNIQUE. THE VIDEO WILL STILL UPLOAD,
#   BUT THE SCRIPT WILL NOT ASSIGN THE CORRECT THUMBNAIL OR PULL THE CORRECT URL.

import re, pyperclip, os, sys
from wystia import WistiaApi
from wystia import WistiaUploadApi

# Defines minute- and second-pulling regex
GetMin, GetSec= re.compile(r'\((\d\d)'), re.compile(r'(\d\d)\)')

# Creates timestamp and question lists from timestamps.txt and questions.txt
with open(os.path.join(sys.path[0], 'timestamps.txt')) as f:
    tslist = f.readlines()
tslist = [x.strip() for x in tslist]
with open(os.path.join(sys.path[0], 'questions.txt')) as f:
    qlist = f.readlines()
qlist = [x.strip() for x in qlist]

# Creates lists of minutes and seconds for timestamps and questions
tsmin, tssec, qmin, qsec = [GetMin.findall(i) for i in tslist if str(i) != '()'], [GetSec.findall(i) for i in tslist if str(i) != '()'], [GetMin.findall(i) for i in qlist if str(i) != '"?" ()'], [GetSec.findall(i) for i in qlist if str(i) != '"?" ()']
tsmin, tssec, qmin, qsec = [item for sublist in tsmin for item in sublist], [item for sublist in tssec for item in sublist], [item for sublist in qmin for item in sublist], [item for sublist in qsec for item in sublist]

# Gets the latest file added to `search_dir` and isolates the name of the video for upload
search_dir = r'ENTER FILEPATH HERE'
os.chdir(search_dir)
vids = [os.path.join(search_dir, f) for f in filter(os.path.isfile, os.listdir(search_dir))]
vids.sort(key=lambda x: os.path.getctime(x))
vidlatest = vids[-1]
vidsplit = vidlatest.split('\\')
vidname = vidsplit[-1][:-4]

# Prints lists and latest video for verification before continuing
print('TIMESTAMPS:\n')
for i in tslist:
    if str(i) != '()':
        print(i)
print('\nList of minutes:')
print(tsmin)
print('\nList of seconds:')
print(tssec)
print('\n----------\n\nQUESTIONS:\n')
for i in qlist:
    if str(i) != '"?" ()':
        print(i)
print('\nList of minutes:')
print(qmin)
print('\nList of seconds:')
print(qsec)
print(f'\n----------\n\nMost recent video: {vidlatest}\nWistia video name: {vidname}')
a = input('\n\nPress ENTER to continue. . .')

# Asks for the title of the video, then uploads to Wistia under that title
WistiaApi.configure('ENTER WISTIA API KEY HERE')
project = 'ENTER WISTIA PROJECT ID# HERE'
print('\nUploading video. . .')
vidupload = WistiaUploadApi.upload_file(vidlatest, project, vidname)
assert vidupload.created
print('Upload complete.')

# Gets hashed_id of the video, needed for HTML dump and thumbnail creation
video = WistiaApi.list_videos(project, vidname)
vidid = video[0].hashed_id

# Generates image from first frame of video, sets that as the thumbnail
thumbstart = video[0].assets[0].url[:-3]
thumbend = f'{thumbstart}jpg?video_still_time=0'
print('\nAssigning thumbnail. . .')
tn = WistiaUploadApi.upload_link(thumbend, project, f'{vidname}_TN')
assert tn.created
WistiaApi.update_video(vidid, thumbnail_media_id=tn.hashed_id)
a = input('Thumbnail assignment complete.\n\nPress ENTER to generate HTML. . .')

# Creates the HTML dump and adds it to the clipboard

# Wistia embed, start of unordered list
outputKB = f'<p style="text-align: center;"><script src="https://fast.wistia.com/embed/medias/{str(vidid)}.jsonp" async></script><script src="https://fast.wistia.com/assets/external/E-v1.js" async></script><span class="wistia_embed wistia_async_{str(vidid)} popover=true popoverAnimateThumbnail=true" style="display: inline-block; height: 480px; width: 600px;"> </span></p>\n<ul>\n'
# List items from timestamps.txt
if len(tsmin) > 0:
    for x, i in enumerate(tslist):
        # if statement ignores lines that only contain `()` and nothing else, i.e., empty lines in timestamps.txt
        if str(i) != '()':
            outputKB += f' 	<li><a href="#wistia_{str(vidid)}?time={str(tsmin[x])}m{str(tssec[x])}s">{str(i)}</a></li>\n'
# Separator between timestamps.txt and questions.txt lists
outputKB += '</ul>\n<ul>\n'
# List items from questions.txt
if len(qmin) > 0:
    for x, i in enumerate(qlist):
        if str(i) != '"?" ()':
            outputKB += f' 	<li><a href="#wistia_{str(vidid)}?time={str(qmin[x])}m{str(qsec[x])}s">{str(i)}</a></li>\n'
# Unordered list closing tag
outputKB += f'</ul>'

# Copies HTML dump to clipboard
pyperclip.copy(outputKB)
a = input('\n\nHTML copied to clipboard. Press ENTER to generate YouTube timestamps. . .')

# Creates the YouTube timestamp dump
outputYT = ''
if len(tsmin) > 0:
    for x, i in enumerate(tslist):
        if str(i) != '()':
            outputYT += f'{str(tsmin[x])}:{str(tssec[x])} {str(i[:-8])}\n'
outputYT += '\n'
if len(qmin) > 0:
    for x, i in enumerate(qlist):
        if str(i) != '"?" ()':
            outputYT += f'{str(qmin[x])}:{str(qsec[x])} {str(i[:-8])}\n'

# Replaces any HTML tags, such as <strong> or <em>, with * so the inner text is rendered in bold
r = re.compile('<.*?>', re.DOTALL)
outputYT = r.sub(r'*', outputYT)

# Copies YouTube timestamp dump to clipboard
pyperclip.copy(outputYT)
print('\nYouTube timestamps copied to clipboard. Have a nice day.')
