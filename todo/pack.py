def greater(date_2, date_1):
    if date_1[0] > date_2[0]:
        return True
    elif date_1[0] < date_2[0]:
        return False
    else:
        if date_1[1] > date_2[1]:
            return True
        elif date_1[1] < date_2[1]:
            return False
        else:
            if date_1[2] >= date_2[2]:
                return True
            elif date_1[2] < date_2[2]:
                return False
