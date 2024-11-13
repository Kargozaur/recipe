import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    # If we receive the key token as part of the response it would be bite object
    # Bite objects are bad to serialize, so they should be decoded before render User object
    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get("errors", None)
        token = data.get("token", None)
        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
