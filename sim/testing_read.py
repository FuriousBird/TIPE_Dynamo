import numpy, matplotlib.pyplot as plt

with open('TESTING.ans', 'r', encoding="utf-8") as f:
    lines = f.readlines()

#split the lines into blocks with: [string: the name of the block]\n <block splanning multiple lines>

blocks = []
for line in lines:
    line = line.rstrip()
    if line.startswith('['):
        blocks.append([line])
    else:
        blocks[-1].append(line)

#get the Solution block
solution = [block for block in blocks if block[0].startswith('[Solution]')][0]
#remove the first and 2nd lines
count = int(solution[1].strip())
solution = solution[2:]
#then parse the lines into a numpy array of floats, lenght coulnt, with 3 columns
solution = numpy.array([output for line in solution if (output :=list(map(float, line.split()[:3]))) and len(output) == 3])

plt.figure()
plt.scatter(solution[:, 0], solution[:, 1], c=solution[:, 2], s=1)
plt.colorbar()
plt.title('Solution')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
