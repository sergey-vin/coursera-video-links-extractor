Video Links Extractor from Coursera
==============================

Extracts links to all lessons for others to fetch with curl later

## Why?
Well, I needed to give a few links of interesting coursera videos to my friend. The problem was that course already ended and he couldn't see videos. Luckily, auth/enrollment is not required to watch the video if you know the direct link to .mp4. For not to dig for those links manually in firebug, I wrote this small script.

Ok, ok. I didn't write it right away. I tried to search for something already existing, found https://github.com/coursera-dl/coursera/tree/master/coursera and https://gist.github.com/macias/2880753, but first was too big and the second was too php :)

## Killer features?
* usability 

You can feed the tool with any coursera's class link - like https://www.coursera.org/course/hwswinterface or https://class.coursera.org/digitalmedia-002/lecture/79 - it will find all the needed stuff by itself

* does what it says, and nothing more

In true UNIX style, it doesn't copy functionality of other's tools, just extracts urls. If you want to download actual .mp4 files - with continuation/in proper folders/on other PCs, try `curl` - just copy-paste the output of this tool and it'll invoke curl with proper arguments.

* easy-to-read code (not that you may need that while using, but still)

I don't deal that much with cache/cookies/storing passwords/etc., so code is compact and clean. Should be quite simple to understand/extend

## Usage
`  Usage: python ./extract.py user password 'coursera_class_url' [curl(default)|text|csv|urls]

  Example:  python ./extract.py user@mail.com 'SuperPass!#$%' 'https://www.coursera.org/course/hwswinterface' curl

  Example2: python ./extract.py user@mail.com 'SuperPass!#$%' 'https://class.coursera.org/digitalmedia-002/lecture/79' text`

## Example
Call it like 

`python ./extract.py user@mail.com 'SuperPass!#$%' 'https://class.coursera.org/digitalmedia-002/lecture/79' curl`

You'll get the following output (showing only first 3 lines):

`curl -C - -o 'Video_(MP4)_for_1.1_introduction_(2_28).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.2_Processing_(2_35).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.3_Running_Apps_on_Android_(3_21).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4'`

pass it to your friends, or if you want to download .mp4s yourself - just copy-paste the output to console and `curl` will download the whole stuff for you. 

Don't worry if you had to terminate in the middle - just copy paste again and `curl` will continue from the position where it stopped.

## What about those curl|text|csv|urls?
This is just a way how you want to represent the output. By default it's curl, but you can choose:
### curl
`curl -C - -o 'Video_(MP4)_for_1.1_introduction_(2_28).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.2_Processing_(2_35).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.3_Running_Apps_on_Android_(3_21).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4'`
### text
`Video (MP4) for 1.1 introduction (2:28): http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4

Video (MP4) for 1.2 Processing (2:35): http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4

Video (MP4) for 1.3 Running Apps on Android (3:21): http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4`
### csv
`name,url

Video (MP4) for 1.1 introduction (2:28),http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4

Video (MP4) for 1.2 Processing (2:35),http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4

Video (MP4) for 1.3 Running Apps on Android (3:21),http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4
`
### urls
http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4

http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4

http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4

## How to download .mp4s again?
Just paste the output to console and enjoy:

`$ curl -C - -o 'Video_(MP4)_for_1.1_introduction_(2_28).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.2%20Sonic%20Painter%20%20%5Be82173eb%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.2_Processing_(2_35).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FWk1p3%20%281280%20x%20720%29%20%5B3a791a0f%5D%20.mp4'

curl -C - -o 'Video_(MP4)_for_1.3_Running_Apps_on_Android_(3_21).mp4' 'http://d396qusza40orc.cloudfront.net/digitalmedia/recoded_videos%2FCP%20-%20Lecture%201.3_fixed_audio.38eec000f88011e3bdfc196b7e6e218b.mp4'

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current

                                 Dload  Upload   Total   Spent    Left  Speed

100 5812k  100 5812k    0     0   641k      0  0:00:09  0:00:09 --:--:--  791k

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current

                                 Dload  Upload   Total   Spent    Left  Speed

100 8556k  100 8556k    0     0   716k      0  0:00:11  0:00:11 --:--:-- 1008k

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current

                                 Dload  Upload   Total   Spent    Left  Speed

100 15.6M  100 15.6M    0     0   874k      0  0:00:18  0:00:18 --:--:-- 1395k`
