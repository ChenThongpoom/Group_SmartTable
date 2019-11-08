# 
# from num2words import num2words
# from subprocess import call




#Calls the Espeak TTS Engine to read aloud a Text
# call(["aplay /home/pi/Desktop/Text.wav 2>/dev/null"], shell=True)



from num2words import num2words
from subprocess import call


cmd_beg= 'espeak '
cmd_end= ' | aplay /home/pi/Desktop/noPeople.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/noPeople.wav ' # To store the voice file

text = "There is no people detected"
print(text)

#Replacing ' ' with '_' to identify words in the text entered
text = text.replace(' ', '_')

#Calls the Espeak TTS Engine to read aloud a Text
call([cmd_beg+cmd_out+text+cmd_end], shell=True)

