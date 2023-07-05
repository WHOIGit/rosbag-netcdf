import bagpy

import pandas as pd

# to get lz4 support, you'll need to follow this SO post
# https://stackoverflow.com/q/58754968

# and on macOS, you'll need to install lz4 with brew first and then do this
# https://stackoverflow.com/a/70950162

# Read bag file
b = bagpy.bagreader('data/rosbags/example.bag')

# list available topics
print(b.topic_table)

# read a topic
gps_fix_messages = pd.read_csv(b.message_by_topic('/gps/fix'))

print(gps_fix_messages.head())