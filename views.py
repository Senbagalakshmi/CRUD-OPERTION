from django.shortcuts import render, redirect
from .models import User
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from .models import User
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import os
import pdfkit
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse  # Import reverse for URL resolution
# Homepage View
def homepage(request):
    return render(request, 'home.html')
# Read (List Users)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Create (Add User)
def user_create(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        User.objects.create(name=name, email=email)
        return redirect('user_list')
    return render(request, 'user_form.html')

# Update (Edit User)
def user_update(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.save()
        return redirect('user_list')
    return render(request, 'user_form.html', {'user': user})

# Delete (Remove User)
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.delete()
        return redirect('user_list')
    return render(request, 'user_delete.html', {'user': user})
# Export Users to Excel
def export_users_to_excel(request):
    users = User.objects.all().values('name', 'email')  # Fetch users
    df = pd.DataFrame(users)  # Convert to DataFrame
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    df.to_excel(response, index=False)  # Save as Excel file
    return response
# Export Users to PDF
def export_users_to_pdf(request):
    users = User.objects.all().values('name','email')
    template = get_template('export_users_pdf.html')
    html_string = render_to_string('export_users_pdf.html', {'users': users})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=users.pdf'

    pdf_status = pisa.CreatePDF(html_string, dest=response)
    if pdf_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response
# Send Email with Attachment
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render

def send_email_with_attachment(request):
    if request.method == 'POST' and request.FILES.get('attachment'):
        subject = "Test Email with Attachment"
        message = "This email contains an attachment."
        from_email = "your_email@gmail.com"  # Sender email
        recipient_list = ["recipient_email@gmail.com"]  # Replace with recipient email
        
        email = EmailMessage(subject, message, from_email, recipient_list)

        # Get uploaded file
        uploaded_file = request.FILES['attachment']
        email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

        try:
            email.send()
            return HttpResponse("Email sent successfully with attachment!")
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

    return render(request, 'send_email.html')
