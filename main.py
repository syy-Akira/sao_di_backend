from datetime import date, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello syy! 你的后端跑起来啦!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "msg": "一切正常"}


class ScheduleRequest(BaseModel):
    members: list[str] = Field(min_length=1, max_length=500)
    start_date: date
    end_date: date


class ScheduleItem(BaseModel):
    date: date
    member: str


@app.post("/schedules/generate", response_model=list[ScheduleItem])
def generate_schedule(data: ScheduleRequest):
    members = [name.strip() for name in data.members]

    if any(not name for name in members):
        raise HTTPException(
            status_code=400,
            detail="成员姓名不能为空"
        )

    if len(set(members)) != len(members):
        raise HTTPException(
            status_code=400,
            detail="成员姓名不能重复"
        )

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="结束日期不能早于开始日期"
        )

    total_days = (data.end_date - data.start_date).days + 1

    schedules = []

    for i in range(total_days):
        current_date = data.start_date + timedelta(days=i)
        member = members[i % len(members)]

        schedules.append(
            ScheduleItem(
                date=current_date,
                member=member
            )
        )

    return schedules

