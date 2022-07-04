path='/home/kuangda/workspace/datasets/Day/Campus/ImageSets/'

f= open(path+'test.txt','w')
for num in range(1,168):
    f.write(format(num,'06d'))
    f.write('\n')
f.close()

f= open(path+'trainval.txt','w')
for num in range(1,168):
    f.write(format(num,'06d'))
    f.write('\n')
f.close()

f= open(path+'train.txt','w')
for num in range(1,168):
    f.write(format(num,'06d'))
    f.write('\n')
f.close()

f= open(path+'val.txt','w')
for num in range(1,168):
    f.write(format(num,'06d'))
    f.write('\n')
f.close()
