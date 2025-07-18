from typing import List, Union, Optional

IMG_JOBS = "https://static.divine-pride.net/images/jobs/icon_jobs_"


def job_icon(job: Union[int, str]) -> Optional[str]:
    if isinstance(job, int):
        return f"{IMG_JOBS}{job}.png"
    if isinstance(job, str) and job.isdigit():
        return f"{IMG_JOBS}{int(job)}.png"
    return None


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
    else:
        # Nenhuma classe especificada
        return {
            "allowed_classes": [],
            "class_icons": []
        }
