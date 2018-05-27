FROM chipgarner/opencv3-webcam:python2

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:mc3man/trusty-media && \
    apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    apt-get purge && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* 
    
    
CMD bash
