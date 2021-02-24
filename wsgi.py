from flask import Flask
from flask import jsonify
from parser.load_vac_utils import load_vacancies_pipeline
app = Flask(__name__)


@app.route('/app_sberjobs_parser/get_vacancies')
def get_new_vacancies():
    load_vacancies_pipeline()
    return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run()
