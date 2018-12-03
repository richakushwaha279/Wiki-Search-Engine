import os, re

def merge(file1, file2, merged_file):
	with open(file1) as f1, open(file2) as f2, open(merged_file, 'w') as f3:
		Entry1 = f1.next()
		term1, PL1 = Entry1.split()
		Entry2 = f2.next()
		term2, PL2 = Entry2.split()
		while(True):
			if(term1 < term2):
				f3.write(Entry1)
				try:
					Entry1 = f1.next()
					term1, PL1 = Entry1.split()
				except:
					while(True):
						try:
							f3.write(Entry2)
							Entry2 = f2.next()
						except:
							break
					break
			elif(term1 > term2):
				f3.write(Entry2)
				try:
					Entry2 = f2.next()
					term2, PL2 = Entry2.split()
				except:
					while (True):
						try:
							f3.write(Entry1)
							Entry1 = f1.next()
						except:
							break
					break
			else:
				#if both same terms then just append the PLs
				Entry = term1 + ' ' + PL1 + '|' + PL2 + '\n'
				f3.write(Entry)
				try:
					Entry1 = f1.next()
					term1, PL1 = Entry1.split()
				except:
					while(True):
						try:
							Entry2 = f2.next()
							f3.write(Entry2)
						except:
							break
					break
				try:
					Entry2 = f2.next()
					term2, PL2 = Entry2.split()
				except:
					while (True):
						try:
							Entry1 = f1.next()
							f3.write(Entry1)
						except:
							break
					break

regex = re.compile('^output\W*')
start = 0
end = 0
#FIND END
l = os.listdir('.')
for f in l:
	if regex.findall(f):
		end+=1
print 'Total out files: ', end
cd = open('total_out_files','w')
cd.write(str(end))
cd.close()
while(start < end -1):
	merge('output' + str(start),'output' + str(start+1),'output' + str(end))
	os.remove('output' + str(start))
	os.remove('output' + str(start+1))
	print 'file created after merge: ', end
	end +=1
	start +=2