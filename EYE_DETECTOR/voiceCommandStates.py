
#import speech_recognition as sr
import sys
import pyttsx


def mainVoice(txt):
    engine1 = pyttsx.init()
    engine1.say(txt)
    engine1.runAndWait()
    print(txt)
    return

# def center():
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         audio = r.listen(source)
#         text = r.recognize_google(audio)
#         try:
#             print(text)
#             if 'stationary' in text:
#                 print('proceeding to stationary state')
#                 stationaryState()
#             elif 'test' in text:
#                 print('proceeding to testing state')
#                 testState()
#             elif 'up' in text :
#                 print('proceeding to rise up the table')
#                 riseUp()
#             elif 'down' in text :
#                 print('proceeding to lower down the table')
#                 lowerDown()
#             elif 'terminate' in text:
#                 engine.say("Okay. See you again")
#                 engine.runAndWait()
#         except sr.UnknownValueError :
#             print("Nothing can be heard, please say something")
#             center()


# def lowerDown(txt):
# #     r = sr.Recognizer()
# #     mic = sr.Microphone()
# #     with mic as source:
# #         try:
#     print("SOT is speaking ...")
#     engine.say(txt)
# #             engine.say("What can I do next?")
#     engine.runAndWait()
#     return 
#             center()
#         except sr.UnknownValueError :
#             print("Nothing can be heard, please say something")
#             center()


# def stopMove(txt):
#     print('SOT is speaking...')
#     engine.say(txt)
#     engine.runAndWait()
#     return


# def riseUp(txt):
# #     r = sr.Recognizer()
# #     mic = sr.Microphone()
# #     with mic as source:
# #         try:
#     print("SOT is speaking")
#     engine.say(txt)
# #             engine.say("What can I do next?")
#     engine.runAndWait()
#     return
#             center()
#         except sr.UnknownValueError :
#             print("Nothing can be heard, please say something")
#             center()


# def testState():
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         print("Say something!")
#         audio = r.listen(source)
#         text = r.recognize_google(audio)
#         try:
#             engine.say("You said :" + " ' " + text + " '")
#             print("You said :" + " ' " + text + " '")
#             engine.say("What can I do next?")
#             engine.runAndWait()
#             center()
#         except sr.UnknownValueError :
#             print("Nothing can be heard, please say something")
#             testState()
# 
# 
# def stationaryState():
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         try:
#             print("Okay, I will set the SOT to stay put")
#             engine.say("Okay, I will set the SOT to stay put")
#             engine.say("What can I do next?")
#             engine.runAndWait()
#             center()
#         except sr.UnknownValueError :
#             print("Nothing can be heard, please say something")
#             center()
mainVoice('hello')


