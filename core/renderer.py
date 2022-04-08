from rest_framework.renderers import JSONRenderer

from collections.abc import Iterable

"""
Success
{
    "success": true,
    "data": { . . . }
}

Fail
{
    "success": false,
    "errors": ["message 1", "message 2", . . .],
}
"""

class BahooRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            success=data.get('success', True)
        else:
            success=True

        # exception handler renders the exceptions, we skip them
        if not success:
            return super().render(data, accepted_media_type, renderer_context)

        response = {
            "success": success
        }

        # Check for pagination
        if isinstance(data, Iterable) and "pagination" in data and "data" in data:
            pagination = data.pop('pagination')
            data = data.pop('data')
            response.update({'pagination':pagination})

        response.update({"data": data})

        return super().render(response, accepted_media_type, renderer_context)