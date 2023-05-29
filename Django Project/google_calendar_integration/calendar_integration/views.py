from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'path/to/client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )

        request.session['oauth_state'] = state

        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code', None)

        state = request.GET.get('state', None)
        if state != request.session.get('oauth_state'):
            return JsonResponse({'error': 'Invalid state'}, status=400)

        flow = InstalledAppFlow.from_client_secrets_file(
            'path/to/client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
        )
        flow.fetch_token(code=code)

        service = build('calendar', 'v3', credentials=flow.credentials)

        events = service.events().list(calendarId='primary').execute()

        return JsonResponse({'events': events})

