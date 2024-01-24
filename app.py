from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='9yru8c5MZs7qC8rNA0LbfXPWvWjbwPaD9OKAggK/nrHIHkJ4bRy4rC+L6ClqN9Jcbdt2wscu1mlhyWbxTy8v19UvvkiON38wyrL9lsGVonXmFJXXIuDyQbq53eV0b2y/w45EiR7PbJX9QsNNw/ascgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d9a8a0024fd010f5367d0d5ee5e23e98')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="Hi")]
            )
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)