
# Copyright 2011 Greg Warner <gdwarner@gmail.com>
# (Pretty much copied from diagrameditor.py)


from zim.plugins import PluginClass
from zim.plugins.base.imagegenerator import ImageGeneratorClass, BackwardImageGeneratorObjectType

from zim.newfs import LocalFile, TmpFile
from zim.applications import Application, ApplicationError


# TODO put these commands in preferences
diagcmd = ('seqdiag', '-T', 'svg', '-o')


class InsertSequenceDiagramPlugin(PluginClass):

	plugin_info = {
		'name': _('Insert Sequence Diagram'), # T: plugin name
		'description': _('''\
This plugin provides a sequence diagram editor for zim based on seqdiag.
It allows easy editing of sequence diagrams.
'''), # T: plugin description
		'help': 'Plugins:Sequence Diagram Editor',
		'author': 'Greg Warner',
	}

	@classmethod
	def check_dependencies(klass):
		has_diagcmd = Application(diagcmd).tryexec()
		return has_diagcmd, [("seqdiag", has_diagcmd, True)]


class BackwardSequenceDiagramImageObjectType(BackwardImageGeneratorObjectType):

	name = 'image+seqdiagram'
	label = _('Sequence Diagram') # T: menu item
	syntax = None
	scriptname = 'seqdiagram.diag'


class SequenceDiagramGenerator(ImageGeneratorClass):

	imagefile_extension = '.svg'

	def __init__(self, plugin, notebook, page):
		ImageGeneratorClass.__init__(self, plugin, notebook, page)
		self.diagfile = TmpFile('seqdiagram.diag')
		self.diagfile.touch()
		self.imgfile = LocalFile(self.diagfile.path[:-5] + self.imagefile_extension) # len('.diag') == 5

	def generate_image(self, text):
		# Write to tmp file
		self.diagfile.write(text)

		# Call seqdiag
		try:
			diag = Application(diagcmd)
			diag.run((self.imgfile, self.diagfile))
		except ApplicationError:
			return None, None # Sorry, no log
		else:
			return self.imgfile, None

	def cleanup(self):
		self.diagfile.remove()
		self.imgfile.remove()
