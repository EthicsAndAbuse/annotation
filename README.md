# annotation
annotation Python scripts

Instructions:

To use filter.py, you will need to install pandas:

        'pip install pandas'


Once installed, have json samples in the same folder as filter & tag files 
From here, can run filter with:

        'python filter.py sample_10.json'


This will take a while, there is an active print command that is trigger randomly through which can help you see if still working.
Run tag.py to annotate code:

        'python tag.py precategorised_data.json <your name>'

If you already have an annotated file, and remember the number of utterances you've annotated previously, run this to continue with the annotation:
	
	'python tag.py precategorised_data.json <your name> <num>'

where num is where you left off last time, because we count the conversations starting from 0.

if you don't feel like annotating the whole 500 things then enter q, which will save the annotations done so far.

------- RE-ANNOTATION -------------

To run the annotation with the new categories:

	'python retag.py <your name>' 

<your name>: it is CASE SENSITIVE, so put it the SAME as the one you've already annotated 

NB: make a BACK-UP copy of your previously annotated files, just for emergencies.



----------------------------------------
Feb, 23

Copy this to annotate:
	
	'python tag.py precategorised_data.json <yourname> 400'

After you're done, you should have a file called annotatedMore_yourname.json, send me that please.



Any problem, message on telegram
