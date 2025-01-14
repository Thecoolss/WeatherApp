import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton
from PyQt5.QtCore import Qt

class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,400,200)
        self.enterlabel=QLabel("Enter a city:",self)
        self.input=QLineEdit(self)
        self.button=QPushButton("Get Weather",self)
        self.templabel=QLabel(self)
        self.emojilabel=QLabel(self)
        self.desclabel=QLabel(self)
        
        self.initUI()
        
    def initUI(self):
        vbox=QVBoxLayout()
        vbox.addWidget(self.enterlabel)
        vbox.addWidget(self.input)
        vbox.addWidget(self.button)
        vbox.addWidget(self.templabel)
        vbox.addWidget(self.emojilabel)
        vbox.addWidget(self.desclabel)
        self.setLayout(vbox)
        
        self.enterlabel.setAlignment(Qt.AlignCenter)
        self.templabel.setAlignment(Qt.AlignCenter)
        self.emojilabel.setAlignment(Qt.AlignCenter)
        self.desclabel.setAlignment(Qt.AlignCenter)
        #self.input.setAlignment(Qt.AlignCenter)
        #self.button.setAlignment(Qt.AlignCenter)
        
        self.enterlabel.setObjectName("enterlabel")
        self.templabel.setObjectName("templabel")
        self.emojilabel.setObjectName("emojilabel")
        self.desclabel.setObjectName("desclabel")
        self.input.setObjectName("input")
        self.button.setObjectName("button")
        
        self.setStyleSheet("""
                          QPushButton,QLable{
                              font-family:Arial; 
                           }
                           
                          QPushButton#button{
                          font-size:30px;
                          padding:5px;
                          font-weight:bold;
                          }
                          QLineEdit{
                              font-size:30px;
                              padding:4px;
                              }
                          QLabel#enterlabel{
                              font-size:30px;
                              }
                          QLabel#templabel{
                          font-size:100px;
                          }
                          QLabel#emojilabel{
                          font-size:100px;
                          font-family:Segoe UI emoji;
                          }
                          QLabel#desclabel{
                          font-size:50px;
                          }
                           """)
        self.button.clicked.connect(self.getweather)
        
       
        
    def getweather(self):
        api="e5410b26ae839e1379ed58e5129ff4eb"
        city=self.input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
            
        try:
            response=requests.get(url)
            response.raise_for_status()
            info=response.json()
                
            if info["cod"]==200:
              self.displayweather(info)
        except requests.exceptions.HTTPError as http_error:
               match response.status_code:
                    case 400:
                        self.displayerror("Bad RequestError\n Check your input!")
                    case 401:
                        self.displayerror("Unauthorized\nBad API Key!")
                    case 403:
                        self.displayerror("Forbidden Error\nDenied Access!")
                    case 404:
                        self.displayerror("Request Not Found\nCity Not Found!")
                    case 500:
                        self.displayerror("Internal Server Error\nPlease Try Again Later!")
                    case 502:
                        self.displayerror("Bad Gateway\nInvalid Response From The Server!")
                    case 503:
                       self.displayerror("Service Unavailable\nServer Has Problems!")
                    case 504:
                        self.displayerror("Gateway Timeout\nNo Response From The Server!")
                    case _:
                        self.displayerror(f"HTTP Error Occured {http_error}")
        except requests.exceptions.RequestException as request_error:
            self.displayerror(f"Request Error\n {request_error}!")
        except requests.exceptions.ConnectionError:
            self.displayerror("Connection Error\n Check Your Internet Connection!")
        except requests.exceptions.Timeout:
            self.displayerror("Timeout Error\n The Request Timed Out!")
        except requests.exceptions.TooManyRedirects:
            self.displayerror("Too Many Requests\n Check The URL!")  
    
    
    def displayweather(self,info):
        self.templabel.setStyleSheet("font-size:50px;")
        tempk=info["main"]["temp"]
        tempcel=tempk-273.15
        tempf=(tempk*9/5)-459.67
        
        weatherid=info["weather"][0]["id"]
        weatherdesc=info["weather"][0]["description"]
         
        self.templabel.setText(f"{tempcel:.0f}°C\n{tempf:.0f}°F")
        self.desclabel.setText(weatherdesc)
        self.emojilabel.setText(self.getemoji(weatherid))
        
    def displayerror(self,msg):
        self.templabel.setStyleSheet("font-size:30px;")
        self.emojilabel.clear()
        self.templabel.setText(msg)
        self.desclabel.clear()
        
    @staticmethod    
    def getemoji(wid):
        if 200<=wid<=232:
           return "⛈️"
        elif 300<=wid<=321:
           return "⛅"
        elif 500<=wid<=531:
           return "🌧️"
        elif 600<=wid<=622:
            return "🌨❄️"
        elif 701<=wid<=741:
            return "🌫️"
        elif wid==762:
            return "🌋"
        elif wid==771:
            return "💨"
        elif wid==781:
            return "🌪️"
        elif wid==800:
            return "☀️"
        elif 801<=wid<=804:
            return "☁️"
        else:
            return ""
app=QApplication(sys.argv)
weatherapp=Weatherapp()
weatherapp.show()
sys.exit(app.exec_())
