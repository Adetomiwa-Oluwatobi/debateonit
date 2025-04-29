# rooms/views.py

from debate.utils import assign_roles
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Room, Player
from debate.models import Topic  # Assuming Topic model is in the `debate` app
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import json

def room_create(request):
    if request.method == 'POST':
        player_count = int(request.POST.get('player_count', 0))
        player_names = []

        for i in range(1, player_count + 1):
            name = request.POST.get(f'player{i}')
            if name:
                player_names.append(name)

        if len(player_names) != player_count:
            return HttpResponse("Missing player names!")

        # Define role sets
        roles_4 = ["OG", "OO", "CG", "CO"]
        roles_8 = ["PM", "LO", "DPM", "DLO", "MG", "MO", "GW", "OW"]
        # Assign roles randomly
        if player_count == 4:
            random.shuffle(player_names)
            assigned_roles = dict(zip(player_names, roles_4))
        elif player_count == 8:
            random.shuffle(player_names)
            assigned_roles = dict(zip(player_names, roles_8))
        else:
            return HttpResponse("Invalid number of players selected")

        # Select a random topic
        topic = random.choice(Topic.objects.all())

        # Create room and assign players
        room = Room.objects.create(topic=topic)

        for name in player_names:
            role = assigned_roles.get(name)
            player = Player.objects.create(name=name, role=role, room=room)
            room.players.add(player)

        return redirect('debate_room', room_id=room.id)

    return render(request, 'rooms/room_create.html')

def debate_room(request, room_id):
    room = Room.objects.get(id=room_id)
    
    # Always use BP format (since your example shows PM role)
    player_order = ["PM", "LO", "DPM", "DLO", "MG", "MO", "GW", "OW"]
    
    players_qs = room.players.all()
    players_by_role = {player.role: player.name for player in players_qs}

    ordered_players = []
    for role in player_order:
        player_name = players_by_role.get(role)
        if player_name:
            ordered_players.append((role, player_name))

    # Send player names and roles as JSON
    player_names = [name for _, name in ordered_players]
    roles_dict = {name: role for role, name in ordered_players}

    return render(request, 'rooms/debate_room.html', {
        'room': room,
        'ordered_players': ordered_players,
        'ordered_players_json': json.dumps(player_names, cls=DjangoJSONEncoder),
        'roles_json': json.dumps(roles_dict, cls=DjangoJSONEncoder),
    })
    
def landing_page(request):
    return render(request, 'rooms/landing.html', {'year': 2025})

def join_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        try:
            room = Room.objects.get(id=room_id)
            return redirect('debate_room', room_id=room.id)
        except Room.DoesNotExist:
            return render(request, 'landing.html', {'error': 'Room not found.', 'year': 2025})

def judge_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Get all players in BP format order
    player_order = ["PM", "LO", "DPM", "DLO", "MG", "MO", "GW", "OW"]
    
    players_qs = room.players.all()
    players_by_role = {player.role: player for player in players_qs}

    ordered_players = []
    for role in player_order:
        if role in players_by_role:
            ordered_players.append(players_by_role[role])
    
    # Handle form submission for scores
    if request.method == 'POST':
        # Process and save scores
        for player in ordered_players:
            content_score = request.POST.get(f'content_{player.id}', 0)
            style_score = request.POST.get(f'style_{player.id}', 0)
            strategy_score = request.POST.get(f'strategy_{player.id}', 0)
            poi_score = request.POST.get(f'poi_{player.id}', 0)
            
            # Calculate total score
            total_score = float(content_score) + float(style_score) + float(strategy_score) + float(poi_score)
            
            # Update player model with scores
            player.content_score = content_score
            player.style_score = style_score
            player.strategy_score = strategy_score
            player.poi_score = poi_score
            player.total_score = total_score
            player.save()
        
        # Redirect to results page or back to judge page with success message
        return redirect('debate_results', room_id=room.id)
    
    # For GET request, just display the judging form
    return render(request, 'rooms/judge.html', {
        'room': room,
        'players': ordered_players,
        'topic': room.topic,
    })

def debate_results(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Get all players ordered by total score (descending)
    players = room.players.all().order_by('-total_score')
    
    # Group players by team
    opening_gov = [p for p in players if p.role in ["PM", "DPM"]]
    opening_opp = [p for p in players if p.role in ["LO", "DLO"]]
    closing_gov = [p for p in players if p.role in ["MG", "GW"]]
    closing_opp = [p for p in players if p.role in ["MO", "OW"]]
    
    # Calculate team scores
    team_scores = {
        'Opening Government': sum(p.total_score for p in opening_gov),
        'Opening Opposition': sum(p.total_score for p in opening_opp),
        'Closing Government': sum(p.total_score for p in closing_gov),
        'Closing Opposition': sum(p.total_score for p in closing_opp),
    }
    
    # Sort teams by score
    ranked_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
    
    return render(request, 'rooms/results.html', {
        'room': room,
        'players': players,
        'ranked_teams': ranked_teams,
        'topic': room.topic,
    })
    


def download_resource(request, resource_id):
    # Logic to handle resource downloads
    # Could serve a PDF, DOC, or other file
    pass

def view_article(request, article_id):
    # Logic to display an article
    pass

from django.views.generic import ListView, DetailView
from .models import Tutorial, TutorialCategory

class TutorialListView(ListView):
    """Display all tutorial resources organized by category"""
    model = Tutorial
    template_name = 'rooms/tutorial.html'
    context_object_name = 'tutorials'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories with their tutorials
        categories = TutorialCategory.objects.prefetch_related('tutorials')
        
        # Create a dictionary of category -> tutorials
        categorized_tutorials = {}
        for category in categories:
            categorized_tutorials[category] = category.tutorials.all()
        
        context['categorized_tutorials'] = categorized_tutorials
        
        # Get featured tutorials for potential highlighting
        context['featured_tutorials'] = Tutorial.objects.filter(featured=True)
        
        return context

class TutorialDetailView(DetailView):
    """Display a single tutorial in detail"""
    model = Tutorial
    template_name = 'rooms/tutorial_detail.html'
    context_object_name = 'tutorial'
    slug_url_kwarg = 'tutorial_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related tutorials in the same category
        tutorial = self.get_object()
        context['related_tutorials'] = Tutorial.objects.filter(
            category=tutorial.category
        ).exclude(id=tutorial.id)[:3]
        return context