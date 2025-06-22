import requests
from dotenv import load_dotenv
import os

load_dotenv()

class MailSender:
    def __init__(self, address, to):
        self.address = address
        self.to = to
        self.fallback_text = "Tenderbot Notification - Type: "
    
    def _fallbackMsg(self,typeof,text):
        return self.fallback_text + typeof + "\n" + text
    
    def _HTMLMsg(self,typeof,text:str):
        banner = str()
        if typeof == "Notification":
            banner = '''
                    <div style="margin-left: 20px; margin-right: 20px; display: flex; align-items: center; justify-content: space-between; border-radius: 8px; background-color: #f3f4f6; padding-left: 20px">
                        <div style="font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; color: #000001">Type: </div>
                         <div style="margin: 0; border-top-right-radius: 8px; border-bottom-right-radius: 8px; background-color: #3b82f6; padding: 20px; font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; font-weight: 600; color: #fffffe">Notification</div>
                    </div>
                    '''
        elif typeof == "Warning":
            banner = '''
                    <div style="margin-left: 20px; margin-right: 20px; display: flex; align-items: center; justify-content: space-between; border-radius: 8px; background-color: #f3f4f6; padding-left: 20px">
                        <div style="font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; color: #000001">Type: </div>
                         <div style="margin: 0; border-top-right-radius: 8px; border-bottom-right-radius: 8px; background-color: #eab308; padding: 20px; font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; font-weight: 600; color: #fffffe">Warning</div>
                    </div>
                    '''
        elif typeof == "Error":
            banner = '''
                    <div style="margin-left: 20px; margin-right: 20px; display: flex; align-items: center; justify-content: space-between; border-radius: 8px; background-color: #f3f4f6; padding-left: 20px">
                        <div style="font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; color: #000001">Type: </div>
                         <div style="margin: 0; border-top-right-radius: 8px; border-bottom-right-radius: 8px; background-color: #ef4444; padding: 20px; font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; font-weight: 600; color: #fffffe">Error</div>
                    </div>
                    '''
        textDiv = '<div style="padding: 24px">\n'
        texts = text.split('\n')
        for i in texts:
            textDiv += f'<p style="margin-bottom: 16px; font-family: ui-sans-serif, system-ui, -apple-system, \'Segoe UI\', sans-serif; color: #000001">{i}</p>\n' 
        textDiv += '</div>\n'
        return banner + textDiv
    
    def SendMail(self,subject,typeof,message):
        text = self._fallbackMsg(typeof, message)
        html_body = self._HTMLMsg(typeof,message)
        whole_html = f'''
        <!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
  <meta charset="utf-8">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings xmlns:o="urn:schemas-microsoft-com:office:office">
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <style>
    td,th,div,p,a,h1,h2,h3,h4,h5,h6 {{font-family: "Segoe UI", sans-serif; mso-line-height-rule: exactly;}})
  </style>
  <![endif]-->
  <title>Tenderbot Notification</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet" media="screen">
</head>
<body style="margin: 0">
  <div role="article" aria-roledescription="email" aria-label="Tenderbot Notification" lang="en">
    <div style="margin-left: auto; margin-right: auto; width: 80%; border-radius: 8px; background-color: #fffffe; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)">
      <div style="margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; border-top-left-radius: 8px; border-top-right-radius: 8px; background-color: #fe3c72; padding: 20px">
        <h1 style="font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; font-size: 24px; font-weight: 700; color: #fffffe">Tenderbot Notification</h1>
      </div>
                    {html_body}
            </div>
        </html>
        '''
        resonse = requests.post(
            os.getenv("MAIL"),
            auth=("api", os.getenv("API")),
            data={
                "from": self.address,
                "to": self.to,
                "subject": subject,
                "text": text,
                "html": whole_html
            }
        )