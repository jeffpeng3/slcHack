from aiohttp import request
from dataclasses import dataclass
from fastapi.responses import FileResponse
import qrcode
from fastapi import FastAPI
base_url = "https://slc.ctld.ntust.edu.tw/rest/council/common/bookings/pager"

@dataclass
class User:
    uuid: str
    name: str
    user_id: str

@dataclass
class Book_Info:
    place: str
    creator: User
    create_date: str
    Participants: list[User]
    booking_end_date: str
    booking_start_date: str

def parse_user_data(data:dict) -> User:
    if 'participantName' in data:
        user_name:str = data['participantName']
        user_id:str = data['participantAccount']
        user_uuid:str = data['pid']
    else:
        user_name:str = data['creatorName']
        user_id:str = data['hostAccount']
        user_uuid:str = data['creatorId']
    return User(user_uuid, user_name, user_id)

def parse_book_data(data:dict):
    creator:User = parse_user_data(data)
    Participants:list[User] = []
    for Participant in data['bookingParticipants']:
        Participants.append(parse_user_data(Participant))
    create_date:str = data['createDate']
    booking_end_date:str = data['bookingEndDate']
    booking_start_date:str = data['bookingStartDate']
    resource = data['mainResourceName']
    return Book_Info(resource,creator, create_date, Participants, booking_end_date, booking_start_date)

app = FastAPI()

@app.get('/')
async def booking_info():
    async with request('GET',base_url) as resp:
        jdata = await resp.json()
    results = jdata['resultList']
    bookings = []
    for result in results:
        booking_info = parse_book_data(result)
        bookings.append(booking_info)
    return bookings

@app.get('/{uid}')
async def get_qr_code(uid:str):
    if uid == 'favicon.ico':
        return ""
    qr = qrcode.make(uid)
    file_name = f'{uid}_qrcode.png'
    qr.save(file_name)
    return FileResponse(file_name)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)