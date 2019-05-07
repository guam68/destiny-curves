from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Card
import requests
import json


def index(request):
    return render(request, 'main/index.html')


def get_decks(request):
    url = 'https://swdestinydb.com/api/public/decklist/'
    data = json.loads(request.body)
    user_deck = requests.get(url + data['deck_id'].strip()).json()
    opp_deck = requests.get(url + data['opp_deck'].strip()).json()

    user_chars = user_deck['characters']
    opp_chars = opp_deck['characters']

    user_char_dict = assign_characters(user_chars)
    opp_char_dict = assign_characters(opp_chars)

    return JsonResponse({'user': user_char_dict, 'opp': opp_char_dict})


def assign_characters(chars):
    char_dict = {}
    i = 0
    for char in chars:
        if chars[char]['quantity'] == 1:
            card = Card.objects.filter(id = char)[0]
            char_dict[i] = { 
                'card': model_to_dict(card),
                'dice': chars[char]['dice'],
                'dice_dmg': card.calc_dmg()
            }
            i += 1
        else:
            for copy in range(chars[char]['quantity']):
                card = Card.objects.filter(id = char)[0]
                char_dict[i] = { 
                    'card': model_to_dict(Card.objects.filter(id = char)[0]),
                    'dice': 1,
                    'dice_dmg': card.calc_dmg()
                }
                i += 1
    
    return char_dict

