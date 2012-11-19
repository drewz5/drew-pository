from django.template.response import TemplateResponse

import models

def team_list(request):
    """
    Lists all teams in the Database
    """
    return TemplateResponse(request, 'softball/team/list.html', {
            'teams':models.Team.objects.all().order_by('name'),
    })

def team_view(request, team_id):
    """
    Lists all teams in the Database
    """
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/team/view.html', {
        'team': team,
        'record': team.record(),
    })

#def player_list(request):
 #   """
  #  Lists all players in the Database
   # """
   # return TemplateResponse(request, 'softball/teams/players/
