#!/usr/bin/env python
# Created by zahza at 3/11/20

from audio import AudioStream

session_id = "123456"
project_id = "atomic-nation-268705"
language_code = "en-US"


def main():
	while True:
		audio = AudioStream.record_voice(recording_duration=5)
		AudioStream.write_audio_file(audio)
		parsed_audio = AudioStream.parse_audio()
		print("User Said: " + str(parsed_audio))
		print("Assistant Said: " + str(
			AudioStream.detect_intent_texts(project_id, session_id, parsed_audio, language_code)))


if __name__ == '__main__':
	main()
