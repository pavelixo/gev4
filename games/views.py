from random import choices, uniform, random
from django.http import JsonResponse
from django.views import View, generic


class MineView(generic.TemplateView):
    template_name = 'mine.html'


class MineAPIView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'User is not authenticated'
            }, status=401)
        
        finding = self.finding()
        value = self.mine() if finding else 0

        if not finding:
            return JsonResponse({
                'is_successful': finding,
                'user_balance': request.user.balance,
                'value': value,
            })
            
        request.user.add_balance(value)
        request.user.save()

        return JsonResponse({
            'is_successful': finding,
            'user_balance': request.user.balance,
            'value': value,
        })

    def finding(self):
        chance = 0.5

        if not random() <= chance:
            return False
        
        return True

    def mine(self):
        ranges = [
            (0.00, 1.00, 80),    # 80% chance: 0.00 / 1.00
            (1.01, 10.00, 5),    # 5% chance: 1.01 / 10.00
            (10.01, 50.00, 10),  # 10% chance: 10.01 / 50.00
            (50.01, 100.00, 5)   # 5% chance: 50.01 / 100.00
        ]
        
        # Select a range based on weight
        selected = choices(ranges, weights=[r[2] for r in ranges])[0]

        # Generate a random value within the selected range
        value = round(uniform(selected[0], selected[1]), 2)

        return value