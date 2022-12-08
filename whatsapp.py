from heyoo import WhatsApp
import logging
import requests
from dotenv import load_dotenv
from flask import Flask, request, make_response



app = Flask(__name__)
token = 'EAAVk5rqOCsABAOC3EvCx9VoHclZAVqbMkP8ptWiUG5EsbC2nZALFZBhJUhU6jATXVMalxmvv3yIZA8smhr5kZBVfDqjGLEcZCzg4pR51RrF3WcPzbbYQ6pY9bAbTtLXBKIXpvag42Vhxplq4RJSE7QsY4yz6PgDNS887sIF0ZARZA622i1XEBZAWiydA2cDPZBeg4XS5o8CV7UmHkjRG8lDWIIlon9trRnt4YZD'
messenger = WhatsApp(token,  phone_number_id='100398242927044')

messenger.send_message('Hey its Jahansher ', '13477037561')


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

print("hello")

@app.route("/hook", methods=["GET", "POST"])



def hook():
    print("okiee")

    if request.method == "GET":
        if request.args.get("hub.verify_token") == token:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            print(mobile)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

    return "ok"

if __name__ == "__main__":
    app.run(port=5000, debug=True)

