from marshmallow import Schema, fields, validate, ValidationError



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

class InteractionSchema(Schema):
    time_viewing = fields.Float(required=True)
    pressed_share = fields.Boolean(required=False)
    pressed_save = fields.Boolean(required=True)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))
