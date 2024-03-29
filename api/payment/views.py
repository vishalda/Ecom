from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree
from django.conf import settings


# Create your views here.

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='bk7ns9zg5sw95h4b',
    public_key='4p8yk66nky638585',
    private_key='90dba8b3a410e35ae61c3f6a112a07d6'
  )
)


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error' : 'Invalid session, Please login again!'})

    try:
        #clientToken = gateway.client_token.generate({'customer_id':id})
        clientToken = gateway.client_token.generate(
        params={'merchant_account_id': settings.BRAINTREE_MERCHANT_ID})
        return JsonResponse({'clientToken':clientToken, 'success':True})
    except:
        return JsonResponse({'clientToken':gateway.client_token.generate({}), 'success':True})


@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error' : 'Invalid session, Please login again!'})
    
    nonce_from_the_client = request.POST["paymentMethodNonce"]
    amount_from_the_client = request.POST["amount"]

    result = gateway.transaction.sale({
        "amount":amount_from_the_client,
        "payment_method_nonce":nonce_from_the_client,
        "options":{
            "submit_for_settlement":True
        }
    })

    if result.is_success:
        return JsonResponse({
            "success":result.is_success,
            "transaction":{'id':result.transaction.id, 'amount':result.transaction.amount}
        })
    else:
        return JsonResponse({'error':True, 'success':False})