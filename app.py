from flask import Flask, render_template, request, redirect
from serpapi import GoogleSearch

app = Flask(__name__)

result = []

def find(query):
	params = {
		'q':'',
		'hl':'en',
		'gl':'us',
		'api_key':'5bdc9e6a1aafdb8a94cbfd4bf85aa23b36c648293df4b509f83a73ec9dbdf327'
	}
	params['q'] = query
	search = GoogleSearch(params)
	results = search.get_dict()
	print(results)

	if 'answer_box_list' in results:
		return results['answer_box_list']

	if 'answer_box' in results:
		if results["answer_box"]["type"] == "calculator_result" or results["answer_box"]["type"] == "currency_converter":
			res = results["answer_box"]["result"]
			return [res]
		elif results["answer_box"]["type"] == "weather_result":
			res = results["answer_box"]["temperature"] + " " + results["answer_box"]["unit"]
			return [res]
		elif results["answer_box"]["type"] == "finance_results":
			res = results["answer_box"]["price"] + " " + results["answer_box"]["currency"]
			return [res]
		elif results["answer_box"]["type"] == "population_result":
			res = results["answer_box"]["population"]
			return [res]
		elif results["answer_box"]["type"] == "translation_result":
			res = results["answer_box"]["target"]["text"]
			return [res]
		elif results["answer_box"]["type"] == "directions":
			res = results["answer_box"]["routes"]["summary"]
			return [res]
		elif results["answer_box"]["type"] == "formula":
			res = results["answer_box"]["answer"]
			return [res]
		elif results["answer_box"]["type"] == "unit_converter":
			fromVal = results["answer_box"]["from"]["value"]
			fromUnit = results["answer_box"]["from"]["unit"]
			toVal = results["answer_box"]["to"]["value"]
			toUnit = results["answer_box"]["to"]["unit"]
			res = f'{str(fromVal)} {fromUnit} - {str(toVal)} {toUnit}'
			return [res]
		elif results["answer_box"]["type"] == "dictionary_results":
			res = []
			definitions = results["answer_box"]["definitions"]
			for i, e in enumerate(definitions):
				res.append(f'{str(i+1)}. {e}') 
			return res
		elif results["answer_box"]["type"] == "organic_result":
			if 'list' in results['answer_box']:
				lst = results["answer_box"]["list"]
				res = []
				for i, e in enumerate(lst):
					res.append(f'{str(i+1)}. {e}') 
				return res 
			elif 'snippet' in results['answer_box']:
				res = results["answer_box"]['snippet']
				return [res]
			elif 'contents' in results['answer_box']:
				res = results["answer_box"]["contents"]["table"]
				return [res]
		else:
			res = results["answer_box"]
			return [res]

	if 'organic_results' in results:
		res = results['organic_results'][0]['snippet']	
		return [res]

	return results

@app.route('/', methods=['GET', 'POST'])
def index():
	global result 
	print(request)
	if request.method == 'POST':
		form_content = request.form['content']
		result = find(form_content)
		print(result)
		return redirect('/')
	else:
		return render_template('index.html', result=result)


if __name__ == '__main__':
	app.run(debug=True, port=8000)