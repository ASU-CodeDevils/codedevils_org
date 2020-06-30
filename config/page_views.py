"""Used to store any custom view actions or context for pages."""

from django.shortcuts import render, redirect

def contact_us(request):
    """View function for the Contact Us page."""
    if request.method == 'POST':
        contact_email = request.POST.get('Contact[email]')
        contact_subject = request.POST.get('Contact[subject]')
        contact_message = request.POST.get('Contact[message]')

        # format the message
        message = 'Someone has used the Contact Us page to send a message:\n\n{}'.format(contact_message)

        # send email to webmaster
        send_email.delay(subject=contact_subject,
                         from_email=contact_email,
                         recipient_list=['webmaster@codedevils.org'],
                         message=message,
                         fail_silently=True)

        # log the contact
        logger.info('Contact message sent from {} to webmaster'.format(contact_email))
        messages.info(request, message='Your message has been received and we\'ll email you back soon.')
        return redirect('home:index')
    else:
        context = {
            'title': 'Contact Us',
            'show_navbar': 'True',
        }
        return render(request, 'contactus/contact.html', context=context)