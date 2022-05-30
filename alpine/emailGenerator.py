import smtplib
import constants
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(stocks):
    stock = ""
    j=[]
    
    for i, x in stocks.iterrows():
        
        tempString="<li>"+x['symbol']+": "+str(x['analysis'])+"</li>"
        j.append(tempString)

    listStocks = stock.join(j)
    
    sender = constants.SENDER
    receiver = constants.RECIEVER
    psswd= constants.PSSWD

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Test Email"
    msg['From'] = sender
    msg['To'] = receiver
    
    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
        <h1> Here is the results of your analysis</h1>
                <h3>Buy or sell trades will be placed based on the results below.</h3>
                <ul>{0}</ul>  </body>
    </html>
    """.format(listStocks)
    
    
    # Record the MIME types of both parts - text/plain and text/html. 
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.  
    
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender,psswd)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()