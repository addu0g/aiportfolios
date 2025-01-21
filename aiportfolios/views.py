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
    age = request.POST["age"]
    risk = request.POST["risk"]
    horizon = request.POST["horizon"]
    objective = request.POST["objective"]
    language = "English"
    if "language" in request.POST:
        language = "Spanish"
    role = "Act as Warren Buffet, Act as Peter Lynch, Act as Stanley Druckenmiller, Act as Ray Dalio"
    goal = f"Generate a portfolio for a person in its {age} who is looking a risk tolerance: {risk}, and with an investment horizon of {horizon} this investment will be to {objective}" 
    restrictions = "Use simple language, write in a formal tone"
    format = f"Create the response in language: {language}, Answer with bullet points, include an html table for the portfolio summary"
    prompt = f"{role} - {goal} - {restrictions} - {format}"
    portfolioResult = model.generate_content(prompt)
    context = {
        "result": markdown.markdown(portfolioResult.text)
    }
    return HttpResponse(template.render(context, request))

    