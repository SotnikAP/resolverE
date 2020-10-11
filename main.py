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

        """Покрывает ситуацию, когда Балм объединяет два перехода по разным символам:
        MAIL ^ ^ err s2 s2
        DATA ^ ^ err s2 s2
        В один перехрд (MAIL,DATA) ^ ^ err s2 s2
        
        Если символ содержит ( в начале и ) в конце - отрезаем скобки и пытаемся разделить на символы - split(',')
        Если символов больше 1 (т.е. это реально объединение, а не название символа), то каждый символ пытаемся добавить в словарь
        Иначе - это имя символа такое и пытаемся добавть его со скобками. Т.е. имя символа '(SYMBOL)'.
        """
        if true_symbol[0] == '(' and true_symbol[-1] == ')':
            united_symbols = true_symbol[1:-1].split(',')
            if len(united_symbols) > 1:
                for symbol in united_symbols:
                    if dict.get(E) != None:
                        if dict[E].count(symbol) == 0:
                            dict[E].append(symbol)
                    else:
                        dict.update({E: [symbol]})
        else:
            if dict.get(E) != None:
                if dict[E].count(true_symbol) == 0:
                    dict[E].append(true_symbol)
            else:
                dict.update({E: [true_symbol]})

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

def get_channels_with_len(channels, channels_with_len):
    channels_len = []
    for channel in channels:
        channels_len.append(channel + "(" + str(channels_with_len[channel]) + ")")

    return channels_len
# ~def

def process_pre_product_support(line, ordered_channels, channels_with_len):
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
        ordered_channels_with_len = get_channels_with_len(ordered_channels, channels_with_len)
        words[3] = ','.join(ordered_channels_with_len)

    words[3] = words[3] + "," + E
    return ' '.join(words)
# ~def

def add_alphabet_size_to_channels_in_support(line, channels_with_len):
    words = line.split(" ")
    channels = words[3].split(",")
    E = channels[-1]
    channels.remove( channels[-1] )
    channels_with_size = get_channels_with_len(channels, channels_with_len)
    words[3] = ",".join(channels_with_size)

    words[3] = words[3] + "," + E

    return ' '.join(words)
# ~def

"""
Получает словарь вида {имя_канала : [алфавит]}
Возвращает словарь вида {имя_канала : мощность_канала}
"""
def get_channel_size(channel_with_alph):
    channel_with_len = {}
    for key, value in channel_with_alph.items():
        channel_with_len.update({key : len(value)})

    return channel_with_len
# ~def

"""Редактирует сырой скрипт
Args: old_script - старый скрипт
      dict - словарь соответствия настоящего имени канала его E- каналу
      ordered_channels - каналы бОльшего автомата в порядке, указаном в файле
      channels_with_len_1/2 - словари каналов и их мощностей
"""
def make_new_script(old_script, dict, ordered_channels, channels_with_len):
    lines = [line.rstrip('\n') for line in old_script]
    # first expansion
    if lines[6] != '':
        lines[6] = process_expansion_restriction(lines[6], dict)
    # second expansion
    if lines[7] != '':
        lines[7] = process_expansion_restriction(lines[7], dict)
    lines[8] = process_pre_product_support(lines[8], ordered_channels, channels_with_len)
    # Change original channels to balm channels in restriction
    lines[11] = process_expansion_restriction(lines[11], dict)
    lines[12] = add_alphabet_size_to_channels_in_support(lines[12], channels_with_len)
    lines[13] = process_write_para(lines[13], dict)
    f = open("edited_script.sh", 'tw', encoding='utf-8')

    lineNum = 0
    for line in lines:
        if (line != '') & (lineNum > 5):
            f.write(line + '\n')
            f.write("sleep 1" + '\n')
        lineNum += 1
# ~def



def make_star(bigger_aut, extandable, original):
    start_state = "start"
    first_state = "first"
    second_state = "second"
    states_number = "3"

    def make_new_states_line(symbols):
        new_line = " ".join(symbols[:3])
        states_line = " " + " ".join([states_number, start_state, first_state, second_state])
        new_line += states_line + "\n"
        return new_line
    # ~def

    file_object = open( "star.aut", "w+" )
    bigger_aut.seek(0)

    for line in bigger_aut:
        if line.find("CS, NS") == -1:
            file_object.write(line)
        else:
            new_line = make_new_states_line( line.split(" ") )
            file_object.write(new_line)
            break;

    next_line_is_init_state = False
    for line in bigger_aut:
        if( not next_line_is_init_state ):
            file_object.write(line)
            if line.find(".reset") != -1:
                next_line_is_init_state = True
        else:
            file_object.write(start_state + "\n")
            break;

    next_line_is_finish_state = False
    for line in bigger_aut:
        if( not next_line_is_finish_state ):
            file_object.write(line)
            if line.find(".default") != -1:
                next_line_is_finish_state = True
        else:
            file_object.write(start_state + " 1" + "\n")
            break;

    for line in bigger_aut:
        file_object.write(line)
        if( line.find("CS -> NS") != -1 ):
            break;

    symbol1 = ""
    symbol2 = ""
    for key in original:
        if extandable.count(original[key]) == 0:
            if symbol2 == "":
                symbol2 = original[key]
            else:
                symbol1 = original[key]
        else:
            continue

    aplhabet_line = "- - - - "
    first_line = aplhabet_line + extandable[0] + " " + start_state + " " + first_state + "\n"
    middle_line_1 = aplhabet_line + symbol2 + " " + first_state + " " + second_state + "\n"
    middle_line_2 = aplhabet_line + symbol1 + " " + second_state + " " + first_state + "\n"
    last_line = aplhabet_line + extandable[1] + " " + first_state + " " + start_state + "\n"
    file_object.write( first_line )
    file_object.write( middle_line_1 )
    file_object.write( middle_line_2 )
    file_object.write( last_line )
    file_object.write(".end")

# ~def


def main():
    print(len(sys.argv))
    #if len(sys.argv) != 6:
         #print("!!! Need 5 files: 1.aut poly1.aut 2.aut poly2.aut script.sh")
         #return

    handle_poly_1 = open(sys.argv[1]) #open("polyMach1.aut", 'r')
    handle_sync_1 = open(sys.argv[2]) #open("syncMach.aut", 'r')
    handle_poly_2 = open(sys.argv[3]) #open("polyWait1.aut", 'r')
    handle_sync_2 = open(sys.argv[4]) #open("syncWait.aut", 'r')

    #handle_poly_1 = open("polyclient_SMTP.aut", 'r')
    #handle_sync_1 = open("syncpolyclient_SMTP.aut", 'r')
    #handle_poly_2 = open("polyserver_SMTP.aut", 'r')
    #handle_sync_2 = open("syncpolyserver_SMTP.aut", 'r')

    original_1 = make_original_dictionarie(handle_poly_1)
    print("Original_1: ", original_1)
    ordered_channels_1 = get_original_order(original_1)
    print("Ordered_channels_1: ", ordered_channels_1)
    original_2 = make_original_dictionarie(handle_poly_2)
    print("Original_2: ", original_2)
    ordered_channels_2 = get_original_order(original_2)
    print("Ordered_channels_2: ", ordered_channels_2)
    balm_1 = make_balm_dictionarie(handle_sync_1, len(original_1))
    print("Balm_1: ", balm_1)
    balm_2 = make_balm_dictionarie(handle_sync_2, len(original_2))
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

    script = open("script.sh", "r") #open(sys.argv[5])#
    ordered_channels = []
    if( len(ordered_channels_1) > len(ordered_channels_2)):
        make_star( handle_sync_1, extandable_channels, original2 )
        ordered_channels = ordered_channels_1
    else:
        make_star( handle_sync_2, extandable_channels, original1 )
        ordered_channels = ordered_channels_2

    channels_with_len_1 = get_channel_size(original_1)
    channels_with_len_2 = get_channel_size(original_2)
    biggest = {}
    if len(channels_with_len_1) > len(channels_with_len_2):
        biggest = channels_with_len_1
    else:
        biggest = channels_with_len_2
    make_new_script(script, original, ordered_channels, biggest)

if __name__ == "__main__":
    main()

