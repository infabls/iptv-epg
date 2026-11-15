# iptv-epg

Лёгкая телепрограмма (XMLTV) только для каналов из `channels.txt`: вырезка из `epg.one`,
обновляется раз в сутки через GitHub Actions. Адрес для TiviMate после включения Pages:
`https://infabls.github.io/iptv-epg/epg.xml.gz`.

Локально: `python -I filter_epg.py src.xml.gz channels.txt docs/epg.xml.gz`.
