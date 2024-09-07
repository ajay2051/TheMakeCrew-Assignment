from django.shortcuts import render


def room(request, room_name):
    context = {
        'room_name': room_name,
    }
    return render(request, 'chatroom.html', context=context)
