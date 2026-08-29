import json,base64,io,os,glob,csv,subprocess,sys
from PIL import Image, ExifTags
import pillow_heif, imageio_ffmpeg
pillow_heif.register_heif_opener()
FF=imageio_ffmpeg.get_ffmpeg_exe()
TR="/root/.claude/projects/-home-user-Yina-Belt-OS/d84fea99-2c30-54dd-91bc-083362e17840/tool-results"
OUT="/tmp/claude-0/-home-user-Yina-Belt-OS/d84fea99-2c30-54dd-91bc-083362e17840/scratchpad/exif/rows.csv"

rows={}
if os.path.exists(OUT):
    for r in csv.DictReader(open(OUT)): rows[r["title"]]=r

def probe_video(raw):
    p="/tmp/v.mov"; open(p,"wb").write(raw)
    try:
        o=subprocess.run([FF,"-i",p],capture_output=True,text=True,timeout=120).stderr
    finally:
        os.remove(p)
    ct=dur=model=""
    for line in o.splitlines():
        s=line.strip()
        if s.startswith("creation_time") and not ct: ct=s.split(":",1)[1].strip()
        if s.startswith("model") and not model: model=s.split(":",1)[1].strip()
        if "Duration:" in s and not dur: dur=s.split("Duration:")[1].split(",")[0].strip()
    return ct,dur,model

n=0
for f in glob.glob(TR+"/mcp-Google_Drive-download_file_content-*.txt"):
    try: d=json.load(open(f))
    except Exception: continue
    t=d.get("title");
    if not t or t in rows: continue
    raw=base64.b64decode(d["content"]); n+=1
    rec={"title":t,"id":d.get("id"),"bytes":len(raw),"captured":"","model":"","dims":"","dur":"","gps":""}
    try:
        if d.get("mimeType","").startswith("video"):
            ct,dur,model=probe_video(raw)
            rec["captured"]=ct.replace("T"," ").replace("Z","")[:19]; rec["dur"]=dur; rec["model"]=model
        else:
            im=Image.open(io.BytesIO(raw)); ex=im.getexif()
            tg={ExifTags.TAGS.get(k,k):v for k,v in ex.items()}
            sub={ExifTags.TAGS.get(k,k):v for k,v in ex.get_ifd(0x8769).items()}
            dt=sub.get("DateTimeOriginal") or tg.get("DateTime") or ""
            rec["captured"]=str(dt).replace(":","-",2)
            rec["model"]=f"{tg.get('Make','') or ''} {tg.get('Model','') or ''}".strip()
            rec["dims"]=f"{im.size[0]}x{im.size[1]}"
            rec["gps"]="yes" if ex.get_ifd(0x8825) else ""
    except Exception as e:
        rec["captured"]=f"ERR {type(e).__name__}"
    rows[t]=rec

w=csv.DictWriter(open(OUT,"w",newline=""),fieldnames=["title","id","bytes","captured","model","dims","dur","gps"])
w.writeheader()
for t in sorted(rows): w.writerow(rows[t])
print(f"parsed {n} new; total {len(rows)}")
