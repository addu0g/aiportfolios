from django.http import HttpResponse
from django.template import loader
import markdown
import google.generativeai as genai
import os

def home(request):
    template = loader.get_template("master.html")
    context = {  }

    return HttpResponse(template.render(context, request))    

def index(request):
    template = loader.get_template("aiportfolios/index.html")
    context = {  }

    return HttpResponse(template.render(context, request))


def iaquery(request):
    
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    template = loader.get_template("aiportfolios/iaresult.html")
    if not 'age' in request.POST:
        return HttpResponse(template.render({
                                            "result": markdown.markdown('You have to introduce an age.')
                                    }, request))
    if not 'ammount' in request.POST:
        return HttpResponse(template.render({
                                            "result": markdown.markdown('You have to introduce an ammount to create the protfolio.')
                                    }, request))
    age = request.POST["age"]
    risk = request.POST["risk"]
    horizon = request.POST["horizon"]
    objective = request.POST["objective"]
    ammount = request.POST["ammount"]
    language = "English"
    if "language" in request.POST:
        language = "Spanish"
    role = "Act as Warren Buffet, Act as Peter Lynch, Act as Stanley Druckenmiller, Act as Ray Dalio"
    goal = f"Generate a portfolio for a person in its {age} who is looking a risk tolerance: {risk}, and with an investment horizon of {horizon} this investment will be to {objective}" 
    restrictions = "Use simple language, write in a formal tone"
    format = f"""Create the response in language: {language}, Answer with bullet points, 
                Include in each response an html table for the portfolio summary with a list of possible tickers, 
                Condense all the tickers and portfolio suggestion in a global html table for an easy understanding, 
                Must be presented in an HTML format, 
                Remove the inversor name from the global portfolio, 
                Show the percentage column and make sure to balance the values in it summing them and getting the result equal to 100, 
                Remove the repeated tickers in Ticker column for the global table and rebalance the percentage column,
                Add a column with the name 'Ammount' in it and use the percentage column to prorate the ammount ${ammount} using each percentage for each ticker"""
    prompt = f"{role} - {goal} - {restrictions} - {format}"
    portfolioResult = model.generate_content(prompt)
    context = {
        "result": markdown.markdown(portfolioResult.text.replace('```html', '').replace('```', ''))
    }
    return HttpResponse(template.render(context, request))

    