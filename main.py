import sys
import os
import re

def get_alphbet(collection):
    alphabet = []
    for symbol in collection:
        if symbol != "^\n":
            alphabet.append(symbol.rstrip('\n'))

    return alphabet
# ~def

def make_original_dictionarie(handle):
    originalDict = {}
    for line in handle:
        if line.find(".mv") == -1:
            continue

        words = line.split(" ")
        if words[2].isnumeric():
            if( words[1] != "E" ):
                originalDict.update({ words[1]: get_alphbet(words[3:])})
        else:
            break

    return originalDict

# def form_clear_balm_dict(lenght):
#     """Form dict: E-: []"""
#     dict = {}
#     counter = 0
#     while counter != lenght:
#         dict.update({"E" + str(counter): []})
#         counter += 1
#
#     return dict
# ~def

def make_balm_dictionarie(handle, canals_num):
    """Forms dict: E-: [alphabet]"""
    #dict = form_clear_balm_dict(canals_num)
    dict = {}
    transitions_started = False

    for line in handle:
        # Find last string after which there will be transitions
        if line.find("CS -> NS") != -1:
            transitions_started = True
            continue

        # Skip string after transitions
        if(transitions_started != True):
            continue

        # Check, that ther are more transitions
        if (line == ' \n') or (line == '.end'):
            break

        symbols = line.split(" ")

        E = symbols[canals_num]
        aplh_before_E = symbols[0:canals_num]
        true_symbol = ""
        for symbol in aplh_before_E:
            if symbol != "-":
                true_symbol = symbol

        if dict.get(E) != None:
            if dict[E].count(true_symbol) == 0:
                dict[E].append(true_symbol)
        else:
            dict.update({E:[true_symbol]})

    return dict
    # ~for
# ~def

def make_originalBalm_dict(original_dict, balm_dict):
    for key, value in original_dict.items():
        value.sort()

    for key, value in balm_dict.items():
        value.sort()

    original_to_balm_dict = {}
    for orig_key in original_dict:
        for balm_key in balm_dict:
            if original_dict[orig_key] == balm_dict[balm_key]:
                original_to_balm_dict.update({orig_key: balm_key})

    return original_to_balm_dict
# ~def

def get_extendable_channels(dict1, dict2):
    extandable_channels = []
    if len(dict1) > len(dict2):
        for channel in dict1:
            if dict2.get(channel) == None:
                extandable_channels.append(channel)
    else:
        for channel in dict2:
            if dict1.get(channel) == None:
                extandable_channels.append(channel)

    return extandable_channels
# ~def

def process_expansion_restriction(line, dict):
    words = line.split(" ")
    originalChannels = words[3].split(",")
    balmChannels = []
    for channel in originalChannels:
        balmChannels.append(dict[channel])
    words[3] = ','.join(balmChannels)
    return ' '.join(words)


def process_write_para(line, dict):
    words = line.split(" ")
    originalChannels = words[4].split("|")
    balmChannels = []
    for channel in originalChannels:
        balmChannels.append(dict[channel])
    words[4] = '|'.join(balmChannels)
    return ' '.join(words)


def get_original_order(dict):
    ordered = []
    for key in dict:
        ordered.append(key)
    return ordered


# ~def

def process_pre_product_support(line, ordered_channels):
    words = line.split(" ")
    channels = words[3].split(",")
    E = ""
    channelsWithoutE = []
    for channel in channels:
        if (re.fullmatch("E\(\d\)", channel) == None):
            channelsWithoutE.append(channel)
        else:
            E = channel

    if (len(channelsWithoutE) == len(ordered_channels)):
        words[3] = ','.join(ordered_channels)

    words[3] = words[3] + "," + E
    return ' '.join(words)
# ~def

def make_new_script(old_script, dict, ordered_channels):
    lines = [line.rstrip('\n') for line in old_script]
    # first expansion
    if lines[6] != '':
        lines[6] = process_expansion_restriction(lines[6], dict)
    # second expansion
    if lines[7] != '':
        lines[7] = process_expansion_restriction(lines[7], dict)
    lines[8] = process_pre_product_support(lines[8], ordered_channels)
    # Change original channels to balm channels in restriction
    lines[10] = process_expansion_restriction(lines[10], dict)
    lines[12] = process_write_para(lines[12], dict)
    f = open("edited_script.sh", 'tw', encoding='utf-8')

    lineNum = 0
    for line in lines:
        if (line != '') & (lineNum > 5):
            f.write(line + '\n')
            f.write("sleep 1" + '\n')
        lineNum += 1
# ~def




def main():
    print(len(sys.argv))
    #if len(sys.argv) != 6:
         #print("!!! Need 5 files: 1.aut poly1.aut 2.aut poly2.aut script.sh")
         #return

    #handle_1 = open(sys.argv[1]) #open("polyMach1.aut", 'r')
    #handle_poly_1 = open(sys.argv[2]) #open("syncMach.aut", 'r')
    #handle_2 = open(sys.argv[3]) #open("polyWait1.aut", 'r')
    #handle_poly_2 = open(sys.argv[4]) #open("syncWait.aut", 'r')

    handle_1 = open("test.aut", 'r')
    handle_poly_1 = open("syncpolytest.aut", 'r')
    handle_2 = open("test2.aut", 'r')
    handle_poly_2 = open("syncpolytest2.aut", 'r')

    original_1 = make_original_dictionarie(handle_1)
    print("Original_1: ", original_1)
    ordered_channels_1 = get_original_order(original_1)
    print("Ordered_channels_1: ", ordered_channels_1)
    original_2 = make_original_dictionarie(handle_2)
    print("Original_2: ", original_2)
    ordered_channels_2 = get_original_order(original_2)
    print("Ordered_channels_2: ", ordered_channels_2)
    balm_1 = make_balm_dictionarie(handle_poly_1, len(original_1))
    print("Balm_1: ", balm_1)
    balm_2 = make_balm_dictionarie(handle_poly_2, len(original_2))
    print("Balm_2: ", balm_2)

    original1 = make_originalBalm_dict(original_1, balm_1)
    print("Original1: ", original1)
    original2 = make_originalBalm_dict(original_2, balm_2);
    print("Original2: ", original2)

    original = original1
    original.update(original2)
    print( "Original: ", original)

    extandable_channels = get_extendable_channels(balm_1, balm_2)
    print("Extendable: ", extandable_channels)

    script = open("script-2-side.sh", "r") #open(sys.argv[5])#
    ordered_channels = []
    if( len(ordered_channels_1) > len(ordered_channels_2)):
        ordered_channels = ordered_channels_1
    else:
        ordered_channels = ordered_channels_2
    make_new_script(script, original, ordered_channels)

if __name__ == "__main__":
    main()

