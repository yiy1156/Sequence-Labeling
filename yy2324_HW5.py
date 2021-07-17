def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def is_first_word(input_file_list, current_line_index):
    if current_line_index == 0:
        return False
    else:
        line = input_file_list[current_line_index - 1].strip('\n')
        if line == "":
            return True
    return False


def is_second_word(input_file_list, current_line_index):
    if current_line_index == 0 or current_line_index == 1:
        return False
    else:
        line = input_file_list[current_line_index - 2].strip('\n')
        if line == "":
            return True
    return False


def is_last_word(input_file_list, current_line_index):
    if current_line_index >= len(input_file_list) - 1:
        return False
    line = input_file_list[current_line_index+1].strip('\n')
    if line == "":
        return True
    return False


def is_second_to_last_word(input_file_list, current_line_index):
    if current_line_index >= len(input_file_list) - 2:
        return False
    line = input_file_list[current_line_index+2].strip('\n')
    if line == "":
        return True
    return False


def get_next_word(input_file_list, current_line_index):
    if is_last_word(input_file_list, current_line_index):
        return "END"
    else:
        return input_file_list[current_line_index+1].strip('\n').split('\t')[0]


def get_next_pos_tag(input_file_list, current_line_index):
    if is_last_word(input_file_list, current_line_index):
        return "END"
    else:
        return input_file_list[current_line_index+1].strip('\n').split('\t')[1]


def get_previous_word(input_file_list, current_line_index):
    if is_first_word(input_file_list, current_line_index):
        return "BEGIN"
    else:
        return input_file_list[current_line_index-1].strip('\n').split('\t')[0]


def get_previous_pos_tag(input_file_list, current_line_index):
    if is_first_word(input_file_list, current_line_index):
        return "END"
    else:
        return input_file_list[current_line_index-1].strip('\n').split('\t')[1]


def is_capital(input_file_list, current_line_index):
    word = input_file_list[current_line_index].strip('\n').split('\t')[0]
    if word[0].isupper(): 
        return "TRUE"
    else:
        return "FALSE"


def is_previous_word_capital(input_file_list, current_line_index):
    if is_first_word(input_file_list, current_line_index):
        return "False"
    else:
        word = input_file_list[current_line_index-1].strip('\n').split('\t')[0]
        if word[0].isupper(): 
            return "TRUE"
        else:
            return "FALSE"


def is_next_word_capital(input_file_list, current_line_index):
    if is_last_word(input_file_list, current_line_index):
        return "False"
    else:
        word = input_file_list[current_line_index+1].strip('\n').split('\t')[0]
        if word[0].isupper():
            return "TRUE"
        else:
            return "FALSE"


def build_training_output_line(current_word, current_pos, current_bio, next_word, next_pos, previous_word,
                                   previous_pos, current_cap, previous_cap, next_cap):
    current_word = current_word
    current_pos = 'POS=' + current_pos
    current_bio = current_bio 
    next_word = 'next_word=' + next_word
    next_pos = 'next_POS=' + next_pos
    previous_word = 'previous_word=' + previous_word
    previous_pos = 'previous_POS=' + previous_pos
    current_cap = 'is_current_word_capital=' + current_cap
    previous_cap = 'is_previous_word_capital=' + previous_cap
    next_cap = 'is_next_word_capital=' + next_cap

    param_list_for_training_file = [current_word, current_pos, next_word, next_pos, previous_word, previous_pos,
                                    current_cap,
                                    previous_cap, next_cap,
                                    current_bio]  
    training_output_line = '\t'.join(param_list_for_training_file)

    return training_output_line


def build_test_output_line(current_word, current_pos, next_word, next_pos, previous_word,
                               previous_pos, previous_bio, current_cap, previous_cap, next_cap):
    current_word = current_word
    current_pos = 'POS=' + current_pos
    next_word = 'next_word=' + next_word
    next_pos = 'next_POS=' + next_pos
    previous_word = 'previous_word=' + previous_word
    previous_pos = 'previous_POS=' + previous_pos
    previous_bio = 'Previous_BIO=' + previous_bio
    current_cap = 'is_current_word_capital=' + current_cap
    previous_cap = 'is_previous_word_capital=' + previous_cap
    next_cap = 'is_next_word_capital=' + next_cap

    param_list_for_test_file = [current_word, current_pos, next_word, next_pos, previous_word, previous_pos,
                                current_cap,
                                previous_cap, next_cap,
                                previous_bio]  
    test_output_line = '\t'.join(param_list_for_test_file)

    return test_output_line


def generate_training_file(input_file):
    with open(input_file, 'r') as input_file:
        with open('training.feature', 'w') as training_output_file:
            data = input_file.readlines()
            line_written = 0
            for index, line in enumerate(data):
                line = line.rstrip('\n')
                if line != '':
                    current_word, current_pos_tag, current_bio_tag = line.split('\t')
                    next_word = get_next_word(data, index)
                    next_pos_tag = get_next_pos_tag(data, index)
                    previous_word = get_previous_word(data, index)
                    previous_pos_tag = get_previous_pos_tag(data, index)
                    current_word_capital = is_capital(data, index)
                    previous_word_capital = is_previous_word_capital(data, index)
                    next_word_capital = is_next_word_capital(data, index)

                    training_line = build_training_output_line(current_word, current_pos_tag,
                                                                       current_bio_tag, next_word, next_pos_tag,
                                                                       previous_word, previous_pos_tag,
                                                                       current_word_capital,
                                                                       previous_word_capital, next_word_capital)
                    training_output_file.write(training_line + '\n')
                else:
                    training_output_file.write('\n')

                line_written += 1
                print(str(line_written), " lines written for training file.")


def generate_test_file(input_file):
    with open(input_file, 'r') as input_file:
        with open('test.feature', 'w') as test_output_file:
            data = input_file.readlines()
            line_written = 0
            for index, line in enumerate(data):
                line = line.strip('\n')
                if line != '':
                    current_word, current_pos_tag = line.split('\t')
                    next_word = get_next_word(data, index)
                    next_pos_tag = get_next_pos_tag(data, index)
                    previous_word = get_previous_word(data, index)
                    previous_pos_tag = get_previous_pos_tag(data, index)
                    previous_bio_tag = "@@"
                    current_word_capital = is_capital(data, index)
                    previous_word_capital = is_previous_word_capital(data, index)
                    next_word_capital = is_next_word_capital(data, index)

                    test_line = build_test_output_line(current_word, current_pos_tag,
                                                                       next_word, next_pos_tag,
                                                                       previous_word, previous_pos_tag,
                                                                       previous_bio_tag, current_word_capital,
                                                                       previous_word_capital, next_word_capital)
                    test_output_file.write(test_line + '\n')
                else:
                    test_output_file.write('\n')

                line_written += 1
                print(str(line_written), " lines written for test file.")

#generate training 
#generate_training_file('WSJ_02-21.pos-chunk')
generate_test_file('WSJ_23.pos')
