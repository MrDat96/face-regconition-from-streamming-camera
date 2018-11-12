import os
import pickle
import shutil
import subprocess
import json

import click
from PIL import Image

from fas_recognition import detection, feature_extraction

def probe(input_video_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(input_video_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = ["ffprobe",
               "-loglevel",  "quiet",
               "-print_format", "json",
               "-show_format",
               "-show_streams",
               input_video_path
              ]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def video_duration(input_video_path):
    """
        Video's duration in seconds, return a float number
    """
    _json = probe(input_video_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('Wrong format video')
    # return None


def training(input_video_path, output_encodings_folder, user_id):
    # encode_path = os.getenv("ENCODE_PATH")
    # video_path = os.getenv("VIDEO_STORE_PATH")
    # print("Encdoe path :" + encode_path + " " + encode_name)
    # print("Video Store :" + video_path + " " + video_name)
    print("Video path " + input_video_path)
    print("Output encodesing foler " + output_encodings_folder)
    print("User ID " + user_id)

    if (user_id is None or user_id == ''):
        print("User ID can not be null")

    if 10 < video_duration(input_video_path) < 60:
        # os.makedirs(output_encodings_folder, exist_ok=True)

        detector = detection.MTCNNDetector(thresholds=[0.75, 0.85, 0.85])
        encoder = feature_extraction.FaceEncoder()

        input_video_name = os.path.basename(input_video_path)
        label = os.path.splitext(input_video_name)[0]

        output_frame_folder = f'./{label}_frames'
        os.makedirs(output_frame_folder, exist_ok=True)

        # Cut video into frames
        subprocess.call(['ffmpeg', '-i', input_video_path, '-vf', 'fps',
                         output_frame_folder + '/%04d.jpg', '-loglevel',
                         'quiet'])

        # Initialize encodings array
        encodings = []

        # Encode faces
        frames = os.listdir(output_frame_folder)

        i = 0
        offset = 0
        step = int(len(frames) * 0.05)

        while len(encodings) < 75:
            if i >= len(frames):
                offset += 1
                i = offset

            if offset == step:
                break

            frame_path = os.path.join(output_frame_folder, frames[i])

            frame = Image.open(frame_path)

            i += step

            # Detect face in frame
            boxes = detector.detect(frame)
            if len(boxes) != 1:
                continue

            # Encode the face and append to array
            encodings.append(encoder.encode(frame, boxes)[0])

        # Delete frames
        shutil.rmtree(output_frame_folder)

        # Don't save encodings if not enough 75 faces were processed
        if len(encodings) != 75:
            raise Exception('Video does not meet requirement')
            return false

        # Save face encodings file
        output_encodings_file = os.path.join(output_encodings_folder,
                                             f'{user_id.lower()}.fev')
        with open(output_encodings_file, 'wb') as output_file:
            pickle.dump(encodings, output_file)
        print("Training " + user_id + " finished")
        return True
    else:
        raise Exception('Video does not meet requirement')
        return False