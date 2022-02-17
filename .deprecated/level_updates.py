from twitter_client.models import Level

level1 = Level.objects.get(id=1)
level1.message="\"Once you choose hope, anything is possible.\" – Christopher Reeve username, hopefully, this song will help lift you up a bit. Also, email us if you need someone to chat with: whatsyourlevel@yahoo.com"
level1.save()


level2 = Level.objects.get(id=2)
level2.message="A 2? Well, username, at least you're not a 1! Shake it off and crank some tunes. Jumping from a 2 to a 5 is easy as pie. Lets go!"
level2.save()


level3 = Level.objects.get(id=3)
level3.message="Nobody wants to be a 3. username, tune in below and lets get you up to 6 stat!"
level3.save()


level4 = Level.objects.get(id=4)
level4.message="I'm going to pretend you didn't type that. If you're a 4, you're basically a 5. username, lets get you on the winning side. Tune in 👇"
level4.save()

level5 = Level.objects.get(id=5)
level5.message="A 5 ey? The middle seat is the worst seat, username, let's get you into the winning category. Tune in👇"
level5.save()


level6 = Level.objects.get(id=6)
level6.message="A 6? \"username gotta pump those numbers up. Those are rookie numbers in this racket.\" - Mark Hana"
level6.save()


level7 = Level.objects.get(id=7)
level7.message="Lucky number 7. We like 7's. Embrace the goodness and enjoy the day username."
level7.save()


level8 = Level.objects.get(id=8)
level8.message="An 8? Now you're talking! What's it going to take to break through to a 9 or a 10 username? Lets do this!!!"
level8.save()


level9 = Level.objects.get(id=9)
level9.message="A 9? C'mon, why not a 10? What's it going to take to break through username? LFG!!! Own the day!!!"
level9.save()


level10 = Level.objects.get(id=10)
level10.message="Boom!!! Oh yea username!!! Not every day you can be a 10, but today is your day.  Seize the day. LFG!!!"
level10.save()