from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import openai
import os
from django.conf import settings

credentials = settings.CONFIG['openapi']['api_key']
openai.api_key = credentials

import logging
logger = logging.getLogger(__name__)

def chatgpt(request):
    if request.method == "POST":
        receiveText = request.POST['receiveText']
        receiveImage = request.POST['receiveImage']
        try:
            result = {}
            if receiveText:
                result['textResult'] = openai_textGenerator(receiveText)
            if receiveImage:
                result['imageResult'] = openai_image(receiveImage)
        except Exception as e:
            messages.error(request, e)
            logger.debug("Error in chatGPT api response : {}".format(e))
        return render(request, "templateGenerator.html", context=result)
    else:
        return render(request, "templateGenerator.html")

# Generate text about a topic
def openai_textGenerator(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=150,
      temperature=0.5
    )
    return response['choices'][0]['text']

# Generate image from text
def openai_image(prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url        