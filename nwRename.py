import os
import argparse
import re
import shutil
import textwrap
import sys
import align

parser = argparse.ArgumentParser(
	prog='python nwRename.py',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent(
	"""Auto rename files based on similarity.
	
assumes:
	There are only files of two different 3-letter extensions in the folder.
	"""),
)
parser.add_argument(
	'--no-backup',
	'-n',
	const=False,
	default=True,
	dest='backup',
	action='store_const',
	help="Don't backup the files before renaming (only the ones with the " \
"provided extension are renamed)."
)
parser.add_argument(
	'-e',
	type=str,
	default='srt',
	dest='extension',
	nargs='?',
	action='store',
	help="File extension. Default is .srt.",
)
parser.add_argument(
	'dir',
	type=str,
	default=os.getcwd(),
	nargs='?',
	action='store',
	help="The directory where the files are (default is the dir from which " \
"this file was called. Use only absolute paths.)",
)
args = parser.parse_args()

def issub(file):
	
	return re.findall('\.'+args.extension+'$', file)

def abort(msg=''):
	
	raise SystemExit('Aborted.\n'+msg)

def pair_up(files):
	subs = []
	vids = []
	for f in files:
		if issub(f):
			subs.append(f)
		else:
			vids.append(f)
	if len(subs) != len(vids):
		print "Different number of files with one extension than with other. " \
"This results in undefined behaviour, but should work..."
	aligned_vids = []
	i = 0
	n = len(subs)
	for s in subs:
		alignments = [align.Alignment(s, v) for v in vids]
		scores = [a.getAlignmentScore() for a in alignments]
		chosen = scores.index(max(scores))
		aligned_vids.append(vids[chosen])
		sys.stdout.write(' {} out of {} done\r'.format(i, n))
		sys.stdout.flush()
		i += 1
	return subs, aligned_vids
		

def ask_confirmation_and_rename(subs, aligned_vids):
	
	print 'Check new filenames before we rename them:'
	for i in xrange(len(subs)):
		print aligned_vids[i][:-4]+'.'+args.extension, '<-', subs[i]
	try:
		in_ = raw_input(
			"Is that correct? Ctrl+c to stop, enter to continue."
		)
		if args.backup:
			print 'Backing up files to '+args.dir+'backup...'
			if not os.path.exists(args.dir+'backup'):
				os.makedirs(args.dir+'backup')
			for ep in subs:
				shutil.copy2(args.dir+ep, args.dir+'backup/'+ep)
			print 'Done.'
		print 'Renaming...'
		for i in xrange(len(subs)):
			os.rename(
				args.dir+subs[i],
				args.dir+aligned_vids[i][:-4]+'.'+args.extension
			)
	except KeyboardInterrupt:
		abort("If you'd like to see this fixed, report it to " \
"https://github.com/a442")
	
	print 'Done.'

def list_files():
	args.dir += '/'
	return [i for i in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir,i))	]

if __name__ == '__main__':
	subs, aligned_vids = pair_up(list_files())
	ask_confirmation_and_rename(subs, aligned_vids)
