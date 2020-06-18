import os
import io
import sys
import traceback
import time
import numpy as np

from OpenNaja.pyffi_ext.formats.ovl import OvlFormat
from OpenNaja.pyffi_ext.formats.ms2 import Ms2Format
from OpenNaja.modules import extract, inject, hasher, walker


class MainWindow():

	def __init__(self):
		self.ovl_data = OvlFormat.Data(progress_callback=self.update_progress)

		supported_types = ("DDS", "PNG", "MDL2", "TXT", "FGM", "FDB", "MATCOL", "XMLCONFIG", "ASSETPKG", "LUA")
		self.filter = "Supported files ({})".format( " ".join("*."+t for t in supported_types) )

	@property
	def commands(self,):
		# get those commands that are set to True
		return [ x for x in ("write_dat", "write_frag_log") if getattr(self, x)]

	@property
	def write_dds(self,):
		return self.t_write_dds.isChecked()
	
	@property
	def write_2K(self,):
		return self.t_2K.isChecked()
	
	@property
	def write_dat(self,):
		return self.t_write_dat.isChecked()

	@property
	def write_frag_log(self,):
		return self.t_write_frag_log.isChecked()

	def update_commands(self):
		# at some point, just set commands to archive and trigger changes there
		self.ovl_data.commands = self.commands

	def update_progress(self, message, value=None, vmax=None):
		# avoid gui updates if the value won't actually change the percentage.
		# this saves us from making lots of GUI update calls that don't really
		# matter.
		try:
			if vmax > 100 and (value % (vmax // 100)) and value != 0:
				value = None
		except ZeroDivisionError:
			value = 0
		except TypeError:
			value = None
		
	def load_ovl(self, filepath):
		ovl_name = os.path.split(filepath)
		start_time = time.time()			
		try:
			with open(filepath, "rb") as ovl_stream:
				self.ovl_data.read(ovl_stream, file=filepath)
			self.ovl_name = ovl_name
		except Exception as ex:
			traceback.print_exc()
			print(ex)
		print(f"Done in {time.time()-start_time:.2f} seconds!")
		self.update_progress("Operation completed!", value=1, vmax=1)
		
	def save_ovl(self, filepath):
		ovl_name = os.path.split(filepath)
		# just a dummy stream
		with io.BytesIO() as ovl_stream:
			self.ovl_data.write(ovl_stream, file_path=filepath)
		print("Done!")
	
	def skip_messages(self, error_files, skip_files):
		error_count = len(error_files)
		skip_count = len(skip_files)
		if error_count:
			print("Files not extracted due to error:")
			for ef in error_files:
				print("\t",ef)
			
		if skip_count:
			print("Unsupported files not extracted:")
			for sf in skip_files:
				print("\t",sf)
				
	
	def extract_all(self):
				dir = self.cfg["dir_extract"]
				# create output dir
				try:
					os.makedirs(dir, exist_ok=True)
					error_files = []
					skip_files = []
					da_max = len(self.ovl_data.archives)
					for da_index, archive in enumerate(self.ovl_data.archives):
						self.update_progress("Extracting archives", value=da_index, vmax=da_max)
						
						archive.dir = dir
						error_files_new, skip_files_new = extract.extract(archive, self.write_dds, progress_callback=self.update_progress)
						error_files += error_files_new
						skip_files += skip_files_new
							
					self.skip_messages(error_files, skip_files)
					self.update_progress("Operation completed!", value=1, vmax=1)
				except Exception as ex:
					traceback.print_exc()
					print(ex)
			
	def inject(self, files):
		try:
			inject.inject( self.ovl_data, files, True, False )
		except Exception as ex:
			traceback.print_exc()
		print("Done!")
			
	def hasher(self):
		if self.ovl_name:
			names = [ (tup[0].text(), tup[1].text()) for tup in self.e_name_pairs ]
			for archive in self.ovl_data.archives:
				hasher.dat_hasher(archive, names, self.ovl_data.header.files,self.ovl_data.header.textures)

	def walker(self, dummy=False, walk_ovls=True, walk_models=True):
		errors = []
		if start_dir:
			export_dir = os.path.join(start_dir, "walker_export")
			# don't use internal data
			ovl_data = OvlFormat.Data()
			mdl2_data = Ms2Format.Data()
			if walk_ovls:
				error_files = []
				skip_files = []
				ovl_files = walker.walk_type(start_dir, extension="ovl")
				of_max = len(ovl_files)
				for of_index, ovl_path in enumerate(ovl_files):
					self.update_progress("Walking OVL files: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
					try:
						# read ovl file
						with open(ovl_path, "rb") as ovl_stream:
							ovl_data.read(ovl_stream, file=ovl_path, commands=self.commands, mute=True)
						# create an output folder for it
						outdir = os.path.join(export_dir, os.path.basename(ovl_path[:-4]))
						# create output dir
						os.makedirs(outdir, exist_ok=True)
						for archive in ovl_data.archives:
							archive.dir = outdir
							error_files_new, skip_files_new = extract.extract(archive, self.write_dds, only_types=["ms2",])#, progress_callback=self.update_progress)
							error_files += error_files_new
							skip_files += skip_files_new
					except Exception as ex:
						traceback.print_exc()
						errors.append((ovl_path, ex))
						
				self.skip_messages(error_files, skip_files)

			# holds different types of flag - list of byte maps pairs
			type_dic = {}
			if walk_models:
				mdl2_files = walker.walk_type(export_dir, extension="mdl2")
				mf_max = len(mdl2_files)
				for mf_index, mdl2_path in enumerate(mdl2_files):
					mdl2_name = os.path.basename(mdl2_path)
					self.update_progress("Walking MDL2 files: " + mdl2_name, value=mf_index, vmax=mf_max)
					try:
						with open(mdl2_path, "rb") as mdl2_stream:
							mdl2_data.read(mdl2_stream, file=mdl2_path, quick=True, map_bytes=True)
							for model in mdl2_data.mdl2_header.models:
								if model.flag not in type_dic:
									type_dic[model.flag] = ([], [])
								type_dic[model.flag][0].append(mdl2_name)
								type_dic[model.flag][1].append(model.bytes_map)
					except Exception as ex:
						traceback.print_exc()
						errors.append((mdl2_path, ex))
			# report
			print("\nThe following errors occured:")
			for file_path, ex in errors:
				print(file_path, str(ex))

			print("\nThe following type - map pairs were found:")
			for flag, tup in type_dic.items():
				print(flag, bin(flag))
				names, maps_list = tup
				print("Some files:", list(set(names))[:25])
				print("num models", len(maps_list))
				print("mean", np.mean(maps_list, axis=0).astype(dtype=np.ubyte))
				print("max", np.max(maps_list, axis=0))
				print()
				
			self.update_progress("Operation completed!", value=1, vmax=1)

	def closeEvent(self, event):
		print('close')

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32