from wger.weight.models import WeightEntry
from django.contrib.auth.decorators import login_required
from fitbit.api import Fitbit
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import logging
import datetime

client_id = os.getenv('FITBIT_CLIENT_ID', None)
client_secret = os.getenv('FITBIT_CLIENT_SECRET', None)
fitbitObj = Fitbit(
    client_id,
    client_secret,
    timeout=10,
    system="en_AU"
)


@login_required
def fitbit_authorize(request):
    url, _ = fitbitObj.client.authorize_token_url()
    return HttpResponseRedirect(url)


@login_required
def fitbit_get_token(request):
    code = request.GET.get("code", None)

    if code:
        try:
            fitbitObj.client.fetch_access_token(code)
            request.session['fitbit_token'] = fitbitObj.client.session.token
            return HttpResponseRedirect(reverse('weight:overview',
                                                kwargs={
                                                    'username': request.user.username}))
        except Exception as er:
            logging.error("Token:" + str(er))

    return fitbit_authorize(request)


@login_required
def fitbit_get_weight(request):
    token = request.session.get('fitbit_token', {})
    token['client_id'] = client_id
    token['client_secret'] = client_secret
    token['timeout'] = 10
    token['system'] = 'en_AU'
    fitbitM = Fitbit(**token)

    weights = None
    date = datetime.date.today()
    try:
        weights = fitbitM.get_bodyweight(base_date=date, period='30d').get('weight', False)
    except Exception as er:
        logging.error("Weight:" + str(er))
        return fitbit_authorize(request)
    if weights:
        try:
            for weight in weights:
                entry = WeightEntry(user=request.user,
                                    weight=weight['weight'],
                                    date=weight['date'])
                entry.save()
        except Exception as er:
            logging.error("Did not save weight" + str(er))

    return HttpResponseRedirect(reverse('weight:overview',
                                        kwargs={
                                            'username': request.user.username}))
