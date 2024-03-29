from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login

import models, forms

def user_signup(request):
    if request.method == 'POST':
        form = forms.UserSignupForm(data=request.POST)
        if form.is_valid():
            form.save()
        # log user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, u'Welcome to the Softball Tracker')
            return redirect('softball_home')
    else:
        form = forms.UserSignupForm()
    return TemplateResponse(request, 'softball/user_signup.html', {
            'form':form,
    })

@login_required
def user_edit(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, u'User profile updated')
            return redirect('user_edit')
    else:
        form = forms.UserForm(instance=user)
    return TemplateResponse(request, 'softball/user_edit.html', {
            'user': user,
            'form': form,
    })

def team_list(request):
    paginator = Paginator(models.Team.objects.all().order_by('name'),
                          10)
    page = request.GET.get('page')
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/team/list.html', {
        'teams': teams,
    })


def team_view(request, team_id):
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/team/view.html', {
        'team': team,
        'record': team.record(),
    })


@login_required
@permission_required('softball.add_team')
def team_create(request):
    if request.method == 'POST':
        team_form = forms.TeamForm(request.POST)
        if team_form.is_valid():
            team = team_form.save()
            return redirect('team_view', team_id=team.id)
    else:
        team_form = forms.TeamForm()

    return TemplateResponse(request, 'softball/team/create.html', {
        'team_form': team_form,
    })

@login_required
def team_edit(request, team_id=None):
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        team_form = forms.TeamForm(request.POST, instance=team)
        if team_form.is_valid():
            team = team_form.save()
            return redirect('team_view', team_id=team.id)
    else:
        team_form = forms.TeamForm(instance=team)

    return TemplateResponse(request, 'softball/team/edit.html', {
        'team': team,
        'record': team.record(),
        'team_form': team_form,
    })
@login_required
def team_delete(request, team_id):
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Player.DoesNotExist:
        raise Http404
    team.delete()
    messages.success(request, 'Team {0} delehted'.format(team.name))
    return redirect('team_list')

def player_list(request):
    paginator = Paginator(models.Player.objects.all().order_by('name'),
                          10)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/player/list.html', {
        'players': players,
    })


def player_view(request, player_id):
    try:
        player = models.Player.objects.get(pk=player_id)
    except models.Team.DoesNotExist:
        raise Http404
    messages.success(request, 'Player {0} created'.format(player.name))
    return TemplateResponse(request, 'softball/player/view.html', {
        'player': player,
    })

@login_required
@permission_required('softball.add_player')
def player_create(request):
    # if there's a team_id specified, use that team as the preset team for
    # this player
    team = models.Team()
    if request.GET.has_key('team_id'):
        try:
            team = models.Team.objects.get(pk=request.GET['team_id'])
        except models.Team.DoesNotExist, e:
            # Team doesn't exist, so just use an empty team
            pass
    player = models.Player(team=team)

    if request.method == 'POST':
        player_form = forms.PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player = player_form.save()
            return redirect('player_view', player_id=player.id)
    else:
        player_form = forms.PlayerForm(instance=player)

    return TemplateResponse(request, 'softball/player/create.html', {
        'player': player,
        'player_form': player_form,
    })

@login_required
def player_edit(request, player_id):
    try:
        player = models.Player.objects.get(pk=player_id)
    except models.Player.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        player_form = forms.PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player = player_form.save()
            return redirect('player_view', player_id=player.id)
    else:
        player_form = forms.PlayerForm(instance=player)

    return TemplateResponse(request, 'softball/player/edit.html', {
        'player': player,
        'player_form': player_form,
    })

@login_required
def player_delete(request, player_id):
    try:
        player = models.Player.objects.get(pk=player_id)
    except models.Player.DoesNotExist:
        raise Http404
    player.delete()
    messages.success(request, 'Player {0} delehted'.format(player.name))
    return redirect('player_list')

def game_list(request):
    paginator = Paginator(models.Game.objects.all().order_by('played_on'),
                          10)
    page = request.GET.get('page')
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/game/list.html', {
        'games': games,
    })


def game_view(request, game_id):
    try:
        game = models.Game.objects.get(pk=game_id)
    except models.Game.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/game/view.html', {
        'game': game,
        'away_roster': game.away_roster,
        'home_roster': game.home_roster,
    })

@login_required
@permission_required('softball.add_game')
def game_create(request):
    if request.method == 'POST':
        game_form = forms.GameForm(request.POST)
        if game_form.is_valid():
            # home_team must be assigned a roster
            home_roster = models.Roster(
                team=game_form.cleaned_data['home_team'])
            home_roster.save()
            # away_team must be assigned a roster
            away_roster = models.Roster(
                team=game_form.cleaned_data['away_team'])
            away_roster.save()
            game = game_form.save(commit=False)
            game.home_roster = home_roster
            game.away_roster = away_roster
            game.save()
            messages.success(request, 'Game {0} created'.format(game))
            return redirect('game_edit', game_id=game.id)
    else:
        game_form = forms.GameForm()
    return TemplateResponse(request, 'softball/game/create.html', {
        'game_form': game_form,
    })

@login_required
def game_edit(request, game_id):
    try:
        game = models.Game.objects.get(pk=game_id)
    except models.Player.DoesNotExist:
        raise Http404

    initial = {
        'home_team': game.home_roster.team_id,
        'away_team': game.away_roster.team_id,
    }
    if request.method == 'POST':
        game_form = forms.GameForm(request.POST, instance=game, initial=initial)
        home_statistic_formset = forms.GameStatisticModelFormSet(
            request.POST, prefix='home', instance=game.home_roster)
        away_statistic_formset = forms.GameStatisticModelFormSet(
            request.POST, prefix='away', instance=game.away_roster)
        if game_form.is_valid() and home_statistic_formset.is_valid() \
                and away_statistic_formset.is_valid():
            game = game_form.save()
            # if home_team or away_team were changed, clear the statistics
            if 'home_team' in game_form.changed_data:
                game.home_roster.team = game_form.cleaned_data['home_team']
                game.home_roster.save()
                game.home_roster.player_statistics.all().delete()
            else:
                home_statistic_formset.save()
            if 'away_team' in game_form.changed_data:
                game.away_roster.team = game_form.cleaned_data['away_team']
                game.away_roster.save()
                game.away_roster.player_statistics.all().delete()
            else:
                away_statistic_formset.save()
            if 'home_team' in game_form.changed_data or \
               'away_team' in game_form.changed_data:
                return redirect('game_edit', game_id=game.id)
            messages.success(request, 'Game {0} updated'.format(game))
            return redirect('game_view', game_id=game.id)
    else:
        game_form = forms.GameForm(instance=game, initial=initial)
        home_statistic_formset = forms.GameStatisticModelFormSet(
            prefix='home', instance=game.home_roster)
        away_statistic_formset = forms.GameStatisticModelFormSet(
            prefix='away', instance=game.away_roster)

    return TemplateResponse(request, 'softball/game/edit.html', {
        'game': game,
        'game_form': game_form,
        'home_statistic_formset': home_statistic_formset,
        'away_statistic_formset': away_statistic_formset,
    })

@login_required
def game_delete(request, game_id):
    try:
        game = models.Game.objects.get(pk=game_id)
    except models.Game.DoesNotExist:
        raise Http404
    # be sure to delete the rosters first!
    game.home_roster.delete()
    game.away_roster.delete()
    game.delete()
    messages.success(request, 'Game {0} deleted'.format(game))
    return redirect('game_list')
