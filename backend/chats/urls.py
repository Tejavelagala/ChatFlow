from django.urls import path

from .views import (
    CreateRoomView,
    JoinRoomView,
    RoomDetailsView,
    SendMessageView,
    RoomMessagesView,
    AllRoomsView,
    DeleteRoomView,
    UserPresenceView,
    UploadImageView,
    DeleteMessageView,
    EditMessageView,
    ReactMessageView,
    UploadAudioView,
    UserProfileView,
    UploadFileView,
    PinMessageView,
    UnpinMessageView,
    PinnedMessagesView,
    RoomMembersView,
    LeaveRoomView,
    PromoteUserView,
    BanUserView,
    MuteUserView
)

urlpatterns = [
    path(
        'create-room/',
        CreateRoomView.as_view()
    ),

    path(
        'join-room/<uuid:room_id>/',
        JoinRoomView.as_view()
    ),

    path(
        'room/<uuid:room_id>/',
        RoomDetailsView.as_view()
    ),

    path(
        'send-message/<uuid:room_id>/',
        SendMessageView.as_view()
    ),

    path(
        'all-rooms/',
        AllRoomsView.as_view()
    ),

    path(
        'room-messages/<uuid:room_id>/',
        RoomMessagesView.as_view()
    ),

    path(
        'delete-room/<uuid:room_id>/',
        DeleteRoomView.as_view()
    ),

    path(
        'presence/<str:username>/',
        UserPresenceView.as_view()
    ),

    path(
        'upload-image/',
        UploadImageView.as_view()
    ),

    path(
        'delete-message/<int:message_id>/',
        DeleteMessageView.as_view()
    ),

    path(
        'edit-message/<int:message_id>/',
        EditMessageView.as_view()
    ),

    path(
        'react-message/<int:message_id>/',
        ReactMessageView.as_view()
    ),

    path(
        'upload-audio/',
        UploadAudioView.as_view()
    ),

    path(
        'profile/',
        UserProfileView.as_view()
    ),

    path(
        'upload-file/',
        UploadFileView.as_view()
    ),

    path(
        'pin-message/<int:message_id>/',
        PinMessageView.as_view()
    ),

    path(
        'unpin-message/<int:message_id>/',
        UnpinMessageView.as_view()
    ),

    path(
        'pinned-messages/<uuid:room_id>/',
        PinnedMessagesView.as_view()
    ),

    path(
        'room-members/<uuid:room_id>/',
        RoomMembersView.as_view()
    ),

    path(
        'leave-room/<uuid:room_id>/',
        LeaveRoomView.as_view()
    ),

    path(
        'promote-user/<uuid:room_id>/',
        PromoteUserView.as_view()
    ),

    path(
        'ban-user/<uuid:room_id>/',
        BanUserView.as_view()
    ),

    path(
        'mute-user/<uuid:room_id>/',
        MuteUserView.as_view()
    ),
]