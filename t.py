

# Test ALU

acc = 0b0000
tmp = 0b0101
print("acc :{:04b}".format(acc))

acc = (acc ^ 0b1111) & 0xF
print("acc':{:04b}".format(acc))

#tmp = (tmp ^ 0b1010) & 0xF
#sum = (acc + tmp) & 0xF
#sum = (sum ^ 0b1010) & 0xF

#print(sum)
