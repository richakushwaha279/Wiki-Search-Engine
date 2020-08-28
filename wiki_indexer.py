#!/usr/bin/python
import xml.sax
import sys
import nltk
from nltk.corpus import stopwords
import re
from Stemmer import Stemmer

output = ''
output2 = ''
stemmer = Stemmer("english")
# uselessWords = ['image', 'imagesize', 'alt', 'signature','signature_alt']
finalDictionary = {}
docID = 1
index_file_count_before_merge = 0

class PageHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.id = 0
		self.title = []	
		self.infobox = []
		self.indexStructure = {}
		self.page_content = [] 
		self.stopWords = {}
		words = stopwords.words('english')
		for i in words:
			self.stopWords[i] = 0
		self.externallinks = []
		self.references = [] 
		self.categories = []
		self.CurrentData = ""  #the current tag going on
		# self.pgNO_pgTitle = {}
		self.regex = re.compile(r'[a-zA-Z0-1]+')
		# Regular Expression to remove URLs
		self.regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
		# Regular Expression to remove CSS
		self.regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
		# To remove {{cite **}} or {{vcite **}}
		self.regExp3 = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)
		# To remove [[file:]]
		self.regExp5 = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
		# self.id_pgNo = {}
		# self.pg_no = 0
		self.infoFlag = False
		self.referenceFlag = False
		self.externalFlag = False
		self.flag = False
		# self.pgId_pgTitle = {}
##################################################################################################################################################

	def storeIndexStructure(self, dataList, tag, index):
		# print 'ascha',dataList
		global stemmer, finalDictionary
		dataList3 = dataList
		if tag == "infobox":
			dataList3 = []
			for word in dataList:
				word = word.split('=')
				if len(word) >1:
					# if word[1] in uselessWords:
					# 	continue
					dataList3.append(word[1])
				else:
					dataList3.append(word[0])

		if tag == "references":
			# print 'hosihdfh'
			dataList3 = []
			for word in dataList:
				word = word.split('=')
				if len(word) >1:
					# if word[1] in uselessWords:
					# 	continue
					dataList3.append(word[1])
				else:
					dataList3.append(word[0])
		# print 'hole' , dataList3
		for data in dataList3:
			# print data
			reg = self.regex
			string = reg.findall(data)
			# print string
			dataList2 = [] #filtered words
			for word in string:
				try:
					self.stopWords[word]
				except:
					if len(word) >1:
						dataList2.append(word)
						# print word
			# print dataList2
			for word in dataList2:
				w = stemmer.stemWord(word)
				# print 'herrh',w
				try:
					finalDictionary[w][self.id]
					finalDictionary[w][self.id][index] += 1
				except:
					try:
						finalDictionary[w]
						finalDictionary[w][self.id]=[0,0,0,0,0,0]
						finalDictionary[w][self.id][index] = 1
					except:
						finalDictionary[w] = {}
						finalDictionary[w][self.id]=[0,0,0,0,0,0]
						finalDictionary[w][self.id][index] = 1				
				# # print w
				# try:
				# 	if w in self.stopWords:
				# 		continue
				# 	# print type(w)
				# 	# w = reg.findall(w)
				# 	# print w
				# 	finalDictionary[w][self.id]
				# 	# print finalDictionary
				# 	# print 'hi'
				# 	finalDictionary[w][self.id][index] +=1
				# except Exception as e:
				# 	try:
				# 		finalDictionary[w]
				# 		finalDictionary[w][self.id][index] = 1
				# 	except:
				# 		finalDictionary[w] = {}
				# 	finalDictionary[w][self.id] = [0, 0, 0, 0, 0, 0]
				# 	finalDictionary[w][self.id][index] = 1
				

	def get(self,field,count):
		if(int(count) == 0):
			return ""
		else:
			return field + str(count)

	def printDictionary(self):
		global docID, finalDictionary, index_file_count_before_merge
		out_file_name = 'output' + str(index_file_count_before_merge)
		index_file_count_before_merge +=1
		output_fd = open(out_file_name,'w')

		for word in sorted(finalDictionary):
			w = word + " "
			for d in sorted(finalDictionary[word]):
				w += str(int(d))
				w += self.get("t",finalDictionary[word][d][0])
				w += self.get("p",finalDictionary[word][d][1])
				w += self.get("i",finalDictionary[word][d][2])
				w += self.get("e",finalDictionary[word][d][3])
				w += self.get("c",finalDictionary[word][d][4])     
				w += self.get("r",finalDictionary[word][d][5])
				w += "|"
			w = w[:-1]
			# print w
			# exit()
			
			output_fd.write(w+"\n")
		output_fd.close()
		
   	# Call when an element starts
	def startElement(self, tag, attributes):
		# print self.title
		self.CurrentData = tag
		self.infoFlag = False
		self.referenceFlag = False
		self.externalFlag = False
		if tag == "page":
			self.title = []
			self.infobox = []
			self.externallinks = []
			self.categories = []
			self.page_content = []
			self.references = []
			self.flag = True
		# print self.title
###################################################################################################################################################################################
   	# Call when a character is read
   	def characters(self, content):
   		# print self.title
   		global docID
   		content = content.encode(encoding='UTF-*', errors='strict')
   		strippedContent = content.strip()
   		if((len(strippedContent) ==0 or len(content)<1)):
   			return
   		categoryData = 0
		if self.CurrentData == "title":
			# print content
			self.title.append(content.lower())
			# print self.title, '1'
			# exit()

		elif self.CurrentData == "id":
			if self.flag == True:
				self.id = docID
				docID +=1 
				output2.write(str(self.id)+ '\t'+self.title[0]+'\n')
				# self.pgId_pgTitle[self.id] = self.title
				# print type(self.id)
				# exit()
				# self.id_pgNo[self.id] = self.pg_no
			# self.pg_no += 1
			# self.pgNO_pgTitle[str(int(self.pg_no))] = self.title

		elif self.CurrentData == "text":
			content = re.sub(self.regExp1,'', content)
			content = re.sub(self.regExp2,'', content)
			content = re.sub(self.regExp3,'', content)
			content = re.sub(self.regExp5,'', content)

            ##################################################################
			if(self.infoFlag == False):
				if(content.find("{{Infobox") != -1):
					self.infoFlag = True
			else:
				if(content == "}}" or content.find(".}}") !=-1):
					self.infoFlag = False
            ##################################################################
			if(self.externalFlag == False):
				if(content.find("==External links==") != -1 or content.find("== External links ==") != -1):
					self.externalFlag = True
			if(self.referenceFlag == False):
				if(content == "==References=="):
					self.referenceFlag = True
				else:
					self.referenceFlag = False
			else:
				if(content.find("==") != -1):
					self.referenceFlag = False
				else:
					self.referenceFlag = True
	        ##################################################################
			categoryData = content[11:-2] if(content.find("[[Category:") != -1) else 0

			if(self.infoFlag == True):
				if(content.find("{{Infobox") != -1):
					self.infobox.append(content[9:].lower())
				else:
					self.infobox.append(content.lower())
			elif(self.externalFlag == True and categoryData == 0):
				if(content.find("== External links") != -1):
					self.externallinks.append(content[22:].lower())
				elif(content.find("==External links") != -1):
					self.externallinks.append(content[19:].lower())
				else:
					self.externallinks.append(content.lower())
			elif(categoryData != 0):
				self.categories.append(categoryData.lower())
			elif(self.referenceFlag == True):
				if(content.find("==References==") != -1):
					# print 'Reference'
					self.references.append(content[14:].lower())
				else:
					# print 'Content', content
					self.references.append(content.lower())
			else:
				self.page_content.append(content.lower())
		# print self.title
   	# Call when an element ends
   	def endElement(self, tag):
   		# print 'title',self.title
   		global wordCount, docID, finalDictionary
   		if tag == "page":
   			# print 'calling', self.infobox
   			self.storeIndexStructure(self.title, "title",0)
   			self.storeIndexStructure(self.page_content, "page_content",1)
   			self.storeIndexStructure(self.infobox,"infobox",2)
   			self.storeIndexStructure(self.externallinks, "externallinks",3)
   			self.storeIndexStructure(self.categories,"categories",4)
   			# print self.references
   			self.storeIndexStructure(self.references,"references",5)
   			if self.id % 4000 == 0:
   				# print 'Dictionary'
   				self.printDictionary()
   				finalDictionary = {}
		elif tag == "id" :
			self.flag = False
   		elif tag == "mediawiki":
   			# print len(finalDictionary)
   			self.printDictionary()
   		
   		self.CurrentData = ""
   		# print self.title

   # 		if tag == 'page':
			# print 'here',finalDictionary
			# exit()


def main():
	global output, output2
	output2 = open('id_title_map','w')
	parser = xml.sax.make_parser() # create an XMLReader
   	parser.setFeature(xml.sax.handler.feature_namespaces, 0) # turn off namepsaces
	Handler = PageHandler() # override the default ContextHandler
	parser.setContentHandler(Handler)
	parser.parse(sys.argv[1])
	output2.close()

if __name__ == '__main__':
	main()
