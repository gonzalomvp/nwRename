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
parser.add_argument(
	'--alignment',
	'-a',
	type=str,
	default='semi-global',
	dest='alignmentType',
	nargs='?',
	action='store',
	help="Alignment type to be used.",
)
args = parser.parse_args()

def is_to_be_renamed(file):
	
	return re.findall('\.'+args.extension+'$', file)

def abort(msg=''):
	
	raise SystemExit("Aborted.\n"+msg+"\nIf you think this shouldn't've " \
"happened, try calling with \"-a global\"\nIf that doesn't help, please report"\
" it to https://github.com/a442/")

def pair_up(files):
	
	to_be_renamed = []
	rename_to = []
	for f in files:
		if is_to_be_renamed(f):
			to_be_renamed.append(f)
		else:
			rename_to.append(f)
	total_to_rename = len(to_be_renamed)
	if total_to_rename > len(rename_to):
		abort('There are more files to be renamed than files to rename to.')
	aligned = []
	done = 0
	for ren_from in to_be_renamed:
		alignments = [align.Alignment(ren_from, ren_to, alignmentType=args.alignmentType) for ren_to in rename_to]
		scores = [a.getAlignmentScore() for a in alignments]
		chosen = scores.index(max(scores))
		if not rename_to[chosen] in aligned:
			aligned.append(rename_to[chosen])
		else:
			abort("Couldn't determine which file to rename {} to. The best " \
"candidate, {}, is already what {} was selected to be renamed to.".format(
					ren_from, rename_to[chosen], to_be_renamed[chosen]))
		sys.stdout.write(' {} out of {} done\r'.format(done, total_to_rename))
		sys.stdout.flush()
		done += 1
	return to_be_renamed, aligned
		
def ask_confirmation_and_rename(to_be_renamed, aligned):
	
	total_to_rename = len(to_be_renamed)
	print 'Check the new filenames before we rename them:'
	for i in xrange(total_to_rename):
		print aligned[i][:-4]+'.'+args.extension, '<-', to_be_renamed[i]
	try:
		in_ = raw_input(
			"Is that correct? Ctrl+c to stop, enter to continue."
		)
		if args.backup:
			print 'Backing up files to '+args.dir+'backup...'
			if not os.path.exists(args.dir+'backup'):
				os.makedirs(args.dir+'backup')
			for ep in to_be_renamed:
				shutil.copy2(args.dir+ep, args.dir+'backup/'+ep)
			print 'Done.'
		print 'Renaming...'
		for i in xrange(total_to_rename):
			os.rename(
				args.dir+to_be_renamed[i],
				args.dir+aligned[i][:-4]+'.'+args.extension
			)
	except KeyboardInterrupt:
		abort()
	print 'Done.'

def list_files():
	args.dir += '/'
	return [i for i in os.listdir(args.dir) if (
									os.path.isfile(os.path.join(args.dir,i)))]

if __name__ == '__main__':
	to_be_renamed, aligned = pair_up(list_files())
	ask_confirmation_and_rename(to_be_renamed, aligned)
