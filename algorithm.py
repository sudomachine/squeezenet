def rearrange(sequence, new_positions):
    '''
    get
    changeable sequence of some elements;
    list of new positions of elements

    return rearranged sequence of elements
    '''

    if (len(sequence) != len(new_positions)):
        raise RuntimeError("Is not equal lengths")
    
    last_index = None

    while (len(new_positions) != 0):

        print(sequence)
        
        # take last element of new_positions list - new position
        # take his position - old position
        # take element of new position
        # take element of old position
        # set element from old pos to the new position
        # delete new position from list 
        # repeat

        if last_index == None:
            # take last index of new_positions list
            last_index = len(new_positions) - 1
            begin = last_index

            # take his position - old position
            old_pos = last_index
            # take element of old position
            old_element = sequence[old_pos]

        # take last element of new_positions list - new position
        # try:
        new_pos = new_positions[last_index]
        # except IndexError:
            # new_pos = new_positions[-1]

        if new_pos == old_pos:
            last_index = None
            new_positions.pop()
            continue

        # take element of new position
        new_element = sequence[new_pos]

        # set element from old pos to the new position
        sequence[new_pos] = old_element

        # delete new position from new_positions list 
        new_positions.pop(last_index)
        # new_positions = new_positions[:last_index] + new_positions[last_index+1:]

        if begin == new_pos:
            last_index = None
            continue

        last_index = new_pos
        old_element = new_element
        old_pos = last_index

    return sequence
