from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    inputs = data.get('inputs', [])
    expected_output = data.get('expectedOutput', None)

    input_data = '\n'.join(inputs) + '\n'
    actual_output = ''
    try:
        if language == 'python':
            process = subprocess.Popen(
                ['python', '-c', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == 'javascript':
            process = subprocess.Popen(
                ['node', '-e', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == 'cpp':
            with open('temp.cpp', 'w') as f:
                f.write(code)
            subprocess.check_output(['g++', 'temp.cpp', '-o', 'temp'])
            process = subprocess.Popen(
                ['./temp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == 'c':
            with open('temp.c', 'w') as f:
                f.write(code)
            subprocess.check_output(['gcc', 'temp.c', '-o', 'temp'])
            process = subprocess.Popen(
                ['./temp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == 'java':
            with open('Temp.java', 'w') as f:
                f.write(code)
            subprocess.check_output(['javac', 'Temp.java'])
            process = subprocess.Popen(
                ['java', 'Temp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            return jsonify({'output': 'Unsupported language.'})

        stdout, stderr = process.communicate(input=input_data.encode('utf-8'))
        if stderr:
            actual_output = stderr.decode('utf-8')
        else:
            actual_output = stdout.decode('utf-8')

        # Compare the actual output to expected output if provided
        if expected_output is not None:
            if actual_output.strip() == expected_output.strip():
                result = "Correct Output!"
            else:
                result = f"Incorrect Output.\nExpected:\n{expected_output}\nGot:\n{actual_output}"
        else:
            result = actual_output

        return jsonify({'output': result})

    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output.decode('utf-8')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
