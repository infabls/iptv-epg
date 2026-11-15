"""Вырезает из большого XMLTV только каналы из channels.txt.

Запуск: python -I filter_epg.py SRC.xml.gz channels.txt OUT.xml.gz
channels.txt: одна строка на канал, "имя в плейлисте" или "имя в плейлисте|имя в EPG".
В выходной канал добавляется display-name с именем из плейлиста: по нему TiviMate
сопоставляет программу с каналом (tvg-id в плейлисте нет).
"""
import gzip
import sys
import xml.etree.ElementTree as ET

src, chan_file, out = sys.argv[1:4]

want = {}  # имя EPG (lower) -> имя в плейлисте
for line in open(chan_file, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = [p.strip() for p in line.split("|")]
    want[(parts[1] if len(parts) > 1 else parts[0]).lower()] = parts[0]

keep = {}  # id канала -> имя в плейлисте
channels, programmes = [], []
with gzip.open(src, "rb") as f:
    for _, el in ET.iterparse(f, events=("end",)):
        if el.tag == "channel":
            for dn in el.findall("display-name"):
                name = (dn.text or "").strip().lower()
                if name in want and el.get("id") not in keep:
                    pl = want[name]
                    keep[el.get("id")] = pl
                    if all((d.text or "").strip() != pl for d in el.findall("display-name")):
                        ET.SubElement(el, "display-name").text = pl
                    channels.append(el)
                    break
            else:
                el.clear()
        elif el.tag == "programme":
            if el.get("channel") in keep:
                programmes.append(el)
            else:
                el.clear()

root = ET.Element("tv")
root.extend(channels)
root.extend(programmes)
with gzip.open(out, "wb") as f:
    ET.ElementTree(root).write(f, encoding="utf-8", xml_declaration=True)

found = set(keep.values())
missing = sorted(set(want.values()) - found)
print(f"channels {len(channels)}, programmes {len(programmes)}")
print("not found:", "; ".join(missing) if missing else "-")
