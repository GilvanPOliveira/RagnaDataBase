from typing import List, Union, Optional

IMG_JOBS = "https://static.divine-pride.net/images/jobs/icon_jobs_"

# Mapa completo nome → ID das 82 classes
JOB_NAME_TO_ID = {
    "novice": 0,
    "super novice": 23,
    "super novice ex": 4307,
    "swordman": 1,
    "knight": 7,
    "lord knight": 4002,
    "rune knight": 4008,
    "rune knight ex": 4054,
    "royal guard": 4015,
    "royal guard ex": 4066,
    "imperial guard": 4252,
    "divine guard": 4258,
    "magician": 2,
    "wizard": 9,
    "sorcerer": 4003,
    "archmage": 4010,
    "archmage ex": 4055,
    "elemental master": 4255,
    "enchanter": 4261,
    "archer": 3,
    "hunter": 11,
    "ranger": 4004,
    "windhawk": 4012,
    "windhawk ex": 4056,
    "troubadour": 4020,
    "trouvere": 4021,
    "minstrel": 4068,
    "maestro": 4263,
    "maestrina": 4264,
    "acolyte": 4,
    "priest": 8,
    "archbishop": 4005,
    "archbishop ex": 4057,
    "cardinal": 4256,
    "monk": 15,
    "champion": 4009,
    "shura": 4016,
    "shura ex": 4070,
    "supreme shura": 4262,
    "merchant": 5,
    "blacksmith": 10,
    "mastersmith": 4006,
    "mechanic": 4011,
    "mechanic ex": 4058,
    "master mechanic": 4253,
    "alchemist": 18,
    "creator": 4019,
    "biochemist": 4071,
    "genetic": 4259,
    "thief": 6,
    "assassin": 12,
    "guillotine cross": 4007,
    "shadow cross": 4013,
    "shadow cross ex": 4059,
    "executor": 4254,
    "rogue": 17,
    "shadow chaser": 4018,
    "abyss chaser": 4072,
    "master chaser": 4260,
    "taekwon kid": 4046,
    "taekwon master": 4047,
    "star emperor": 4239,
    "sky emperor": 4302,
    "soul linker": 4049,
    "soul reaper": 4240,
    "soul ascetic": 4303,
    "ninja": 25,
    "kagerou": 4211,
    "oboro": 4212,
    "imperial kagerou": 4304,
    "imperial oboro": 4305,
    "gunslinger": 24,
    "rebellion": 4215,
    "peacemaker": 4306,
    "doram": 4218,
    "doramic": 4308
}


def job_icon(job: Union[int, str]) -> Optional[str]:
    if isinstance(job, int):
        return f"{IMG_JOBS}{job}.png"
    jid = JOB_NAME_TO_ID.get(str(job).lower())
    return f"{IMG_JOBS}{jid}.png" if jid is not None else None


def extract_allowed_classes(raw_jobs: Optional[List[Union[int, str]]]) -> dict:
    if raw_jobs:
        allowed_classes = [
            int(j) if isinstance(j, str) and j.isdigit() else j
            for j in raw_jobs
            if isinstance(j, (int, str))
        ]
        icons = [job_icon(j) for j in allowed_classes if job_icon(j)]
        return {
            "allowed_classes": allowed_classes,
            "class_icons": icons
        }
    return {
        "allowed_classes": [],
        "class_icons": []
    }
