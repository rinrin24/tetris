def rotate_right(current_shape):
    new_shape = [
        [' ', ' ', ' '],
        [' ', 'x', ' '],
        [' ', '', ' ']
    ]
    for i in range(3):
        if current_shape[0][i] == 'o':
            new_shape[i][2] = 'o'
    if current_shape[1][0] == 'o':
        new_shape[0][1] = 'o'
    if current_shape[1][2] == 'o':
        new_shape[2][1] = 'o'
    for i in range(3):
        if current_shape[2][i] == 'o':
            new_shape[i][0] = 'o'
    return new_shape

def rotate_left(current_shape):
    new_shape = [
        [' ', ' ', ' '],
        [' ', 'x', ' '],
        [' ', ' ', ' ']
    ]
    for i in range(3):
        if current_shape[0][i] == 'o':
            new_shape[2-i][0] = 'o'
    if current_shape[1][0] == 'o':
        new_shape[2][1] = 'o'
    if current_shape[1][2] == 'o':
        new_shape[0][1] = 'o'
    for i in range(3):
        if current_shape[2][i] == 'o':
            new_shape[2-i][2] = 'o'
    return new_shape

def rotate4_right(current_shape) -> None:
    new_shape = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']
    ]
    for i in range(4):
        for j in range(4):
            if current_shape[j][i] == 'o':
                new_shape[i][3-j] = 'o'
    current_shape = new_shape
    return new_shape

def rotate4_left(current_shape) -> None:
    new_shape = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']
    ]
    for i in range(4):
        for j in range(4):
            if current_shape[j][i] == 'o':
                new_shape[3-i][j] = 'o'
    current_shape = new_shape
    return new_shape
        
def print_shape(current_shape):
    for row in current_shape:
        print(row)

shape = [
    [' ', 'o', 'o'],
    ['o', 'x', ' '],
    [' ', ' ', ' ']
]
print_shape(shape)
print_shape(rotate_right(shape))
print_shape(rotate_right(rotate_right(shape)))
print_shape(rotate_right(rotate_right(rotate_right(shape))))
print_shape(rotate_right(rotate_right(rotate_right(rotate_right(shape)))))

print('------')

print_shape(shape)
print_shape(rotate_left(shape))
print_shape(rotate_left(rotate_left(shape)))
print_shape(rotate_left(rotate_left(rotate_left(shape))))
print_shape(rotate_left(rotate_left(rotate_left(rotate_left(shape)))))

shape = [
    [' ', ' ', ' ', ' '],
    ['o', 'o', 'o', 'o'],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ']
]

print_shape(shape)
print_shape(rotate4_right(shape))
print_shape(rotate4_right(rotate4_right(shape)))
print_shape(rotate4_right(rotate4_right(rotate4_right(shape))))
print_shape(rotate4_right(rotate4_right(rotate4_right(rotate4_right(shape)))))

print('----')
print_shape(shape)
print_shape(rotate4_left(shape))
print_shape(rotate4_left(rotate4_left(shape)))
print_shape(rotate4_left(rotate4_left(rotate4_left(shape))))
print_shape(rotate4_left(rotate4_left(rotate4_left(rotate4_left(shape)))))