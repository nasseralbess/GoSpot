from marshmallow import Schema, fields, validate, ValidationError
from schemas.general_schema import GeneralPreferencesSchema, InteractionSchema
# For adding a new users
# Customised validation for adding new users


class UserSchema(Schema):
    user_id = fields.Int(required=True)
    general_preferences = fields.Nested(GeneralPreferencesSchema, required=True)
    location_specific = fields.Dict(required=True)
    friends = fields.List(fields.Str(), required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=0))
    
# For adding interactions 

class UserInteractionSchema(Schema):
    user_id = fields.Int(required=True)
    interaction = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(InteractionSchema),
        required=True
    )


# For updating user preference 
class UpdatePreferencesSchema(Schema):
    user_id = fields.Raw(required=True)
    new_preferences = fields.Nested(GeneralPreferencesSchema, required=True)




