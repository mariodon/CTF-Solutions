def write_flag(offset, char):
    flag.seek(offset)
    flag.write(chr(char).encode())

flag = open('flag.txt', 'wb')

src = open('seek.c', 'r')
for l in src:
    if l.startswith('fseek(fp,'):
        print(l)
        print(l.split(','))
        offset = int(l.split(',')[1])
        print(offset)
        c = int(l.split('!=')[1].split(')')[0])
        print(c)
        write_flag(offset, c)

flag.close()
