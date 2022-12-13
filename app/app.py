from flask import Flask, render_template, request, flash
from flask import send_file
from flask import Markup
from werkzeug.utils import secure_filename
import engine

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

essay_str = ""
summarize_str = ""
keywords_str = ""

@app.route("/")
def main():
	return render_template("info_page.html")

@app.route("/info")
def info():
	return render_template("info_page.html")

@app.route("/upload")
def upload():
	return render_template("process_page.html")

@app.route("/result")
def result():
	flash(str(essay_str))
	flash(str(summarize_str))
	flash(str(keywords_str))
	return render_template("result_page.html")

@app.route("/process", methods=['POST'])
def process():
	f = request.files['file']
	f.save(secure_filename("text.txt"))

	global essay_str 
	global summarize_str
	global keywords_str
	result = engine.run_logic("text.txt")
	essay_str = result[0]
	summarize_str = result[1]
	keywords_str = result[2]

	flash(Markup("<h3>Эссе по тексту:</h3>"))
	flash(str(essay_str))
	flash(Markup("<h3>Подведение итогов:</h3>"))
	flash(str(summarize_str))
	flash(Markup("<h3>Ключевые слова:</h3>"))
	flash(str(keywords_str))
	return render_template("result_page.html")

@app.route("/donwload_result")
def download_result():
	path = 'result.txt'
	return send_file(path, as_attachment=True, cache_timeout=0)

@app.route("/donwload_text")
def download_text():
	path = 'text.txt'
	return send_file(path, as_attachment=True, cache_timeout=0)