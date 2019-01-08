mate-terminal --tab --title='roscore' -e 'bash -c "sleep 1s && cd \"/home/maximilian/Git/EmeraldAI/EmeraldAI/Application/ExecutionScripts\" && roscore ; bash"'


mate-terminal --tab --title='Brain STT' -e 'bash -c "sleep 5s && cd \"/home/maximilian/Git/EmeraldAI/EmeraldAI/Application/ExecutionScripts\" && ./RunBrain_STT.sh ; bash"'

mate-terminal --tab --title='STT' -e 'bash -c "sleep 5s && cd \"/home/maximilian/Git/EmeraldAI/EmeraldAI/Application/ExecutionScripts\" && ./RunSTT.sh ; bash"'

mate-terminal --tab --title='TTS' -e 'bash -c "sleep 5s && cd \"/home/maximilian/Git/EmeraldAI/EmeraldAI/Application/ExecutionScripts\" && ./RunTTS.sh ; bash"'


