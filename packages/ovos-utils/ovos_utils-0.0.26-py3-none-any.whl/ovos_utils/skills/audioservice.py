# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# This file is directly copied from HolmesV, it's a simple utility to
# interface with the AudioService via messagebus outside core
from os.path import abspath
from datetime import timedelta
from ovos_utils.messagebus import Message, get_mycroft_bus


def ensure_uri(s):
    """Interprete paths as file:// uri's.

    Args:
        s: string to be checked

    Returns:
        if s is uri, s is returned otherwise file:// is prepended
    """
    if isinstance(s, str):
        if '://' not in s:
            return 'file://' + abspath(s)
        else:
            return s
    elif isinstance(s, (tuple, list)):
        if '://' not in s[0]:
            return 'file://' + abspath(s[0]), s[1]
        else:
            return s
    else:
        raise ValueError('Invalid track')


class AudioServiceInterface:
    """AudioService class for interacting with the audio subsystem

    Args:
        bus: Mycroft messagebus connection
    """

    def __init__(self, bus=None):
        self.bus = bus or get_mycroft_bus()

    def queue(self, tracks=None):
        """Queue up a track to playing playlist.

        Args:
            tracks: track uri or list of track uri's
                    Each track can be added as a tuple with (uri, mime)
                    to give a hint of the mime type to the system
        """
        tracks = tracks or []
        if isinstance(tracks, (str, tuple)):
            tracks = [tracks]
        elif not isinstance(tracks, list):
            raise ValueError
        tracks = [ensure_uri(t) for t in tracks]
        self.bus.emit(Message('mycroft.audio.service.queue',
                              data={'tracks': tracks}))

    def play(self, tracks=None, utterance=None, repeat=None):
        """Start playback.

        Args:
            tracks: track uri or list of track uri's
                    Each track can be added as a tuple with (uri, mime)
                    to give a hint of the mime type to the system
            utterance: forward utterance for further processing by the
                        audio service.
            repeat: if the playback should be looped
        """
        repeat = repeat or False
        tracks = tracks or []
        utterance = utterance or ''
        if isinstance(tracks, (str, tuple)):
            tracks = [tracks]
        elif not isinstance(tracks, list):
            raise ValueError
        tracks = [ensure_uri(t) for t in tracks]
        self.bus.emit(Message('mycroft.audio.service.play',
                              data={'tracks': tracks,
                                    'utterance': utterance,
                                    'repeat': repeat}))

    def stop(self):
        """Stop the track."""
        self.bus.emit(Message('mycroft.audio.service.stop'))

    def next(self):
        """Change to next track."""
        self.bus.emit(Message('mycroft.audio.service.next'))

    def prev(self):
        """Change to previous track."""
        self.bus.emit(Message('mycroft.audio.service.prev'))

    def pause(self):
        """Pause playback."""
        self.bus.emit(Message('mycroft.audio.service.pause'))

    def resume(self):
        """Resume paused playback."""
        self.bus.emit(Message('mycroft.audio.service.resume'))

    def get_track_length(self):
        """
        getting the duration of the audio in seconds
        """
        length = 0
        info = self.bus.wait_for_response(
            Message('mycroft.audio.service.get_track_length'),
            timeout=1)
        if info:
            length = info.data.get("length") or 0
        return length / 1000  # convert to seconds

    def get_track_position(self):
        """
        get current position in seconds
        """
        pos = 0
        info = self.bus.wait_for_response(
            Message('mycroft.audio.service.get_track_position'),
            timeout=1)
        if info:
            pos = info.data.get("position") or 0
        return pos / 1000  # convert to seconds

    def set_track_position(self, seconds):
        """Seek X seconds.

        Arguments:
            seconds (int): number of seconds to seek, if negative rewind
        """
        self.bus.emit(Message('mycroft.audio.service.set_track_position',
                              {"position": seconds * 1000}))  # convert to ms

    def seek(self, seconds=1):
        """Seek X seconds.

        Args:
            seconds (int): number of seconds to seek, if negative rewind
        """
        if isinstance(seconds, timedelta):
            seconds = seconds.total_seconds()
        if seconds < 0:
            self.seek_backward(abs(seconds))
        else:
            self.seek_forward(seconds)

    def seek_forward(self, seconds=1):
        """Skip ahead X seconds.

        Args:
            seconds (int): number of seconds to skip
        """
        if isinstance(seconds, timedelta):
            seconds = seconds.total_seconds()
        self.bus.emit(Message('mycroft.audio.service.seek_forward',
                              {"seconds": seconds}))

    def seek_backward(self, seconds=1):
        """Rewind X seconds

         Args:
            seconds (int): number of seconds to rewind
        """
        if isinstance(seconds, timedelta):
            seconds = seconds.total_seconds()
        self.bus.emit(Message('mycroft.audio.service.seek_backward',
                              {"seconds": seconds}))

    def track_info(self):
        """Request information of current playing track.

        Returns:
            Dict with track info.
        """
        info = self.bus.wait_for_response(
            Message('mycroft.audio.service.track_info'),
            reply_type='mycroft.audio.service.track_info_reply',
            timeout=1)
        return info.data if info else {}

    def available_backends(self):
        """Return available audio backends.

        Returns:
            dict with backend names as keys
        """
        msg = Message('mycroft.audio.service.list_backends')
        response = self.bus.wait_for_response(msg)
        return response.data if response else {}

    @property
    def is_playing(self):
        """True if the audioservice is playing, else False."""
        return self.track_info() != {}
