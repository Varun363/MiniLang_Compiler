from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from compiler.pipeline import compile_source

app = Flask(__name__)

DEFAULT_CODE = '''program Demo {
    int a;
    int b;
    int result;

    a = 10;
    b = 20;
    result = a + b * 5;

    print(result);
}'''


@app.get("/")
def index():
    return render_template("index.html", default_code=DEFAULT_CODE)


@app.post("/compile")
def compile_route():
    data = request.get_json(silent=True) or {}
    source = data.get("source", "")
    return jsonify(compile_source(source))


if __name__ == "__main__":
    app.run(debug=True)
