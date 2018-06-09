from smtplib import SMTPException
from django.core.mail import send_mail


def send_registration_email(user):
    send_mail(
        'Witaj w Centrum Wyborczym',
        'Twoje konto zostało zarejestrowane. Od tej chwili możesz brać udział w dostępnych dla Ciebie wyborach.',
        'Centrum Wyborcze <kamil@t32.pl>',
        [user.email],
        fail_silently=True
    )


def send_confirmation_email(user, election_id):
    try:
        send_mail(
            'Potwierdzenie oddania głosu',
            'Twój głos w wyborach został uwzględniony.\n'
            'Gdy wybory dobiegną końca, pod poniższym adresem dostępny '
            'będzie raport wyborczy\nhttp://wybory.t32.pl/report/' + str(election_id),
            'Centrum Wyborcze <kamil@t32.pl>',
            [user.email],
            fail_silently=False,
            )
        return True
    except SMTPException:
        return False
