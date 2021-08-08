from NaoVoiceControl import NaoVoiceControl

# Please change keywords and context paths to match your OS , files for windows , linux and mac are available
# under hotwords and commands directory
keyword_path = "hotwords/hey-neo__en_windows_2021-09-06-utc_v1_9_0.ppn"
context_path = "commands/NaoBot_en_windows_2021-09-06-utc_v1_6_0.rhn"
NaoVoiceControl(keyword_path, context_path).run()
