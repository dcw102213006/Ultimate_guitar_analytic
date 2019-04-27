import re
import json

#MAJOR Diatonic chord
#C major
C_diatonic = ['C:maj', 'C:maj7', 'D:min', 'D:min7', 'E:min', 'E:min7', 'F:maj', 'F:maj7', 'G:maj', 'G:7', 'A:min', 'A:min7', 'B:dim']
#Db major
Db_diatonic = ['Db:maj', 'Db:maj7', 'Eb:min', 'Eb:min7', 'F:min', 'F:min7', 'Gb:maj', 'Gb:maj7', 'Ab:maj', 'Ab:7', 'Bb:min', 'Bb:min7', 'C:dim']
#D major
D_diatonic = ['D:maj', 'D:maj7', 'E:min', 'E:min7', 'Gb:min', 'Gb:min7', 'G:maj', 'G:maj7', 'A:maj', 'A:7', 'B:min', 'B:min7', 'Db:dim']
#Eb major
Eb_diatonic = ['Eb:maj', 'Eb:maj7', 'F:min', 'F:min7', 'G:min', 'G:min7', 'Ab:maj', 'Ab:maj7', 'Bb:maj', 'Bb:7', 'C:min', 'C:min7', 'D:dim']
#E major
E_diatonic = ['E:maj', 'E:maj7', 'Gb:min', 'Gb:min7', 'Ab:min', 'Ab:min7', 'A:maj', 'A:maj7', 'B:maj', 'B:7', 'Db:min', 'Db:min7', 'Fb:dim']
#F major
F_diatonic = ['F:maj', 'F:maj7', 'G:min', 'G:min7', 'A:min', 'A:min7', 'Bb:maj', 'Bb:maj7', 'C:maj', 'C:7', 'D:min', 'D:min7', 'E:dim']
#Gb major
Gb_diatonic = ['Gb:maj', 'Gb:maj7', 'Ab:min', 'Ab:min7', 'Bb:min', 'Bb:min7', 'Cb:maj', 'Cb:maj7', 'Db:maj', 'Db:7', 'Eb:min', 'Eb:min7', 'F:dim']
#G major
G_diatonic = ['G:maj', 'G:maj7', 'A:min', 'A:min7', 'B:min', 'B:min7', 'C:maj', 'C:maj7', 'D:maj', 'D:7', 'E:min', 'E:min7', 'Gb:dim']
#Ab major
Ab_diatonic = ['Ab:maj', 'Ab:maj7', 'Bb:min', 'Bb:min7', 'C:min', 'C:min7', 'Db:maj', 'Db:maj7', 'Eb:maj', 'Eb:7', 'F:min', 'F:min7', 'G:dim']
#A major
A_diatonic = ['A:maj', 'A:maj7', 'B:min', 'B:min7', 'Db:min', 'Db:min7', 'D:maj', 'D:maj7', 'E:maj', 'E:7', 'Gb:min', 'Gb:min7', 'Ab:dim']
#Bb major
Bb_diatonic = ['Bb:maj', 'Bb:maj7', 'C:min', 'C:min7', 'D:min', 'D:min7', 'Eb:maj', 'Eb:maj7', 'F:maj', 'F:7', 'G:min', 'G:min7', 'A:dim']
#B major
B_diatonic = ['B:maj', 'B:maj7', 'Db:min', 'Db:min7', 'Fb:min', 'Fb:min7', 'E:maj', 'E:maj7', 'Gb:maj', 'Gb:maj7', 'Ab:min', 'Ab:min7', 'Bb:dim']

keys = [C_diatonic,Db_diatonic,D_diatonic,Eb_diatonic,E_diatonic,F_diatonic,Gb_diatonic,G_diatonic,
        Ab_diatonic,A_diatonic,Bb_diatonic,B_diatonic]

keyName = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

#key_profile
C = ['C','D','E','F','G','A','B']
Db = ['Db','Eb','F','Gb','Ab','Bb','C']
D = ['D','E','Gb','G','A','B','Db']
Eb = ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']
E = ['E', 'Gb', 'Ab', 'A', 'B', 'Db', 'Fb']
F = ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
Gb = ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']
G = ['G', 'A', 'B', 'C', 'D', 'E', 'Gb']
Ab = ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G']
A = ['A', 'B', 'Db', 'D', 'E', 'Gb', 'Ab']
Bb = ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
B = ['B', 'Db', 'Eb', 'E', 'Gb', 'Ab', 'Bb']
key_profile = [C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb,B]

def label_reduce(label,discard_dominant_notes=False):
    '''
    reduce chord vocabulary to majmin7 level,
    and transfer to lab format.
    '''
    #有些和弦會有符號
    #例:A# IV ->只拿A#就好
    label=label.replace('I','')
    label=label.replace('i','')
    label=label.replace('V','')
    label=label.replace('v','')
    label=label.replace('X','')
    label=label.replace('x','')
    label=label.replace('*','')
    label=label.replace('?','')
    label=label.replace('#b','')
    label=label.replace('b#','')
    label=label.strip()
    
    #如果想丟棄屬音
    #例:A#7、A#11 ->A#
    if(discard_dominant_notes):
        digit_position=len(label)
        for i, c in enumerate(label):
            if c.isdigit():
                digit_position=i
                break
        label=label[0:digit_position]

    majmin7_label = None

    if label == "N":
        majmin7_label = label
        return majmin7_label

    label = label.replace("(", "")
    label = label.replace(")", "")

    Advance_Pattern = re.compile('(.*)(\/|aug|Aug|dim|sus|add|ADD|SUS|aDD|Sus|saus|\+|\-)')
    removeRoot_label = Advance_Pattern.search(label)

    if removeRoot_label is not None:
        removeRoot_label = removeRoot_label.group(1)
    else:
        removeRoot_label = label

    Minor_Pattern = re.compile('(.*)(m)(\d?)')
    Major_Pattern = re.compile('([a-zA-Z]+)([0-9]+)')

    if "maj" not in removeRoot_label and "m" in removeRoot_label: #this label is minor related
        
        majmin7_label = Minor_Pattern.search(removeRoot_label)

        if majmin7_label is not None:
            
            chord_eval = transfer_chord_vocabulary(majmin7_label.group(1))
            if majmin7_label.group(3) == "6":
                majmin7_label = chord_eval + ":min"
            elif majmin7_label.group(3) == "7":
                majmin7_label = chord_eval + ":min" + majmin7_label.group(3)
            else: #there is no 5 degree above notes
                majmin7_label = chord_eval + ":min"

    else: #this label is major related
        if "maj" in removeRoot_label:
            removeRoot_label = removeRoot_label.split("maj")

            chord_eval = transfer_chord_vocabulary(removeRoot_label[0])
            if removeRoot_label[1] is not "" and removeRoot_label[1] is not "6" and removeRoot_label[1] is not "9":
                majmin7_label = chord_eval +":maj"+removeRoot_label[1]
            else:
                majmin7_label = chord_eval +":maj"
        elif "M" in removeRoot_label:
            removeRoot_label = removeRoot_label.split("M")

            chord_eval = transfer_chord_vocabulary(removeRoot_label[0])
            if removeRoot_label[1] is not "" and removeRoot_label[1] is not "6" and removeRoot_label[1] is not "9":
                majmin7_label = chord_eval +":maj"+removeRoot_label[1]
            else:
                majmin7_label = chord_eval +":maj"
        else:
            
            PureMajor_label = removeRoot_label
            
            removeRoot_label = Major_Pattern.search(removeRoot_label)
            
            if removeRoot_label is not None: #major chord with 7th like A:maj7
                
                chord_eval = transfer_chord_vocabulary(removeRoot_label.group(1))
                
                #屬和弦與延伸和弦:C9->C:9
                if removeRoot_label.group(2) is not "" and removeRoot_label.group(2) =='7':
                    majmin7_label = chord_eval +":"+ removeRoot_label.group(2)
                else:
                    majmin7_label = chord_eval +":maj"
            else: #pure major chord like: C,D,E
                chord_eval = transfer_chord_vocabulary(PureMajor_label)
                majmin7_label = chord_eval +":maj"

    return majmin7_label

def transfer_chord_vocabulary(chord):
    val = chord

    if chord == 'B#' or chord=='#B':
        val = 'C'
    elif chord == 'A#' or chord=='#A' or chord=='bB':
        val = 'Bb'
    elif chord == 'C#' or chord=='#C' or chord=='bD':
        val = 'Db'
    elif chord == 'D#' or chord=='#D' or chord=='bE':
        val = 'Eb'
    elif chord == 'E#' or chord=='#E' :
        val = 'F'
    elif chord == 'F#' or chord=='#F' or chord=='bG':
        val = 'Gb'
    elif chord == 'G#' or chord=='#G' or chord=='bA':
        val = 'Ab'
    elif chord == 'Cb' or chord=='bC' :
        val = 'B'
    elif chord == 'Fb' or chord=='bF':
        val = 'E'

    return val

def key_estimate(input_str):

    #count each key
    namethatkey = len(keys)*[0]
    #print namethatkey,iterator
    iterator = 0

    input_array = {"chords":input_str}
    data  = json.dumps(input_array)
    chord_sequence = json.loads(data)
    
    iterator = 0
    for each_key in keys:
        for key_element in each_key:
            for each_chords in chord_sequence["chords"]:
                if each_chords==key_element:
                    namethatkey[iterator] +=1
        iterator = iterator+1
    #print(namethatkey)
    namethatkey_indexed_list = zip(namethatkey, range(len(namethatkey)))
    #print namethatkey_indexed_list
    #min_value, min_index = min(namethatkey_indexed_list)
    max_value, max_index = max(namethatkey_indexed_list)

    return {"estimate_key":keyName[max_index],"estimate_key_profile":key_profile[max_index]}

def smooth_key(chord_progression,estimate_key,tokey):
    '''
    This is key smooth function.
    We'll transpose estimate_progression from estimate_key to tokey.
    It needs estimate_key_profile be input
    '''
    
    
    estimate_progression=chord_progression[:]
    
    estimate_key=key_profile[keyName.index(estimate_key)]
    tokey=key_profile[keyName.index(tokey)]
    for i in range(len(estimate_progression)):
        sp = estimate_progression[i].split(":")
        if sp[0] is not "N":
            if "b" in sp[0]:
                if sp[0] in estimate_key:
                    estimate_progression[i] = tokey[estimate_key.index(sp[0])]+":"+sp[1]
                #else:
                    # Warning: this is really our limitation
                    # We try to avoid this problem
                    #justKey = sp[0].strip("b")
                    #estimate_progression[i] = tokey[estimate_key.index(justKey)]+"b:"+sp[1]
            else:
                #print sp[0]
                try:
                    estimate_progression[i] = tokey[estimate_key.index(sp[0])]+":"+sp[1]
                except:#This chord is not in the Tokey_list(regard as outlier)
                    estimate_progression[i] = "N"
        else:
            estimate_progression[i] = "N"

    return estimate_progression


def song1key_to_song2key(song1_chord_progression,song2_chord_progression):
    '''
    This is key smooth function.
    We'll transpose estimate_progression from estimate_key to tokey.
    It needs estimate_key_profile be input
    '''
    
    
    estimate_progression=song1_chord_progression[:]
    
    estimate_key1=key_estimate(song1_chord_progression)['estimate_key']
    estimate_key2=key_estimate(song2_chord_progression)['estimate_key']
    
    
    
    estimate_key=key_profile[keyName.index(estimate_key1)]
    tokey=key_profile[keyName.index(estimate_key2)]
    for i in range(len(estimate_progression)):
        sp = estimate_progression[i].split(":")
        if sp[0] is not "N":
            if "b" in sp[0]:
                if sp[0] in estimate_key:
                    estimate_progression[i] = tokey[estimate_key.index(sp[0])]+":"+sp[1]
                #else:
                    # Warning: this is really our limitation
                    # We try to avoid this problem
                    #justKey = sp[0].strip("b")
                    #estimate_progression[i] = tokey[estimate_key.index(justKey)]+"b:"+sp[1]
            else:
                #print sp[0]
                try:
                    estimate_progression[i] = tokey[estimate_key.index(sp[0])]+":"+sp[1]
                except:#This chord is not in the Tokey_list(regard as outlier)
                    estimate_progression[i] = "N"
        else:
            estimate_progression[i] = "N"

    return estimate_progression




def chord_encoding(chord):
    sp=chord.split(':') #Ex:C:maj7
    chord=sp[0]
    chord_attr=sp[1]
    encoding_vector=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    

def main():
    
    
   '''
    input_str = ['E:min', 'C:maj', 'G:maj', 'D:maj', 'E:min', 'C:maj', 'G:maj', 'E:min', 'C:maj', 'G:maj', 'E:min',
 'C:maj', 'G:maj', 'E:min', 'C:maj', 'G:maj', 'E:min', 'D:maj', 'G:maj', 'E:min', 'C:maj', 'G:maj',
 'E:min', 'C:maj', 'G:maj', 'E:min', 'C:maj', 'G:maj', 'E:min', 'D:maj', 'G:maj', 'D:maj', 'G:maj',
 'E:min', 'E:min', 'C:maj', 'G:maj', 'E:min', 'C:maj', 'D:maj', 'E:min', 'C:maj', 'G:maj', 'E:min',
 'C:maj', 'E:min', 'D:maj', 'G:maj', 'D:maj', 'G:maj']
 
   
    print key_estimate(input_str)
    print smooth_key(input_str,G,A)
    '''

if __name__ == "__main__":
    main()
