from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1334902534447435797/f8Bk814bA_YYfuvU2oxRWE7SDqi5JTgInPJabpoykQgKCIYWRcMoNF-Lr75tSQMOo0qA"

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Valentine's Proposal</title>
        <style>
            body {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: pink;
                font-family: Arial, sans-serif;
                overflow: hidden;
                position: relative;
            }
            h1 {
                color: red;
                text-align: center;
            }
            .buttons {
                position: relative;
                margin-top: 20px;
                width: 200px;
                height: 100px;
            }
            button {
                font-size: 18px;
                padding: 10px 20px;
                margin: 10px;
                border: none;
                cursor: pointer;
                border-radius: 10px;
                position: absolute;
            }
            #yes {
                background-color: lightgreen;
                left: 50px;
                top: 30px;
            }
            #no {
                background-color: lightcoral;
                left: 120px;
                top: 30px;
            }
            .popup {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1 id="question">Will you be my Valentine? ❤️</h1>
        <div class="buttons">
            <button id="yes" onclick="sendYesResponse()">Yes</button>
            <button id="no" onmouseover="moveButton()">No</button>
        </div>

        <div id="popup" class="popup">
            <p>Okay, I'll pick you up at 2 PM! ❤️</p>
            <button onclick="closePopup()">Close</button>
        </div>

        <div id="noPopup" class="popup">
            <p>Haha, you can't say no! 😆</p>
            <button onclick="closeNoPopup()">Close</button>
        </div>

        <script>
            function sendYesResponse() {
                fetch('/send_message', {
                    method: 'POST',
                    body: JSON.stringify({ message: 'someone said yes' }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    document.getElementById("popup").style.display = "block";
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }

            function closePopup() {
                document.getElementById("popup").style.display = "none";
            }

            function closeNoPopup() {
                document.getElementById("noPopup").style.display = "none";
            }

            function moveButton() {
                var noButton = document.getElementById("no");
                var yesButton = document.getElementById("yes");

                var yesButtonRect = yesButton.getBoundingClientRect();

                var minX = yesButtonRect.left - 50;
                var maxX = yesButtonRect.left + yesButtonRect.width + 50;
                var minY = yesButtonRect.top - 50;
                var maxY = yesButtonRect.top + yesButtonRect.height + 50;

                var x = Math.random() * (maxX - minX) + minX;
                var y = Math.random() * (maxY - minY) + minY;

                var bodyRect = document.body.getBoundingClientRect();
                x = Math.max(minX, Math.min(x, bodyRect.width - noButton.offsetWidth - 20));
                y = Math.max(minY, Math.min(y, bodyRect.height - noButton.offsetHeight - 20));

                noButton.style.left = `${x}px`;
                noButton.style.top = `${y}px`;
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get("message", "")

    # Send the message to Discord webhook
    payload = {"content": message}
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        return {"status": "success", "message": "Message sent to Discord!"}
    else:
        return {"status": "error", "message": "Failed to send message to Discord."}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
