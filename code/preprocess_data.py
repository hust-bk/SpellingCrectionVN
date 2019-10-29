from vncorenlp import VnCoreNLP
import re
import sys
import os


def detect_ner(list_senc):
	for par in list_senc:
		for senc in par:

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

			MONNEY = re.findall(r"\d*,\d*,\d*[,|.]*\d*[,|.]*\d*", senc)
			if MONNEY!=[]:
				for monney in MONNEY:
					for m in senc.split(' '):
						if monney in m:
							senc = senc.replace(m, 'MONNEY')

			NUMBER = re.findall(r'\d\d*[,]*\đ*', senc)
			if NUMBER!=[]:
				for number in NUMBER:
					for n in senc.split(' '):
						if number in n:
							senc = senc.replace(n, 'NUMBER')

			print(senc)
			# if NUMBER!=[]:
			# 	print(NUMBER)
			# print(NUMBER)

def remove_space(content):
	return '\n'.join([' '.join(line.strip().split()) for line in content.split('\n') if line.strip() != ''])
	

def process(content, path_jar_file='./VnCoreNLP-1.1.1.jar'):
	non_space = remove_space(content)
	paragraph = non_space.split('\n')
	sentence = map(lambda s: [i_.strip() for i_ in s.split('.') if i_ != ''] ,paragraph)
	list_senc = list(sentence)
	detect_ner(list_senc)
	# annotator = VnCoreNLP(path_jar_file, annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')
	# result = annotator.annotate(content)   
	# return result


def main(folder_input):
	for i in os.listdir(folder_input):
		print(i+'--------------------------------')
		content = open(folder_input+i, 'r').read()
		# print(content)
		result = process(content)


if __name__ == '__main__':
	main(sys.argv[1])