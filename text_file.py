from wit import Wit
import keyboard
client = Wit('V5XCXYGJCVPEANKCYIREQXQ4MGB6NOSV')

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import time

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 5)#originally .5 seconds
    return sample_width, r

def unknown_command():
    print("command not understood")
    
def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    test = True
    plan = {'create function named a',
                'backspace'
                ,'backspace'
                ,'backspace'
                ,'backspace'
                ,'move down'
                ,'create variable named b'
                ,'move down'
                ,'print function with variable b'
                ,'move down'
                ,'create function check with parameters c and d'
                }
    for j in plan:
        test = False
        response_continue = True 
        #while(response_continue):
            #print("please speak a word into the microphone. Say stop to quit.")
            #record_to_file('demo.wav')
            #print("done - result written to demo.wav")
            
            #try:     
            #   with open('demo.wav','rb') as f:
            #      resp = client.speech(f,None,{'Content-Type':'audio/wav'})
            #   response_continue = False;
            #except Exception as e:
            #    print("response issue")
        time.sleep(1)
        resp = client.message(j)
        print('Yay, got Wit.ai response: ' + str(resp))
        if str(resp['_text']).find('stop') >= 0:
            break
        if ( ('structure' in resp['entities']) and resp['entities']['structure'][0]['value'] == 'function'):
            if('function_name' in resp['entities']):
                name = resp['entities']['function_name'][0]['value']
                arguments = ""
                if 'argument' in resp['entities']:
                    for index in range(0,len(resp['entities']['argument_name'])):
                        if index!=0:
                            arguments += ','
                        arguments += resp['entities']['argument_name'][index]['value']
                keyboard.write('def '+ name+ '('+arguments+'):',0.1)        
                keyboard.send('enter,tab')

        elif ('print' in resp['entities']) and resp['entities']['print'][0]['value'] == 'print':
            if('function_name' in resp['entities']):
                name = resp['entities']['function_name'][0]['value']
                keyboard.write('def print_'+name+':')
                keyboard.send('enter,tab')
                keyboard.write('print('+name+')')
                keyboard.send('enter')
                keyboard.send('backspace')
            
        elif ('structure' in resp['entities']) and resp['entities']['structure'][0]['value'] == 'variable':
            if('function_name' in resp['entities']):
                name = resp['entities']['function_name'][0]['value']
                keyboard.write(name+ ' = 0',0.1)
                keyboard.send('enter')
            
        elif ('loop' in resp['entities']) and resp['entities']['loop'][0]['value'] == 'while loop':
            keyboard.write('while True:')
            keyboard.send('enter,tab');
        elif ('move' in resp['entities']) and (resp['entities']['move'][0]['value'] == 'back space'):
            keyboard.send('backspace')
        elif ('function_name' in resp['entities']) and (resp['entities']['function_name'][0]['value'] == 'right'):
            keyboard.send('right arrow')
        elif ('function_name' in resp['entities']) and (resp['entities']['function_name'][0]['value'] == 'left'):
            keyboard.send('left arrow')
        elif ('move' in resp['entities']) and (resp['entities']['move'][0]['value'] == 'up'):
            keyboard.send('up arrow')
        elif ('move' in resp['entities']) and (resp['entities']['move'][0]['value'] == 'down'):
            keyboard.send('down arrow')
        else:
            unknown_command();

    
    #create variables
    #backspace
    #tab
    #go up (number) lines
    #go down (number) lines
    #go left (number) lines
    #go right (number) lines
        
 
    
        
        
