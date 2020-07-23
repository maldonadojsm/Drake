# !/usr/bin/env python

import multiprocessing as mp


class ParallelP:
	def __init__(self):
		self.parallel_threads = []

	def construct_threads(self, process, flag):
		"""
		Build threads according to flags
		@param process: Process that will run in parallel
		@param flag:
		"""
		self.parallel_threads.append(self.prepare_batch(process, flag))

	@staticmethod
	def prepare_batch(workflow_object, flag):

		if flag == 0:
			m = mp.Process(target=workflow_object.start_video_stream)
			return m

		elif flag == 1:
			m = mp.Process(target=workflow_object.start_audio_stream)
			return m

	def run_in_parallel(self):
		"""
		Start & Join Parallel Threads
		"""
		for p in self.parallel_threads:
			p.start()
		for p in self.parallel_threads:
			p.join()
