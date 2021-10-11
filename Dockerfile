FROM ubuntu:latest

WORKDIR /gmod

RUN dpkg --add-architecture i386 \ 
&& apt-get update \
&& apt-get install -y wget \ 
&& apt-get install -y lib32gcc1 \
&& apt-get install -y lib32stdc++6

RUN wget http://media.steampowered.com/client/steamcmd_linux.tar.gz \
&& tar -xvzf steamcmd_linux.tar.gz

RUN ./steamcmd.sh +login anonymous +force_install_dir ./server +app_update 4020 +quit

WORKDIR /gmod/server

COPY workshop.lua garrysmod/lua/autorun/server

COPY server.cfg .

RUN ls garrysmod/lua/autorun
RUN cat server.cfg

ARG STEAM_AUTH_KEY
ARG STEAM_COLLECTION

RUN echo

CMD ["./srcds_run", "-game garrysmod -authkey", "$STEAM_AUTH_KEY", "+exec 'server.cfg' +host_workshop_collection", "$STEAM_COLLECTION", "+maxplayers 12 +map ttt_achievement_city_3 +gamemode terrortown"]
