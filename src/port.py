import moviepy.editor as moviepy
import moviepy.video.fx.all as vfx
from PIL import Image
from pillow_heif import register_heif_opener
from tkinter import filedialog
import cv2
import os


def _fetch_data(file_path):
    """Gathers data about inputed file

    :param str file_path: the imported file path

    :returns: data about imported file
    :rtype: list
    """
    cv2_file = cv2.VideoCapture(file_path[0])
    frame = cv2_file.read()[1]

    name = os.path.splitext(os.path.basename(file_path[0]))[0]
    res = (int(cv2_file.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cv2_file.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    format = str(file_path[0]).split(".")[-1]
    try:
        if len(frame.shape) == 2:
            color_mode = "L"
        elif frame.shape[2] == 4:
            color_mode = "RGBA"
        else:
            color_mode = "RGB"
    except Exception:
            color_mode = "RGB"

    cv2_file.release()
    data = [name,res,color_mode,format,file_path]
    return data


def _save_image(data,export_path):
    """saves an image

    :param list data: data from GUI

    :param str export_path: the path to export file to
    """
    register_heif_opener()
    with Image.open(data["Path"][0]) as image:
        new_image = image.resize(([int(data["X"]),int(data["Y"])]))
        new_image = new_image.convert(data["Color_Space"],palette=Image.Palette.ADAPTIVE)
        new_image.save(f"{export_path}/{data["Name"]}.{data["Format"]}")


def _save_video(data,export_path):
    """saves an video/sequence

    :param list data: data from GUI

    :param str export_path: the path to export file to
    """
    vid_codec = {"mp4":"libx264", "avi":"rawvideo",
                "mov":"libx264", "mkv":"libx264",
                "webm":"libvpx", "3gp":"libx264",
                "flv":"libx264", "ogv":"libtheora",
                "mpeg":"libx264", "m4v":"libx264"}
    audio_codec = {"mp4":"aac", "avi":"mp3",
                  "mov":"aac", "mkv":"aac",
                  "webm":"libvorbis", "3gp":"aac",
                  "flv":"aac", "ogv":"libvorbis",
                  "mpeg":"mp3", "m4v":"aac"}
    
    amount_of_frames = len(list(data["Path"]))
    if amount_of_frames > 1:
        img_seq = list(data["Path"])
        img_seq.sort()
        clip = moviepy.ImageSequenceClip(img_seq,fps=24)
    else:
        clip = moviepy.VideoFileClip(data["Path"][0])

    clip = clip.resize(([int(data["X"]),int(data["Y"])]))
    if data["Color_Space"] == "L":
        clip = clip.fx(vfx.blackwhite)

    if data["Format"] == "gif":
        clip.write_gif(f"{export_path}/{data["Name"]}.{data["Format"]}",remove_temp=True)
    else:
        clip.write_videofile(f"{export_path}/{data["Name"]}.{data["Format"]}",
                             codec=vid_codec[data["Format"]],audio_codec=audio_codec[data["Format"]],remove_temp=True)
    clip.close


def import_file():
    """selects a file to import

    :returns: data about imported file
    :rtype: list
    """
    file_path = filedialog.askopenfilenames()
    data = _fetch_data(file_path)
    return data


def export_file(data):
    """selects a path to export to and calls the respective save function

    :param list data: data from GUI
    """
    is_image = ("png","jpg","jpeg","bmp","webp","heic","tif")
    export_path = filedialog.askdirectory()
    try:
        if data["Format"] in is_image:
            _save_image(data,export_path)
        else:
            _save_video(data,export_path)
        os.startfile(export_path)
    except Exception:
        pass

