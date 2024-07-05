from marshmallow import Schema, fields, validate, ValidationError

class InteractionSchema(Schema):
    unique_place_id = fields.Str(required=True)
    swipe_left = fields.Bool(required=True)
    time_spent_looking = fields.Int(required=True)
    pressed_share = fields.Bool(required=True)
    saved_place = fields.Bool(required=True)

class RecordActivitySchema(Schema):
    interactions = fields.List(fields.Nested(InteractionSchema), required=True)