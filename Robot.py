import schedule
import time
import requests
import json


class Robot(object):

    def __init__(self, name='Robot', schedule=[]):
        self.name = name
        self.schedule = schedule

    def tell(self, webhook):
        self.webhook = webhook
        return self

    def when(self, time):
        self.time = time
        return self

    def do(self, something):
        self.schedule.append({'time': self.time, 'task': something})
        for i in self.schedule:
            if(self.time == i['time']):
                i['task'] = something
        return self

    def job(self, task):
        print(task)
        request = requests.session()
        url = self.webhook
        headers = {
            'Content-Type': 'application/json',
        }
        req = request.post(
            url,
            data=json.dumps(task),
            headers=headers
        )
        print(req.text)

    def start(self):
        print(self.name, self.schedule, self.webhook)

        for item in self.schedule:
            print(item['time'])
            schedule.every().day.at(item['time']).do(
                self.job, item['task']
            )


Atom = Robot('Atom')
Atom.tell(
    'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=*********'
).when('13:30').do(
    {
        'msgtype': "text",
        'text': {
                'content': 'Hello World From Python Robot 30🤖️'
        }
    }
).when('13:31').do(
    {
        'msgtype': "text",
        'text': {
                'content': 'Hello World From Python Robot 31🤖️'
        }
    }
).start()
while True:
    schedule.run_pending()
    time.sleep(1)
