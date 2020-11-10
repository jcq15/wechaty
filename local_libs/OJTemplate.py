def standard_answer(a):
    max_element = -1e20
    current = 0

    for i in range(len(a)):
        if a[i] >= max_element:
            current = i
            max_element = a[i]

    return current


test_inputs = [([1, 2, 5, 6, 3, 4, 7, 8, 99, 99, 1, 2, 7], ),
               ([7, 9, 88, 2, -100, -100, 1000, 1000, 34, 53, 342, 342, 2, -10000], ),
               ([1, 5, 5, 6, -100000, -100000, 1000000, 1000000, 983, 2342, 1000000], ),
               ([999999999, 999999999], ),
               ([23], )]
