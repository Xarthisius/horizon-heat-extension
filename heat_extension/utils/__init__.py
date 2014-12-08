

from heat_extension.utils.heat import get_templates 
from heat_extension.utils.heat import get_environments
from heat_extension.utils.heat import get_template_data 
from heat_extension.utils.heat import get_environment_data 

__all__ = [
    "get_templates",
    "get_environments",
    "get_template_data",
    "get_environment_data",
]

from json import JSONEncoder


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if set(['quantize', 'year']).intersection(dir(obj)):
            return str(obj)
        elif hasattr(obj, 'next'):
            return list(obj)
        return JSONEncoder.default(self, obj)