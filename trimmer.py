from PIL import Image

def make_arr(data, dims):
    width, height = dims
    if width * height > len(data):
        message = f"width * height must be <= the length of data ({width} * {height} = {width*height} > {len(data)})"
        raise(Exception(message))

    out = []
    for y in range(height):
        row = data[(y*height):(y*height) + width]
        out.append(row)

    return out


def row_is(row, value):
    for point in row:
        if point[:len(value)] != value:
            print(f'returning false because: {point[:len(value)]} != {value}')
            return False
        else:
            print(f'passing because: {point[:len(value)]} == {value}')
    return True


def col_is(arr, col_ind, value):
    for row in arr:
        if row[col_ind][:len(value)] != value:
            return False
    return True


def find_edges(arr, value=(255, 255, 255)):
    '''
    Iterates through arr from all 4 directions and then finds
    edge where first pixel doesn't have the given.
    Returns the four edges that were found.
    '''
    top = 0
    bottom = len(arr)
    left = 0
    right = len(arr[0])

    # top
    for i in range(len(arr)):
        row = arr[i]
        if not row_is(row, value):
            top = i
            break

    # bottom
    for i in range(len(arr)):
        ind = len(arr) - 1 - i
        row = arr[ind]
        if not row_is(row, value):
            bottom = ind
            break

    # left
    for i in range(len(arr[0])):
        if not col_is(arr, i, value):
            left = i
            break

    # right
    for i in range(len(arr[0])):
        ind = len(arr[0]) - 1 - i
        if not col_is(arr, ind, value):
            right = ind
            break

    return (left, right, top, bottom)


def clean_to_size(arr, left, right, top, bottom):
    '''
    Trim the arr by the given margins.
    TODO: This is really slow and needs to be sped up
    '''
    newdata = []
    for ind, row in enumerate(arr):
        print(f'{ind} / {len(arr)} = {ind / len(arr)}%')
        if ind >= top and ind <= bottom:
            newdata = newdata + row[left:right+1]

    return newdata


def full_clean(inputimage, value=(255, 255, 255)):
    '''
    Finds the edge of all non-background items
    Then crops out the unnecessary background
    returns the cropped image
    '''
    data = list(inputimage.getdata())
    arr = make_arr(data, inputimage.size)
    
    print('Finding edges...')
    left, right, top, bottom = find_edges(arr, value=value)

    # crops data into one-dimensional array for dumping to output
    print('Croping data to new size...')
    newdata = clean_to_size(arr, left, right, top, bottom)

    # Make new image
    print('Making new image...')
    width, height = (right - left+1), (bottom - top+1)
    newim = Image.new("RGB", (width, height))
    newim.putdata(newdata)

    return newim

if __name__ == "__main__":
    im = Image.open("source_images/one.png")

    newim = full_clean(im)
    print('Showing the new image...')
    newim.show()