import uuid
from django.shortcuts import render
from liqpay import liqpay
from django.contrib.sites.shortcuts import get_current_site

def donate_form(request):
    current_site = get_current_site(request)

    checkout_form = liqpay.get_checkout_form(
        order_id=uuid.uuid4(),
        amount=5,
        description='Донат на хостінг та розвиток сайту',
        result_url=current_site.domain,
        server_url=current_site.domain
    )

    return render(request, 'donate/donate_form.html', {'checkout_form': checkout_form})
