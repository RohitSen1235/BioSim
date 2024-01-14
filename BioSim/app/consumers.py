# consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.consumer import AsyncConsumer
from celery.result import AsyncResult

class LongRunningTaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connected to websocket")
        await self.accept()
        await self.send(json.dumps({
            # 'type':'websocket.accept',
            'text':'Hello World ws://',
            })
        )

    # async def disconnect(self, close_code):
    #     print(f"Disconnected from websocket")
    #     await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        task_id = text_data_json["task_id"]

        while True:
            task = AsyncResult(task_id)
            status = task.status
            await asyncio.sleep(1)
            await self.send(text_data=json.dumps({"status": status}))
            if status == "SUCCESS":
                await self.close()
                break
        return  

            


class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({
            'type':'websocket.accept',
            'text':'Hello World!!!',
        }))
