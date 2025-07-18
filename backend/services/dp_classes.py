from typing import List, Union, Optional
import re

IMG_JOBS = "https://static.divine-pride.net/images/jobs/icon_jobs_"

JOB_NAME_TO_ID = {
    "novice": 0,
    "swordman": 10,
    "knight": 20,
    "crusader": 21,
    "mage": 20,
    "wizard": 21,
    "archer": 30,
    "hunter": 31,
    "thief": 40,
    "assassin": 41,
    "merchant": 50,
    "blacksmith": 51,
    "acolyte": 60,
    "priest": 61,
    "soul linker": 68,
    "ninja": 69,
    "gunner": 70,
    "taekwon": 71,
    # Expandir lista para todos os jobs que você precisa!
}

def job_icon(job: Union[int, str]) -> Optional[str]:
    if isinstance(job, int):
        return f"{IMG_JOBS}{job}.png"
    if isinstance(job, str):
        if job.isdigit():
            return f"{IMG_JOBS}{int(job)}.png"
        jid = JOB_NAME_TO_ID.get(job.lower())
        if jid is not None:
            return f"{IMG_JOBS}{jid}.png"
    return None

def extract_allowed_classes(raw_jobs: Optional[List[Union[int, str]]]) -> dict:
    allowed_classes = []
    icons = []
    for j in raw_jobs or []:
        if isinstance(j, int) or (isinstance(j, str) and j.isdigit()):
            jid = int(j)
            allowed_classes.append(jid)
            icon_url = job_icon(jid)
            if icon_url:
                icons.append(icon_url)
        elif isinstance(j, str):
            jid = JOB_NAME_TO_ID.get(j.lower())
            if jid is not None:
                allowed_classes.append(jid)
                icon_url = job_icon(jid)
                if icon_url:
                    icons.append(icon_url)
    return {
        "allowed_classes": allowed_classes,
        "class_icons": icons
    }

def parse_jobs_from_description(desc: str) -> List[str]:
    """
    Extrai nomes de jobs a partir da descrição de item como:
    ... Usable By: ^808080Swordman Jobs, Merchant Jobs, Thief Jobs^000000
    """
    # Tira códigos de cor e \n:
    clean_desc = re.sub(r"\^(?:[0-9a-fA-F]{6})", "", desc).replace("\n", " ")
    match = re.search(r"Usable By:\s*([^\^]+)", clean_desc)
    if not match:
        return []
    jobs_str = match.group(1)
    # Quebra por vírgula e remove "Jobs"
    jobs = [j.strip().replace(" Jobs", "").replace(" Job", "") for j in jobs_str.split(",")]
    # Remove entradas como "All" e vazias
    jobs = [j for j in jobs if j and not j.lower().startswith("all")]
    return jobs
