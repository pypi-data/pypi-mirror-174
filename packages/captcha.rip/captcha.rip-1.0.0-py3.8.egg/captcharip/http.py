import httpx
import os, time, threading; os.system('clear');

class CaptchaRipUtilities():
      def __init__(self):
          self.startTime        = 0
          self.timerStart       = 0

      def startTimer(self) -> int:
          self.timerStart = 1
          while self.timerStart == 1:
                self.startTime  += 1; time.sleep(
                     1
                )
          return self.startTime

      def startTimerRaw(self) -> int:
          threading.Thread(target = self.startTimer).start(); return 1

      def endTimer(self) -> tuple:
          endTime         = self.startTime;
          self.timerStart = 0;
          return (
               endTime,
          )

class CaptchaRipException(Exception):
      def __init__(self, MESSAGE, DATA):
          self.MESSAGE                = MESSAGE  # Exception Message
          self.DATA                   = DATA     # Exception Data

      def __str__(self):
          return str(self.MESSAGE)

class CaptchaRip:
      def __init__(self, captcha_key: str = '') -> None:
          if captcha_key == '':
             raise CaptchaRipException (
                   'Missing Captcha Key',
                   'Missing Captcha Key Argument'
             )
            
          self.captcha_key     = captcha_key
          self.captcha_headers = {
               'authorization' : captcha_key
          }

      def getRawTaskResult(self, taskId) -> httpx.Response:
          return httpx.post(
                 'https://captcha.rip/api/fetch',
                  headers = {},
                  timeout = 10,
                  json    = {
                          'key' : self.captcha_key,
                          'id'  : taskId,
                  }
          )
        
      def getTaskResult(self, taskId, taskTimeout: int = 3.5) -> tuple:
          taskResponse = {}
          timerHandler = CaptchaRipUtilities()
          timerHandler.startTimerRaw()
          while True:
                if taskTimeout != 0: time.sleep(taskTimeout)
                try:
                   taskResponse = self.getRawTaskResult(taskId).json()
                   if taskResponse['message'] == 'Solved':
                      endTime = timerHandler.endTimer()
                      return (
                           taskResponse.json(),
                           endTime[0],
                      )
                except:
                   raise CaptchaRipException (
                         "JSON Structure Handling Error",
                         "JSON Structure Handling Error With Response"
                   )
                  
        
      def createFunCaptchaTask(
          self,
          public_url,
          public_key,
          service_url,
          blob: str = None,
          wait: int = None,
          proxy: str = '',
          agent: str = '',
      ) -> int:
          payload = {
                  'key'  : self.captcha_key,
                  'task' : {
                         'type'            : 'FunCaptchaTaskProxyless',
                         'site_url'        : public_url,
                         'public_key'      : public_key,
                         'service_url'     : service_url,
                  }
          }
        
          if blob: payload['task']['blob'] = blob
          if agent: payload['task']['user_agent'] = agent
          if proxy: 
             if len(proxy.split(':')) == 4:
                (
                   ip,
                   port,
                   username,
                   password,
                ) = proxy.split(':')
                payload['task']['type'] = 'FunCapthaTask'; (
                         payload['task']['username'],
                         payload['task']['password'],
                         payload['task']['ip'],
                         payload['task']['port']
                ) = username, password, ip, port
             else:
               raise CaptchaRipException (
                     "Proxy Type Unsupported",
                     "Given Proxy Type Unsupported",
               )

          try:
             response = httpx.post(
                        'https://captcha.rip/api/create',
                         headers = {},
                         timeout = 10,
                         json    = payload,
             )

             if response.status_code:
                return int(response.json().get('id'))
             return None
          except:     
             raise CaptchaRipException(
                   'Task ID Creation Error',
                   'Task ID Creation Malfunction || %s' % (response.text)
             )
             
      def getBalance(self, timeout: int = 10) -> dict:
          return httpx.get(
                 'https://captcha.rip/api/balance',
                  headers    = self.captcha_headers,
                  timeout    = 10,
          ).json()
