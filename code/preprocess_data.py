from vncorenlp import VnCoreNLP
import re
import sys
import os
from underthesea import ner


def detect_ner(list_senc, ners):
	list_par=[]
	for par in list_senc:
		list_senc=[]
		for senc in par:

			##vncorenlp
			# PERSON = ners.ner(senc)
			# for p in PERSON[0]:
			# 	if p[1] != 'O':
			# 		senc = senc.replace(p[0].replace('_', ' '), p[1])

			#underthesea
			PERSON = ner(senc)
			for p in PERSON:
				if p[3] != 'O':
					senc = senc.replace(p[0], p[3])


			DATE = re.findall(r"\d\d*[-|/]\d\d*[-|/]\d\d\d\d|[N|n]gày \d\d* tháng \d\d* năm \d\d\d\d|[N|n]ăm \d\d\d\d|[T|t]háng \d\d*", senc)
			if DATE!=[]:
				for date in DATE:
					senc = senc.replace(date,'DATE')

			CODE = re.findall(r'[a-z]*[A-Z]*\d*[/|-|]\d*[/||-][A-Z]*[a-z]*\d*[-|/|]*[A-Z]*[a-z]*\d*', senc)
			if CODE!=[]:
				for code in CODE:
					for c in senc.split(' '):
						if code in c:
							senc = senc.replace(c,'CODE')

			MONEY = re.findall(r"\d*,\d*,\d*[,|.]*\d*[,|.]*\d*", senc)
			if MONEY!=[]:
				for money in MONEY:
					for m in senc.split(' '):
						if money in m:
							senc = senc.replace(m, 'MONEY')

			NUMBER = re.findall(r'\d\d*[,]*\đ*', senc)
			if NUMBER!=[]:
				for number in NUMBER:
					for n in senc.split(' '):
						if number in n:
							senc = senc.replace(n, 'NUMBER')

			list_senc.append(senc)
		# print('. '.join(list_senc))
		list_par.append('. '.join(list_senc))
	return '\n'.join(list_par)


def write_file(txt, name, output='../result/'):
	with open(output+name, 'w+') as f:
 		f.write(txt)

def remove_space(content):
	list_s = [' '.join(line.strip().split()) for line in content.split('\n') if line.strip() != '']
	return '\n'.join([s.lower() if s.isupper() else s for s in list_s])
	

def process(content, ner, name):
	non_space = remove_space(content)
	paragraph = non_space.split('\n')
	sentence = map(lambda s: [i_.strip() for i_ in s.split('.') if i_ != ''] ,paragraph)
	list_senc = list(sentence)
	# write_file('\n'.join(['. '.join(_) for _ in list_senc]), 'data.txt')
	# write_file(detect_ner(list_senc, ner), name)
	gen_data_crnn()

	# return result

def gen_data_crnn():
	words = set()
	content = open('../result/data.txt', 'r').read()
	for i in content.split('\n'):
		for j in i.split(' '):
			words.add(j)

	with open('../result/words.txt', 'w+') as f:
		for i in words:
			f.write(i+'\n')



def main(folder_input, path_jar_file='/home/gmo/Desktop/SpellingCrectionVN/VnCoreNLP/VnCoreNLP-1.1.1.jar'):

	# ner = VnCoreNLP(path_jar_file, annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')
	ner=''
	# print(ner.ner("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."))

	for i in os.listdir(folder_input):
		print(i+'--------------------------------')
		content = open(folder_input+i, 'r').read()
		# print(content)
		result = process(content, ner, i)


if __name__ == '__main__':
	main(sys.argv[1])