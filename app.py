# API_SQL
from flask import Flask, render_template, request, jsonify
import mysql.connector
from summarization import summarize_text
from generation import generate_answer
from translate import translate_text
import os
os.environ['CURL_CA_BUNDLE'] = ''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'dados'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    summarized_text = ''
    answer = ''
    translated_text = ''
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        ethnicity = request.form['ethnicity']
        gender = request.form['gender']
        insert_data(name, age, ethnicity, gender)

        text_summarization = request.form['text_summarization']
        summarized_text = summarize_text(text_summarization)

        text_generation = request.form['text_generation']
        question = request.form['question']
        answer = generate_answer(question, text_generation)

        text_translation = request.form['text_translation']
        language = request.form['language']
        translated_text = translate_text(text_translation, language)

        return render_template('index.html', summarized_text=summarized_text, answer=answer, translated_text=translated_text)

    return render_template('index.html', summarized_text=summarized_text, answer=answer, translated_text=translated_text)

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                 answer, text_translation, language, translated_text):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO INFO(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text) 
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Erro MySQL:", err)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text_to_summarize = data.get('text', '')
    summarized_text = summarize_text(text_to_summarize)
    return jsonify({'summarized_text': summarized_text})

@app.route('/generate_answer', methods=['POST'])
def generate_answer_route():
    try:
        data = request.get_json()
        question = data['question']
        context = data['context']
        answer = generate_answer(question, context)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/generate_answer_from_question', methods=['POST'])
def generate_answer_from_question():
    data = request.json
    question_to_generate_answer = data.get('question', '')
    text_to_generate = data.get('text', '')
    answer = generate_answer(question_to_generate_answer, text_to_generate)
    return jsonify({'answer': answer})
@app.route('/response')
def form_submitted():
    return render_template('response.html')
if __name__ == '__main__':
    app.run(debug=True)
