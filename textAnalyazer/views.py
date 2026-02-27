import os
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

def htmlform(request):
    return render(request,'index.html')

def analyze(request):
    
    #get the text from forntend
    mainText=request.GET.get('txt','default')
    
    #check checkbox values  
    checkbox1=request.GET.get('removepunc','off')
    checkbox2=request.GET.get('capatalized','off')
    checkbox3=request.GET.get('newlineremover','off') #(\n)
    checkbox4=request.GET.get('whitespaceremover','off') #(new_line,spcae,tab)
    checkbox5=request.GET.get('extraspaceremover','off') #(my  name is)
    checkbox6=request.GET.get('charcount','off') #(count the character)

    multi_purposes = []
    
    #main logic ( to check which checkbox is on)
    #function to remove puncutation from paragraph
    if checkbox1=="on":
        analyzed_text = ""
        punctuations="""!()-[]{};:'"\,<>./?@#$%^&*_`~"""
        for char in mainText:
            if char not in punctuations:
                analyzed_text+=char
        multi_purposes.append("Remove Punctuations")
        context={
                'purpose':"Remove Punctuations",
                'after_analyzed':analyzed_text
        }
        mainText=analyzed_text
    

    #function to changed the paragraph to uppercase
    if checkbox2=='on':
        analyzed_text = ""
        for char in mainText:
            analyzed_text+=char.upper()  
        multi_purposes.append("Changed to UpperCase")
        context={
                'purpose':"Changed to UpperCase",
                'after_analyzed':analyzed_text
        }
        mainText=analyzed_text
    
    #function to remove new line
    if checkbox3=='on':
        analyzed_text = ""
        for char in mainText:
            if char!="\n" and char != '\r':
                analyzed_text+=char
        multi_purposes.append("New Line Removed")
        context={
                'purpose':"New Line Removed",
                'after_analyzed':analyzed_text
        }
        mainText=analyzed_text
    
    #function to remove whiteSpaces
    if checkbox4=='on':
        analyzed_text = ""
        for char in mainText:
                analyzed_text+=char.strip()
        multi_purposes.append("White Space Removed")
        context={
                'purpose':"White Space Removed",
                'after_analyzed':analyzed_text
        }
        mainText=analyzed_text
    
    #function to remove extraSpaces
    if checkbox5=='on':
        analyzed_text = ""
        for index,char in enumerate(mainText):
                if not (mainText[index]==" " and mainText[index+1]==" "):
                     analyzed_text+=char
        multi_purposes.append("Extra Space Removed")
        context={
                'purpose':"Extra Space Removed",
                'after_analyzed':analyzed_text
        }
        mainText=analyzed_text


    #function to count the character of the text
    if checkbox6 == 'on':
        count = f"Total character in this text is {len(mainText)}<br>"

        # Multiple checkboxes selected
        if (checkbox1 == 'on' or checkbox2 == 'on' or checkbox3 == 'on' 
            or checkbox4 == 'on' or checkbox5 == 'on'):
            
            analyzed_text = count + mainText
            multi_purposes.append("Character Count")
            context = {
                'purpose': "Character Count",
                'after_analyzed': analyzed_text
            }
        
        # Only character count checkbox selected
        else:
            multi_purposes.append("Character Count")
            context = {
                'purpose': "Character Count",
                'after_analyzed': count
            }


    if (checkbox1=='off' and checkbox2=='off' and checkbox3=='off' and 
        checkbox4=='off' and checkbox5=='off' and checkbox6=='off'):
         return HttpResponse('<h1 style="color: red;">Error! Select at least one checkbox</h1>')


    context['purpose'] = ", ".join(multi_purposes)
    
    return render(request,'analyze.html',context)


def features(request):
    return render(request,'features.html')

def contact(request):
    # Handle contact form POST
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        gender = request.POST.get('gender', '').strip()
        age = request.POST.get('age', '').strip()
        dob = request.POST.get('dob', '').strip()
        country = request.POST.get('country', '').strip()
        other_country = request.POST.get('other_country', '').strip()
        message = request.POST.get('message', '').strip()

        to_email = getattr(settings, 'CONTACT_RECIPIENT_EMAIL', 'hrjobportal.system@gmail.com')
        subject = f"Website contact form submission from {email or phone or 'Anonymous'}"
        plain = (
            f"Email: {email}\nPhone: {phone}\nGender: {gender}\nAge: {age}\nDOB: {dob}\n"
            f"Country: {other_country or country}\n\nMessage:\n{message}\n"
        )
        html = (
            f"<p><strong>Email:</strong> {email}</p>"
            f"<p><strong>Phone:</strong> {phone}</p>"
            f"<p><strong>Gender:</strong> {gender}</p>"
            f"<p><strong>Age:</strong> {age}</p>"
            f"<p><strong>DOB:</strong> {dob}</p>"
            f"<p><strong>Country:</strong> {other_country or country}</p>"
            f"<hr><p>{message}</p>"
        )

        # Try SendGrid API (HTTP) first, fallback to Django email backend
        sent = False
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        if sendgrid_api_key:
            try:
                import requests
                url = 'https://api.sendgrid.com/v3/mail/send'
                payload = {
                    'personalizations': [{ 'to': [{ 'email': to_email }] }],
                    'from': { 'email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@textutils.np') },
                    'subject': subject,
                    'content': [
                        { 'type': 'text/plain', 'value': plain },
                        { 'type': 'text/html', 'value': html },
                    ]
                }
                resp = requests.post(url, json=payload, headers={
                    'Authorization': f'Bearer {sendgrid_api_key}',
                    'Content-Type': 'application/json'
                }, timeout=10)
                if resp.status_code in (200, 202):
                    sent = True
                else:
                    sent = False
                    logger.error('SendGrid returned %s: %s', resp.status_code, resp.text)
            except Exception as e:
                sent = False
                logger.exception('SendGrid send failed: %s', e)

        if not sendgrid_api_key or not sent:
            try:
                msg = EmailMultiAlternatives(subject, plain, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@textutils.np'), [to_email])
                msg.attach_alternative(html, 'text/html')
                msg.send()
                sent = True
            except Exception as e:
                sent = False
                logger.exception('Fallback email send failed: %s', e)

        return render(request, 'contact.html', {'email_sent': sent})

    return render(request,'contact.html', {'email_sent': None})

def about(request):
    return render(request,'about.html')
