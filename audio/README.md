# Sound notes

The default raspberry pi audio output is aweful ( although could be used in a pinch )

We have a USB audio device ( beheinger ) which is pretty powerful and sounds good

After you plug it in, remember to change the default audio device to usb. That's done by moving the 
asound.conf that's here into /etc . You might want to check that everything's quite alright,
which can be done by `aplay -l` which lists devices, then you can make sure the usb device
is at position 1 where it should be.

Also, with some devices the audio output is very low. There is a "volume" shell here that raises it to
80% which is at least enough to do what you're trying to do.


# WARNING

This audio directory should be read from the Google Drive.
