# decode the encoded message

import numpy as np
import setup


def viterbi(p: np.ndarray) -> np.ndarray:
    # print(setup.frame)
    met = np.array((0, 0, 0, 0))  # metric array init
    temp = np.array((0, 0, 0, 0))  # will store metrics from last step
    path = np.zeros((setup.frame + 2, 4), dtype=np.uint8)
    # store observations
    symbols = np.zeros((setup.frame + 2, 4), dtype=np.uint8)
    message = np.zeros((setup.frame + 2,), dtype=np.uint8)  # decoded message
    # decoded message, tail cut
    message_no_tail = np.zeros((setup.frame,), dtype=np.uint8)

    # iterate through the entire argument array
    for i in range(setup.frame + 2):
        # calculate the min of every possible path pair
        min1 = min([p[i][0], p[i][4]])
        min2 = min([p[i][3], p[i][7]])
        min3 = min([p[i][1], p[i][5]])
        min4 = min([p[i][2], p[i][6]])

        # based on ^ assign symbols to paths
        if min1 == p[i][0]:
            symbol1 = 0
        else:
            symbol1 = 4
        if min2 == p[i][3]:
            symbol2 = 3
        else:
            symbol2 = 7
        if min3 == p[i][1]:
            symbol3 = 1
        else:
            symbol3 = 5
        if min4 == p[i][2]:
            symbol4 = 2
        else:
            symbol4 = 6

        # transfer metrics from last step to temp array
        # to not use new metrics to calculate other metrics
        for j in range(4):
            temp[j] = met[j]

        # from the third step onward
        # calculate the smallest value path to every node
        if i > 1:
            if (temp[0] + min1 < temp[1] + min2):
                met[0] = temp[0] + min1
                path[i][0] = 0
                symbols[i][0] = symbol1
            else:
                met[0] = temp[1] + min2
                path[i][0] = 1
                symbols[i][0] = symbol2
            if (temp[2] + min3 < temp[3] + min4):
                met[1] = temp[2] + min3
                path[i][1] = 2
                symbols[i][1] = symbol3
            else:
                met[1] = temp[3] + min4
                path[i][1] = 3
                symbols[i][1] = symbol4
            if (temp[0] + min2 < temp[1] + min1):
                met[2] = temp[0] + min2
                path[i][2] = 0
                symbols[i][2] = symbol2
            else:
                met[2] = temp[1] + min1
                path[i][2] = 1
                symbols[i][2] = symbol1
            if (temp[2] + min4 < temp[3] + min3):
                met[3] = temp[2] + min4
                path[i][3] = 2
                symbols[i][3] = symbol4
            else:
                met[3] = temp[3] + min3
                path[i][3] = 3
                symbols[i][3] = symbol3

        # first step, always the same
        elif i == 0:
            met[0] = min1
            met[2] = min2
            symbols[i][0] = symbol1
            symbols[i][2] = symbol2
            path[i][0] = 0
            path[i][2] = 0

        # second step, always the same
        elif i == 1:
            met[0] = temp[0] + min1
            met[2] = temp[0] + min2
            met[1] = temp[2] + min3
            met[3] = temp[2] + min4
            symbols[i][0] = symbol1
            symbols[i][1] = symbol3
            symbols[i][2] = symbol2
            symbols[i][3] = symbol4
            path[i][0] = 0
            path[i][1] = 2
            path[i][2] = 0
            path[i][3] = 2

    # artifact after checking if observations
    # are correctly guessed
    # pointer = 0
    # for i in range(setup.frame + 2, -1, -1):
    #     message[i-1] = symbols[i-1][pointer]
    #     pointer = path[i-1][pointer]

    # based on path and observations deduce correct input words
    pointer = 0
    for i in range(setup.frame + 2, -1, -1):
        if path[i-1][pointer] == 0:
            if symbols[i-1][pointer] == 0:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 3:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 4:
                message[i-1] = 2
            elif symbols[i-1][pointer] == 7:
                message[i-1] = 3
            else:
                print("error")

        if path[i-1][pointer] == 1:
            if symbols[i-1][pointer] == 0:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 3:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 4:
                message[i-1] = 3
            elif symbols[i-1][pointer] == 7:
                message[i-1] = 2
            else:
                print("error")

        if path[i-1][pointer] == 2:
            if symbols[i-1][pointer] == 1:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 2:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 5:
                message[i-1] = 2
            elif symbols[i-1][pointer] == 6:
                message[i-1] = 3
            else:
                print("error")

        if path[i-1][pointer] == 3:
            if symbols[i-1][pointer] == 1:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 2:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 5:
                message[i-1] = 3
            elif symbols[i-1][pointer] == 6:
                message[i-1] = 2
            else:
                print("error")
        pointer = path[i-1][pointer]

        # cut the tail
        for i in range(setup.frame):
            message_no_tail[i] = message[i]

    return message_no_tail

# the same thing as above but with paths
# corrected for graycode


def viterbi_gray(p: np.ndarray) -> np.ndarray:
    met = np.array((0, 0, 0, 0))
    temp = np.array((0, 0, 0, 0))
    path = np.zeros((setup.frame + 2, 4), dtype=np.uint8)
    symbols = np.zeros((setup.frame + 2, 4), dtype=np.uint8)
    message = np.zeros((setup.frame + 2,), dtype=np.uint8)
    # decoded message, tail cut
    message_no_tail = np.zeros((setup.frame,), dtype=np.uint8)

    for i in range(setup.frame + 2):
        min1 = min([p[i][0], p[i][7]])
        min2 = min([p[i][2], p[i][5]])
        min3 = min([p[i][1], p[i][6]])
        min4 = min([p[i][3], p[i][4]])

        if min1 == p[i][0]:
            symbol1 = 0
        else:
            symbol1 = 7
        if min2 == p[i][2]:
            symbol2 = 2
        else:
            symbol2 = 5
        if min3 == p[i][1]:
            symbol3 = 1
        else:
            symbol3 = 6
        if min4 == p[i][3]:
            symbol4 = 3
        else:
            symbol4 = 4

        for j in range(4):
            temp[j] = met[j]

        if i > 1:
            if (temp[0] + min1 < temp[1] + min2):
                met[0] = temp[0] + min1
                path[i][0] = 0
                symbols[i][0] = symbol1
            else:
                met[0] = temp[1] + min2
                path[i][0] = 1
                symbols[i][0] = symbol2
            if (temp[2] + min3 < temp[3] + min4):
                met[1] = temp[2] + min3
                path[i][1] = 2
                symbols[i][1] = symbol3
            else:
                met[1] = temp[3] + min4
                path[i][1] = 3
                symbols[i][1] = symbol4
            if (temp[0] + min2 < temp[1] + min1):
                met[2] = temp[0] + min2
                path[i][2] = 0
                symbols[i][2] = symbol2
            else:
                met[2] = temp[1] + min1
                path[i][2] = 1
                symbols[i][2] = symbol1
            if (temp[2] + min4 < temp[3] + min3):
                met[3] = temp[2] + min4
                path[i][3] = 2
                symbols[i][3] = symbol4
            else:
                met[3] = temp[3] + min3
                path[i][3] = 3
                symbols[i][3] = symbol3

        elif i == 0:
            met[0] = min1
            met[2] = min2
            symbols[i][0] = symbol1
            symbols[i][2] = symbol2
            path[i][0] = 0
            path[i][2] = 0
        elif i == 1:
            met[0] = temp[0] + min1
            met[2] = temp[0] + min2
            met[1] = temp[2] + min3
            met[3] = temp[2] + min4
            symbols[i][0] = symbol1
            symbols[i][1] = symbol3
            symbols[i][2] = symbol2
            symbols[i][3] = symbol4
            path[i][0] = 0
            path[i][1] = 2
            path[i][2] = 0
            path[i][3] = 2

    pointer = 0
    for i in range(setup.frame + 2, -1, -1):
        if path[i-1][pointer] == 0:
            if symbols[i-1][pointer] == 0:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 2:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 5:
                message[i-1] = 3
            elif symbols[i-1][pointer] == 7:
                message[i-1] = 2
            else:
                print("error")

        if path[i-1][pointer] == 1:
            if symbols[i-1][pointer] == 0:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 2:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 5:
                message[i-1] = 2
            elif symbols[i-1][pointer] == 7:
                message[i-1] = 3
            else:
                print("error")

        if path[i-1][pointer] == 2:
            if symbols[i-1][pointer] == 1:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 3:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 4:
                message[i-1] = 3
            elif symbols[i-1][pointer] == 6:
                message[i-1] = 2
            else:
                print("error")

        if path[i-1][pointer] == 3:
            if symbols[i-1][pointer] == 1:
                message[i-1] = 1
            elif symbols[i-1][pointer] == 3:
                message[i-1] = 0
            elif symbols[i-1][pointer] == 4:
                message[i-1] = 2
            elif symbols[i-1][pointer] == 6:
                message[i-1] = 3
            else:
                print("error")
        pointer = path[i-1][pointer]

        for i in range(setup.frame):
            message_no_tail[i] = message[i]

    return message_no_tail
