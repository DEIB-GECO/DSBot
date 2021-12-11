import threading
from functools import partial
import asyncio

from flask import Flask, jsonify, request, send_file, session
from flask_cors import CORS
from flask_restful import reqparse

from ir.ir import create_IR, run
from comprehension.summary_producer import summary_producer
from comprehension.comprehension_conversation_handler import comprehension_conversation_handler
from log_helpers import setup_logger
from main import Dataset
from needleman_wunsch import NW
from kb import KnowledgeBase
import os
import pandas as pd
import base64
from flask.sessions import SecureCookieSessionInterface

from tuning import get_framework
import flask
from flask import Blueprint, render_template
from flask import Flask, session, request
from flask_session import Session
from flask_socketio import SocketIO, emit, disconnect
import utils

base_url = '/inspire/'
socketio_path = 'socket.io/'

setup_logger()

app = Flask(__name__)

cors = CORS(app, supports_credentials=True)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
Session(app)

session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
data = {}
session_id = None
sio = SocketIO(app,
               manage_session=False,
               cors_allowed_origins='http://localhost:3000',
               async_mode="gevent",
               path=socketio_path,
               logger=False,
               engineio_logger=False,
               debug=False)

message_queue = utils.MessageContainer()
dataset = None
simple_page = Blueprint('root_pages',
                        __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')

@app.route('/receiveds', methods=['POST'])
def receive_ds():
    global dataset
    global session_id
    session_id = session_serializer.dumps(dict(session))
    data[session_id] = {}
    has_index = 0 if request.form['has_index'] == 'true' else None
    has_columns_name = 0 if request.form['has_column_names'] == 'true' else None
    sep = request.form['separator']
    label = request.form['label']
    uploaded_file = request.files['ds']
    if uploaded_file.filename != '':
        try:
            os.makedirs('./temp/temp_' + str(session_id))
        except:
            pass
        uploaded_file.save('./temp/temp_' + str(session_id) + '/' + uploaded_file.filename)
        dataset = pd.read_csv('./temp/temp_' + str(session_id) + '/' + str(uploaded_file.filename),
                              header=has_columns_name, index_col=has_index, sep=sep, engine='python')
        dataset.to_csv('./temp/temp_' + str(session_id) + '/' + uploaded_file.filename)
        dataset = Dataset(dataset)
        dataset.session = session_id
        print(label)

        if label is not None and label != '':
            dataset.set_label(label)
            print('dslabel', dataset.label, dataset.hasLabel)
        dataset.set_characteristics()
        kb = KnowledgeBase()
        kb.kb = dataset.filter_kb(kb.kb)
        data[session_id]['kb'] = kb
        data[session_id]['dataset'] = dataset

    print("SESSION ID", session_id)
    return jsonify({"session_id": session_id})


@app.route('/utterance', methods=['POST'])
def receive_utterance():
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()
    session_id = args['session_id']
    if session_id in data:
        with open('./temp/temp_' + str(session_id) + '/message' + str(session_id) + '.txt', 'w') as f:
            f.write(args['message'])

        os.system(
            'onmt_translate -model wf/run/model1_step_4000.pt -src temp/temp_' + str(session_id) + '/message' + str(
                session_id) + '.txt -output ./temp/temp_' + str(session_id) + '/pred' + str(
                session_id) + '.txt -gpu -1 -verbose')

        with open(f'./temp/temp_{session_id}/pred{session_id}.txt', 'r') as f:
            wf = f.readlines()[0].strip().split(' ')

        comprehension_sentence = summary_producer(wf, "")

        return jsonify({"session_id": session_id,
                        "request": wf,
                        "comprehension_sentence": comprehension_sentence,
                        "comprehension_state": "reformulation",
                        'comprehension_pipeline': wf})
    return jsonify({"message": "Errore"})


def get_results(received_id):
    print("Entrato in GET RESULTS")
    session_id = received_id
    app.logger.info('Polling results for session: %s', session_id)

    # recupero il file
    filename = data[session_id]['dataset'].name_plot
    if filename is None:
        pass

    # codifico il file in bytecode
    with open(filename, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # trasformo il bytecode in stringa
        base64_string = my_string.decode('utf-8')

    framework = get_framework(pipeline=data[session_id]['ir_tuning'],
                              result=base64_string,
                              start_work=partial(re_execute_algorithm, session_id=session_id))

    data[session_id]['framework'] = framework
    details = data[session_id]['dataset'].measures
    tuning_data = framework.handle_data_input({})
    print("STO PER RESTITUIRE")
    emit('results', {"ready": True,
                    "session_id": session_id,
                    'img': str(base64_string),
                    'details': str(details),
                    'tuning': tuning_data}, namespace='/', broadcast=True)


@app.route('/tuning', methods=['POST'])
def tuning():
    json_data = request.get_json(force=True)
    session_id = json_data['session_id']
    if json_data['type'] == 'utterance':
        response = data[session_id]['framework'].handle_text_input(json_data['utterance'])
    else:
        response = data[session_id]['framework'].handle_data_input(json_data['payload'])
    return jsonify({'tuning': response})

@simple_page.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('inspire.html', async_mode=sio.async_mode)

@app.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('inspire.html', async_mode=sio.async_mode)

def execute_algorithm(ir, session_id):
    asyncio.run(execute_algorithm_logic(ir, session_id))

async def execute_algorithm_logic(ir, session_id):
    app.logger.debug('Entering execute_algorithm function')
    app.logger.info('Executing pipeline: %s', [i for i in ir])
    dataset = data[session_id]['dataset']
    if hasattr(dataset, 'label'):
        results = {'original_dataset': dataset, 'labels': dataset.label}
    else:
        results = {'original_dataset': dataset}
    run(ir, results, session_id, socketio=sio)

    app.logger.info('Exiting execute_algorithm function')
    get_results(session_id)

def re_execute_algorithm(ir, session_id):
    data[session_id]['dataset'].name_plot = None
    threading.Thread(target=execute_algorithm, kwargs={'ir': ir, 'session_id': session_id}).start()

@app.route('/echo', methods=['POST'])
def echo():
    json_data = request.get_json(force=True)

    # Do stuff with the data received
    print(json_data)

    # Return a response
    return f"echo -> {json_data['payload']}"


@sio.on('comprehension')
def comprehension_chat(results):
    result = comprehension_conversation_handler(results, data[results['session_id']]['dataset'])
    emit('comprehension_response', result)

@sio.on('message_sent')
def handle_message(data):
    global message_queue
    message_queue.push(data['message'].strip())

@sio.on('ack')
def handle_message(data):
    print('received_message', data)

@sio.on('connect')
def test_connect():
    pass

@sio.on('receiveds')
def on_df_received(form_data):
    print("user data received!")

@sio.on('execute')
def on_execute_received(payload):
    scores = {}
    wf = payload['comprehension_pipeline']
    kb = data[session_id]['kb']
    print(kb.kb)
    for i in range(len(kb.kb)):
        sent = [x for x in kb.kb.values[i, 1:] if str(x) != 'nan']
        print(sent)
        sent = [x for x in sent if x not in ['missingValuesHandle', 'labelRemove','oneHotEncode','labelAppend', 'zerVarRemove','outliersRemove','standardization','normalization']]
        scores[i] = NW(wf, sent, kb.voc) / len(sent)
        print(scores[i])

    print(scores)
    max_key = max(scores, key=scores.get)
    max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
    print('MAX', max_key)

    ir_tuning = create_IR(max_key, message_queue)
    print(ir_tuning)

    data[session_id]['ir_tuning'] = ir_tuning
    execute_algorithm(ir_tuning, session_id)

app.register_blueprint(simple_page, url_prefix=base_url)

if __name__ == '__main__':
    sio.run(app, debug=True, port=5000, use_reloader=False)