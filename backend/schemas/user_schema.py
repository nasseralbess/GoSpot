from marshmallow import Schema, fields, validate, ValidationError

# For adding a new users
# Customised validation for adding new users
def validate_price(value):
    if value not in ["$", "$$", "$$$", "$$$$"]:
        raise ValidationError("Invalid price. Must be one of $, $$, $$$, $$$$.")
def validate_coordinates(coordinates):
    if len(coordinates) != 2:
        raise ValidationError("Coordinates must have exactly two elements.")
    for coord in coordinates:
        if not isinstance(coord, float):
            raise ValidationError("Each coordinate must be a float.")

class GeneralPreferencesSchema(Schema):
    price = fields.Str(required=True, validate=validate_price)
    categories = fields.List(fields.Str(), required=True)
    coordinates = fields.List(fields.Float(), required=True, validate=validate_coordinates)

class UserSchema(Schema):
    user_id = fields.Int(required=True)
    general_preferences = fields.Nested(GeneralPreferencesSchema, required=True)
    location_specific = fields.Dict(required=True)
    friends = fields.List(fields.Str(), required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=0))
    
# For adding interactions 
class InteractionSchema(Schema):
    time_viewing = fields.Float(required=True)
    pressed_share = fields.Boolean(required=False)
    pressed_save = fields.Boolean(required=True)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))

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

