# -*- coding: utf-8 -*-
import json
import os
import sys
import tarfile
import zipfile
from subprocess import getoutput
from urllib.request import Request, urlopen

VERSION = '2.4.1'

HEADER = '	      __   ___  __          __  ___                 ___  __  \n' \
		 '  |\/| |__) |__  /__` | |\ | /__`  |   /\  |    |    |__  |__) \n' \
		 '  |  | |    |___ .__/ | | \| .__/  |  /~~\ |___ |___ |___ |  \ \n' \
		 '                                   Scripton [ ' + VERSION + ' ]    \n'

CONTACT_LINK = "t.me/teslx"

FUCKING_LANG = "en"


class C:
	HEADER = '\033[0;95m'
	BLUE = '\033[0;94m'
	CYAN = '\033[0;96m'
	YELLOW = '\033[0;93m'
	RED = '\033[0;91m'
	NULL = '\033[0m'
	GREEN = '\033[0;92m'
	WHITE = '\033[0;97m'
	BLACK = '\033[0;90m'


class log:
	@staticmethod
	def errorln(text, separ=' + '):
		print("\n" + C.RED + separ + "ERROR: " + C.NULL + text)

	@staticmethod
	def infoln(text, separ=' + '):
		print("\n" + C.BLUE + separ + C.NULL + text)

	@staticmethod
	def warnln(text, separ=' + '):
		print("\n" + C.YELLOW + separ + C.NULL + text)

	@staticmethod
	def successln(text, separ=' + '):
		print("\n" + C.GREEN + separ + C.NULL + text)

	@staticmethod
	def error(text, separ=' + '):
		print(C.RED + separ + "ERROR: " + C.NULL + text)

	@staticmethod
	def info(text, separ=' + '):
		print(C.BLUE + separ + C.NULL + text)

	@staticmethod
	def warn(text, separ=' + '):
		print(C.YELLOW + separ + C.NULL + text)

	@staticmethod
	def success(text, separ=' + '):
		print(C.GREEN + separ + C.NULL + text)


def install(srv, path, is_bin_file=True):
	download_link = srv['download']['link']
	type = srv['type']
	download_file = srv['download']['file']
	download_dirname = srv['download']['dirname']
	bin_file = srv['bin']['file']
	start_cmd = srv['start_cmd']

	# srv['download']['link'] = srv['download']['link'].replace('https', 'http')
	if type != 'jenkins':
		# log.warn(LANG[FUCKING_LANG]['downloading'] + '..', '   - ')
		download(download_link, '/tmp/' + download_file)
		if type == 'archive':
			log.warn(LANG[FUCKING_LANG]['extracting'] + '..', '   - ')
			extract_file('/tmp/' + download_file, '/tmp/')
			copyfile('/tmp/' + download_dirname + '/src ', path)
			copyfile('/tmp/' + download_dirname + '/start.sh ', path)
		elif type == 'github':
			# In dev
			log.error("this function in develop")
		elif type == 'file':
			copyfile('/tmp/' + download_file, path)
			log.warn(LANG[FUCKING_LANG]['gstart'] + '..', '   - ')
			copyfile('/tmp/' + download_file, path)
			cmd = getoutput('echo "' + start_cmd + '" > ' + path + '/start.sh')

		if is_bin_file is True:
			if bin_file != '-':
				log.info('Installing bin:' + '..')
				# log.warn(LANG[FUCKING_LANG]['downloading'] + '..', '   - ')
				download(srv['bin']['link'], '/tmp/' + bin_file)
				log.warn(LANG[FUCKING_LANG]['extracting'] + '..', '   - ')
				extract_file('/tmp/' + bin_file, path)
	else:
		file_name = json.loads(
			request(download_link + '/lastSuccessfulBuild/api/python?pretty=true').read())
		download_url = download_link + '/lastSuccessfulBuild/artifact/' + file_name['artifacts'][0][
			'fileName']

		download(download_url, '/tmp/' + file_name)
		cmd = getoutput('cp -a ' + '/tmp/' + file_name + ' ' + path)
		log.warn(LANG[FUCKING_LANG]['gstart'] + '..', '   - ')
		cmd = getoutput('echo "' + start_cmd + '" > ' + path + '/start.sh')

	cmd = getoutput('rm -rf ' + path + '/tmp')
	cmd = getoutput('chmod +x ' + path + '/start.sh')

	if path == '.':
		starter = './start.sh'
	else:
		starter = 'cd ' + path + ' && ./start.sh'
		log.success(LANG[FUCKING_LANG]['ok'] + ' ' + C.GREEN + starter + C.NULL)


def download(url, path, text='Downloading..'):
	# print(text.encode('utf-8'))
	req = Request(url, headers={'User-Agent': "Magic Browser"})
	resource = urlopen(req)
	out = open(path, 'wb')

	total_length = float(resource.headers['content-length'])
	dwn_length = 0
	tmp = resource.read(1024)

	while total_length != dwn_length:
		out.write(tmp)
		dwn_length += len(tmp)
		percent = float(dwn_length / total_length * 100) / 100
		hashes = '#' * int(round(percent * 20))
		spaces = ' ' * (20 - len(hashes))
		sys.stdout.write(
			'\r   - {2}{6}: {2}[{4}{0}{2}] {3}{1}%{5}'.format(hashes + spaces, int(round(percent * 100)), C.NULL,
															  C.YELLOW,
															  C.GREEN, C.NULL, text))

		sys.stdout.flush()
		tmp = resource.read(1024)

	out.write(resource.read())
	out.close()
	print('')


def request(url):
	return urlopen(url)


def copyfile(source, to):
	return getoutput('cp -a ' + source + ' ' + to)


def extract_file(path, to_directory='.'):
	if path.endswith('.zip'):
		zip_ref = zipfile.ZipFile(path, 'r')
		zip_ref.extractall(to_directory)
		zip_ref.close()
	elif path.endswith('.tar.gz') or path.endswith('.tgz'):
		tar = tarfile.open(path)
		tar.extractall(to_directory)
		tar.close()
	elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
		opener, mode = tarfile.open, 'r:bz2'
	else:
		raise ValueError('Could not extract `%s` as no appropriate extractor is found' % path)


# def update(srv, path):
#     print(C.HEADER + ' - ' + C.NULL + LANG[FUCKING_LANG]['updating'] + ' ' + C.WHITE + srv[
#         'name'] + C.NULL + ':')
#     cmd = commands.getoutput('rm -rf src ' + path + '/PocketMin* ' + path + '/nukkit-*.jar')
#
#     srv['download']['link'] = srv['download']['link'].replace('https', 'http')
#     if (srv['type'] != 'jenkins'):
#         Utils.download(srv['download']['link'], path + '/tmp/' + srv['download']['file'],
#                        C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['downloading'] + '..')
#         if (srv['type'] == 'archive'):
#             print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['extracting'] + '..')
#             Utils.extract_file(path + '/tmp/' + srv['download']['file'], path + '/tmp')
#             cmd = commands.getoutput('cp -a ' + path + '/tmp/' + srv['download']['dirname'] + '/src ' + path)
#         elif (srv['type'] == 'github'):
#             # In dev
#             print("this function in develop")
#         elif (srv['type'] == 'file'):
#             cmd = commands.getoutput('cp -a ' + path + '/tmp/' + srv['download']['file'] + ' ' + path)
#             print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['gstart'] + '..')
#             cmd = commands.getoutput('echo "' + srv['start_cmd'] + '" > ' + path + '/start.sh')
#
#     else:
#         file_name = json.loads(
#             Utils.request(srv['download']['link'] + '/lastSuccessfulBuild/api/python?pretty=true').read())
#         download_url = srv['download']['link'] + '/lastSuccessfulBuild/artifact/' + file_name['artifacts'][0][
#             'fileName']
#
#         Utils.download(download_url, path + '/tmp/' + file_name,
#                        C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['downloading'] + '..')
#         cmd = commands.getoutput('cp -a ' + path + '/tmp/' + file_name + ' ' + path)
#         print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['gstart'] + '..')
#         cmd = commands.getoutput('echo "' + srv['start_cmd'] + '" > ' + path + '/start.sh')
#
#     cmd = commands.getoutput('rm -rf ' + path + '/tmp')
#     cmd = commands.getoutput('chmod +x ' + path + '/start.sh')
#
#     if (path == '.'):
#         starter = './start.sh'
#     else:
#         starter = 'cd ' + path + ' && ./start.sh'
#
#     print(C.NULL + '  ----------------------------------------')
#     print(C.WHITE + '  ' + LANG[FUCKING_LANG]['ok'] + ' ' + C.GREEN + starter + C.NULL)
#
#     def reinstall(srv, path):
#
#         print(C.RED + ' + ' + C.NULL + LANG[FUCKING_LANG][
#             'rei_warning'] + ' ' + C.WHITE + '(1)' + C.NULL + ': ' + C.WHITE)
#         inputin = Utils.inputin(' : ' + C.WHITE, 'No', False)
#
#         if inputin != 'No':
#             print(C.HEADER + ' - ' + C.NULL + LANG[FUCKING_LANG]['reinstalling'] + ' ' + C.WHITE + srv[
#                 'name'] + C.NULL + ':')
#             cmd = commands.getoutput(
#                 'rm -rf src ' + path + '/PocketMin* ' + path + '/start.sh ' + path + '/nukkit-*.jar' + path + '/pl*' + path + '/*.jar' + path + '/*.phar' + path + '/*ump*' + path + '/server*' + path + '/pocket*' + path + '/nukkit*')
#             srv['download']['link'] = srv['download']['link'].replace('https', 'http')
#             if (srv['type'] != 'jenkins'):
#                 Utils.download(srv['download']['link'], path + '/tmp/' + srv['download']['file'],
#                                C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['downloading'] + '..')
#                 if (srv['type'] == 'archive'):
#                     print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['extracting'] + '..')
#                     Utils.extract_file(path + '/tmp/' + srv['download']['file'], path + '/tmp')
#                     cmd = commands.getoutput('cp -a ' + path + '/tmp/' + srv['download']['dirname'] + '/src ' + path)
#                     cmd = commands.getoutput(
#                         'cp -a ' + path + '/tmp/' + srv['download']['dirname'] + '/start.sh ' + path)
#                 elif (srv['type'] == 'github'):
#                     # In dev
#                     print("this function in develop")
#                 elif (srv['type'] == 'file'):
#                     cmd = commands.getoutput('cp -a ' + path + '/tmp/' + srv['download']['file'] + ' ' + path)
#                     print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['gstart'] + '..')
#                     cmd = commands.getoutput('echo "' + srv['start_cmd'] + '" > ' + path + '/start.sh')
#
#                 if (srv['bin']['file'] != '-'):
#                     print(C.HEADER + ' - ' + C.NULL + 'Installing bin:')
#                     Utils.download(srv['bin']['link'], path + '/tmp/' + srv['bin']['file'],
#                                    C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['downloading'] + '..')
#                     print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['extracting'] + '..')
#                     Utils.extract_file(path + '/tmp/' + srv['bin']['file'], path)
#             else:
#                 file_name = json.loads(
#                     Utils.request(srv['download']['link'] + '/lastSuccessfulBuild/api/python?pretty=true').read())
#                 download_url = srv['download']['link'] + '/lastSuccessfulBuild/artifact/' + file_name['artifacts'][0][
#                     'fileName']
#
#                 Utils.download(download_url, path + '/tmp/' + file_name,
#                                C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['downloading'] + '..')
#                 cmd = commands.getoutput('cp -a ' + path + '/tmp/' + file_name + ' ' + path)
#                 print(C.YELLOW + '  + ' + C.NULL + LANG[FUCKING_LANG]['gstart'] + '..')
#                 cmd = commands.getoutput('echo "' + srv['start_cmd'] + '" > ' + path + '/start.sh')
#
#             cmd = commands.getoutput('rm -rf ' + path + '/tmp')
#             cmd = commands.getoutput('chmod +x ' + path + '/start.sh')
#
#             if (path == '.'):
#                 starter = './start.sh'
#             else:
#                 starter = 'cd ' + path + ' && ./start.sh'
#
#             print(C.NULL + '  ----------------------------------------')
#             print(C.WHITE + '  ' + LANG[FUCKING_LANG]['ok'] + ' ' + C.GREEN + starter + C.NULL)
#         else:
#             try:
#                 sys.exit(0)
#             except SystemExit:
#                 os._exit(0)


def inputin(placeholder, default, tpl=True):
	try:
		if tpl:
			return input(C.YELLOW + ' + ' + C.NULL + placeholder + C.BLUE + ' (' + str(
				default) + ')' + C.NULL + ': ') or default
		else:
			return input(placeholder) or default
	except KeyboardInterrupt:
		log.errorln('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)


def check_lang():
	if not os.path.exists('mpesinstaller_data'):
		cmd = getoutput('mkdir mpesinstaller_data')
		if not os.path.exists('mpesinstaller_data/lang.txt'):
			print(
				C.YELLOW + ' + ' + C.NULL + 'Select lang ' + C.WHITE + '(1)' + C.NULL + ': ' + C.WHITE)
			print(C.YELLOW + '   ' + C.GREEN + '1' + C.NULL + ') ' + C.WHITE + 'English' + C.NULL)
			print(
				C.YELLOW + '   ' + C.GREEN + '2' + C.NULL + ') ' + C.WHITE + 'Українська' + C.NULL)
			print(C.YELLOW + '   ' + C.GREEN + '3' + C.NULL + ') ' + C.WHITE + 'Русский' + C.NULL)
			lang = inputin(' : ' + C.WHITE, 1, False)

			lang = int(lang)

			if lang == 1:
				cmd = getoutput('echo "en" > mpesinstaller_data/lang.txt')
			elif lang == 2:
				cmd = getoutput('echo "uk" > mpesinstaller_data/lang.txt')
			elif lang == 3:
				cmd = getoutput('echo "ru" > mpesinstaller_data/lang.txt')

	return getoutput('cat mpesinstaller_data/lang.txt')


class Main:
	@staticmethod
	def run():
		print(HEADER)

		if request(
				'https://raw.githubusercontent.com/TesLex/MPESInstaller/master/version.txt').read().strip() != VERSION:
			log.warn(
				'Please upgrade the installer by command: " + C.HEADER + "wget -O installer.py '
				'"mpeserver.github.io/MPESInstaller/installer.py" && chmod +x ./installer.py && ./installer.py\n')

		log.info(LANG[FUCKING_LANG]['action'] + ' (1):')
		log.info(C.YELLOW + '1) ' + C.NULL + LANG[FUCKING_LANG]['install'], '   ')
		log.info(C.YELLOW + '2) ' + C.NULL + LANG[FUCKING_LANG]['update'], '   ')
		log.info(C.YELLOW + '3) ' + C.NULL + LANG[FUCKING_LANG]['reinstall'], '   ')
		action = inputin(" : " + C.YELLOW, "1", False)

		log.info(LANG[FUCKING_LANG]['path'] + ' (.):')
		path = inputin(' : ', '.', False)

		if path != '.' and not os.path.exists(path):
			cmd = getoutput('mkdir -p ' + path)

		SERVERS = json.load(request('http://raw.githubusercontent.com/TesLex/MPESInstaller/master/servers.json'))

		log.info(LANG[FUCKING_LANG]['core'] + ' (1):')
		for i, s in enumerate(SERVERS):
			log.warn(s['name'], '   ' + str(i + 1) + ') ')
		sex = inputin(' : ', '1', False)

		if int(action) == 1:
			log.info(LANG[FUCKING_LANG]['installing'] + ' ' + SERVERS[int(sex) - 1]['name'])
			install(SERVERS[int(sex) - 1], path)
		elif int(action) == 2:
			log.error("In develop")
		elif int(action) == 3:
			log.error("In develop")
		else:
			log.error("not found")
		exit(0)


# try:
LANG = json.load(request('http://raw.githubusercontent.com/TesLex/MPESInstaller/master/lang.json'))
FUCKING_LANG = check_lang()
Main.run()
# except Exception as e:
# 	log.error(str(e))
# 	log.info('Please contact with us: ' + C.GREEN + CONTACT_LINK)
