import os

import yaml

from script import translate_tool, audio_tool, whisper_tool


def getFileNames(path):
    videoFile = []
    files = os.listdir(path)
    for i in range(len(files)):
        if (files[i][-4:] == "webm" or files[i][-4:] == ".mkv"):
            videoFile.append(files[i])
    return videoFile

if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    videoFile = getFileNames(config['path'])
    for file in videoFile:
        filename = file.split('.',1)[0]
        fullpath = os.path.join(config['path'], file)
        outpath = os.path.join(config['output'], filename)
        srtpath = os.path.join(config['path'], filename)
        audio_tool.audio_extract(fullpath, outpath+'.mp3')
        whisper_tool.do_whisper(outpath+'.mp3', srtpath+'.srt')
        translate_tool.do_translate(srtpath+'.srt', srtpath+'-zh.srt', config['from'], config['to'],
                                    config['translate_threads'], config['appid'], config['secretKey'])
        
    # print("audio extract begin")
    # audio_tool.audio_extract(config['input'], config['output'])
    # print("audio extract success")

    # print("whisper begin")
    # whisper_tool.do_whisper(config['output'], config['srt_path'])
    # print("whisper success")

    # print("translate begin")
    # translate_tool.do_translate(config['srt_path'], config['srt_translate_path'], config['from'], config['to'],
    #                             config['translate_threads'])
    # print("translate success")

    # print("success")
