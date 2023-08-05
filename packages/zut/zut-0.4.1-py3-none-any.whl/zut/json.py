from __future__ import annotations
import re, json
from datetime import datetime, date

def extended_json_decode_hook(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = extended_json_decode_hook(value)

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = extended_json_decode_hook(value)

    elif isinstance(obj, str):
        if len(obj) < 10:
            return obj # ignore
        
        if re.match(r'^\d{4}-\d{2}-\d{2}$', obj):
            # date only
            return datetime.strptime(obj, "%Y-%m-%d").date()
        
        m = re.match(r'^(\d{4}-\d{2}-\d{2}T)(\d{2}:\d{2}:\d{2})(\.\d{3,6})?(Z|[\+\-]\d{2}:\d{2})?$', obj)
        if not m:
            return obj # ignore

        datepart = m.group(1) # mandatory
        timepart = m.group(2) # mandatory
        microsecondpart = m.group(3) # optional
        timezone = m.group(4) # optional
        
        # adapt timezone: replace 'Z' with +0000, or +XX:YY with +XXYY
        if timezone == 'Z':
            timezone = '+0000'
        elif timezone:
            timezone = timezone[:-3] + timezone[-2:]
        
        # NOTE: we don't decode XX:XX:XX into a time: too much risky that it's not actually a time
        # if not datepart:
        #     # time only: we only handle non-timezone-aware times, see: DjangoJSONEncoder
        #     if timezone:
        #         return obj

        #     if microsecondpart:
        #         return time.strptime(f"{timepart}{microsecondpart}", "%H:%M:%S.%f")
        #     else:
        #         return time.strptime(f"{timepart}", "%H:%M:%S")

        # datetime
        if microsecondpart:
            return datetime.strptime(f"{datepart}{timepart}{microsecondpart}{timezone}", "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            return datetime.strptime(f"{datepart}{timepart}{timezone}", "%Y-%m-%dT%H:%M:%S%z")

    return obj


class ExtendedJSONDecoder(json.JSONDecoder):
    """
    JSONDecoder subclass that knows how to decode date/time, decimal types, and UUIDs.
    Reverse of: ExtendedJSONEncoder.
    Usage example: json.loads(data, cls=ExtendedJSONDecoder)
    """
    def __init__(self, **kwargs):
        if not 'object_hook' in kwargs:
            kwargs['object_hook'] = extended_json_decode_hook
        super().__init__(**kwargs)


class ExtendedJSONEncoder(json.JSONEncoder):
    """
    Adapted from: django.core.serializers.json.DjangoJSONEncoder
    Usage example: json.dumps(data, indent=2, cls=ExtendedJSONEncoder)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            r = o.isoformat()
            if o.microsecond and o.microsecond % 1000 == 0:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, date):
            return o.isoformat()
        # elif isinstance(o, datetime.time):
        #     if is_aware(o):
        #         raise ValueError("JSON can't represent timezone-aware times.")
        #     r = o.isoformat()
        #     if o.microsecond:
        #         r = r[:12]
        #     return r
        # elif isinstance(o, datetime.timedelta):
        #     return duration_iso_string(o)
        # elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
        #     return str(o)
        else:
            return super().default(o)
