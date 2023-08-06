from django.urls import re_path
from pretalx.event.models.event import SLUG_CHARS

from . import views

urlpatterns = [
    re_path(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/signup/$",
        views.SignupView.as_view(),
        name="signup",
    ),
    re_path(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/thanks/$",
        views.ThanksView.as_view(),
        name="thanks",
    ),
    re_path(
        # The user needs to be the last element of the URL due to the JS code
        # Trailing slashes are ignored by the JS code.
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/talks/(?P<signed_user>[^/]+)/$",
        views.SubmissionListView.as_view(),
        name="talks",
    ),
    re_path(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/api/$",
        views.ApiView.as_view(),
        name="api",
    ),
]
