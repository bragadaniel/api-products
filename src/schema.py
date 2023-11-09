from marshmallow import Schema, fields


class CarSchema(Schema):
    make = fields.Str(required=True)
    year = fields.Integer(required=True)
    model = fields.Str()
    id = fields.Str()
