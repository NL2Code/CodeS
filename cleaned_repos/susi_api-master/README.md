# API for solved AI challenges

In the last years a lot of challenges in the area of text understanding, image
and speech recognition and generation has been solved. This project aims to
channel well-known solutions into one proxy-like API which can be accessed
from a client application easily. The purpose of this approach is to replace
these proxy functions with on-site hosted AI functions.
The recent achievements in transformer models for the named function gives the
perspective that this is doable in the near future.

## API Design

To create a properly structured and well-named API we clone API defitions from
existing providers. To give different implementations a good structure, we
distinguish the challenge fields:

- text
- audio
- image
- video

More fields may arise in the future if these topics are fully covered with AI
functions and more challenging targets become into sight. Even if an
exponential growth in the named topics become vertical, new topics may appear
which have not yet reached human-level AI abilities.

To be able to have an easier approach to test the AI functions we also
provide a drop-in replacement to OpenAI API functions. Therefore we
re-implement specific OpenAI API endpoints as well.

## Integration into SUSI

SUSI (the new SUSI) will use this API as intelligent back-end. Since the
beginning of the SUSI project it was a target to bring all functions to a
RaspberryPi device "which could be used on Mars".
The final product should work completely offline.

During the first phase of the SUSI project until 2021 the biggest challenge was
on-device speech recognition. It looks like this is now possible. This project
therefore shall bootstrap a second SUSI development phase where we can build
upon now-existing technology.