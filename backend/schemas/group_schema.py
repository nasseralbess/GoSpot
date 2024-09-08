from marshmallow import Schema, fields, validate, ValidationError
from schemas.general_schema import GeneralPreferencesSchema, InteractionSchema




class GroupSchema(Schema):
    group_id = fields.Int(required=True)
    creator = fields.Int(required=True)
    group_name = fields.Str(required=True)
   
class addGroupSchema(Schema): 
    group_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

class GroupInteractionSchema(Schema):
    group_id = fields.Int(required=True)
    interaction = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(InteractionSchema),
        required=True
    )

