import smtplib, ssl, time, random
from datetime import date, timedelta
from tmdbv3api import Discover, TMDb  # pip install tmdbv3api

email = input("Enter your email: ")
password = input("Enter your email's password: ")


def get_recommended_movies():
    tmdb = TMDb()
    tmdb.api_key = 'your-api-key'
    tmdb.language = 'en'

    movies = ''

    discover = Discover()
    movie = discover.discover_movies({
        'primary_release_date.lte': '{}'.format(date.today().__str__()),
        'primary_release_date.gte': '1900-01-01'
    })

    num = 0
    for m in movie:
        if num == 10:
            return movies
        mo = '\t' + m.title + ' : \n\n\t' + m.overview + '\n\n\n\n'
        movies += mo
        num += 1

    return movies


def send_movies_mail():
    movies = get_recommended_movies()

    port = 465
    smtp_server = "smtp.gmail.com"
    message = """Subject: Your automated recommended movies mail

    Hi, how are you doing?

    This E-Mail is sent to you from your python movies sender bot.


    These are your recommended movies for this week:


{}
    Enjoy your time!""".format(movies).encode('ascii', 'ignore').decode('ascii')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)


if __name__ == '__main__':
    while True:
        local_time = time.localtime(time.time())
        if local_time.tm_hour == 20 and local_time.tm_min == 0:
            send_movies_mail()
            time.sleep(60 * 60 * 24 * 7)
        time.sleep(59)
