# from marshmallow import Schema, fields, validate, ValidationError

# class InteractionSchema(Schema):
#     unique_place_id = fields.Str(required=True)
#     swiped_left = fields.Bool(required=True)
#     time_viewing = fields.Int(required=True)
#     pressed_share = fields.Bool(required=True)
#     pressed_save = fields.Bool(required=True)

# class RecordActivitySchema(Schema):
#     interactions = fields.List(fields.Nested(InteractionSchema), required=True)



from marshmallow import Schema, fields, validate, ValidationError

class InteractionSchema(Schema):
    time_viewing = fields.Float(required=True)  # Changed from Int to Float
    pressed_details = fields.Bool(required=True)  # New field
    pressed_share = fields.Bool(required=True)
    pressed_save = fields.Bool(required=True)
    

class RecordActivitySchema(Schema):
    interactions = fields.Dict(keys=fields.Int(), values=fields.Nested(InteractionSchema), required=True)
