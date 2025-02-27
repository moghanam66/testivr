import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

# Securely retrieve credentials
APP_ID = "b0a29017-ea3f-4697-aef7-0cb05979d16c"
APP_PASSWORD = "2fc8Q~YUZMbD8E7hEb4.vQoDFortq3Tvt~CLCcEQ"
# Configure the bot adapter with environment variables
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    if name:
        return render_template('hello.html', name=name)
    else:
        return redirect(url_for('index'))

@app.route('/api/messages', methods=['POST'])
def messages():
    body = request.json
    activity = Activity().deserialize(body)

    async def turn_logic(turn_context: TurnContext):
        await turn_context.send_activity(f"You said: {turn_context.activity.text}")
    
    return adapter.process_activity(activity, '', turn_logic)

if __name__ == '__main__':
    app.run(debug=True, port=3978)
