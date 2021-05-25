
def split(string, sep):
    li = string.rstrip("\n").split(sep)
    for elem in li:
        if elem.isnumeric():
            print(elem)

def print_number():
    l=""
    with open('numbers.txt', 'r') as f:
        for line in f:
            l = line
    split(l,',')
 

if __name__ == '__main__':
    print_number()