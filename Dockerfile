FROM ros:noetic

RUN apt update && apt install -y ros-noetic-rosbag-pandas

CMD tail -f /dev/null
