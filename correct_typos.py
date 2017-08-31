def is_suitable(original, unclear):
    diff = abs(len(original) - len(unclear))
    if diff == 1:
        return contains_omission_or_redund(original, unclear)
    if diff == 0:
        return contains_swap(original, unclear)


def contains_omission_or_redund(original, unclear):
    shorter, longer = sorted([original, unclear], key=len)
    for ind in range(len(shorter)):
        if shorter[ind] != longer[ind]:
            if shorter[: ind] + longer[ind] + shorter[ind:] == longer:
                return True
            return
    if shorter + longer[-1] == longer:
        return True


def contains_swap(original, unclear):
    curr_ind, next_ind = 0, 1
    while next_ind < len(unclear):
        if unclear[: curr_ind] + unclear[next_ind] + unclear[curr_ind] + unclear[next_ind + 1:] == original:
            return True
        curr_ind += 1
        next_ind += 1
