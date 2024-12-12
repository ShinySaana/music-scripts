#!/usr/bin/env python3

import os
import subprocess
import sys

import requests

def get_mb_session():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    s.headers.update({"User-Agent": "Saana's music scripts"})
    return s

def get_url(suffix: str):
    return f"https://musicbrainz.org/ws/2{suffix}"

def get_release(session, id: str):
    r = session.get(get_url(f"/release/{id}?inc=recordings+artist-credits+artists"))
    return r.json()

def get_tracks_from_release(session, release_id: str):
    release = get_release(session, release_id)
    
    tracks = []

    for media in release["media"]:
        if media["format"] == "DVD":
            continue

        for track in media["tracks"]:
            tracks.append({
                "track_id": track["id"],
                "recording_id": track["recording"]["id"],
                "title": track["recording"]["title"],
                
                "track_number": track["position"],
                "disk_number": media["position"],

                "album": release["title"],
                "album_id": release["id"],
            })

    tracks = sorted(tracks, key=lambda track: (track["disk_number"], track["track_number"]))

    return tracks

def list_files(directory):
    files = [os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    files = [entry for entry in files if entry.endswith('.flac')]
    return sorted(files)

def get_kid3_command(tag, value, path):
    kid3_cli_set_tag = "kid3-cli -c \"set '{tag}' '{value}' 2\" \"{path}\""
    return kid3_cli_set_tag.format(
        tag=tag,
        value=value,
        path=path,
    )

def generate_kid3_commands(files, tracks):
    if len(tracks) != len(files):
        print("Number of tracks from release: {}".format(len(tracks)))
        print("Number of files: {}".format(len(files)))
        print("Mismatched number of files and tracks.")
        exit(1)

    commands = []
    for index in range(len(files)):
        file = files[index]
        track = tracks[index]

        file_escaped = file.replace('"', r'\"')
        title = track["title"].replace("'", r"\'")
        album = track["album"].replace("'", r"\'")

        commands.append(get_kid3_command("title", title, file_escaped))
        commands.append(get_kid3_command("album", album, file_escaped))

        commands.append(get_kid3_command("tracknumber", track["track_number"], file_escaped))
        commands.append(get_kid3_command("discnumber", track["disk_number"], file_escaped))

        commands.append(get_kid3_command("MUSICBRAINZ_RELEASETRACKID", track["track_id"], file_escaped))
        commands.append(get_kid3_command("MUSICBRAINZ_TRACKID", track["recording_id"], file_escaped))
        commands.append(get_kid3_command("MUSICBRAINZ_ALBUMID", track["album_id"], file_escaped))
    return commands

def execute_commands(commands):
    for command in commands:
        print(command)
        subprocess.call(command, shell=True, executable='/bin/bash')


directory_path = sys.argv[1]
release_id = sys.argv[2]
session = get_mb_session()

tracks = get_tracks_from_release(session, release_id)

execute_commands(generate_kid3_commands(list_files(directory_path), tracks))

