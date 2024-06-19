from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    phone = fields.Str()
    name = fields.Str()
    username = fields.Str()
    password = fields.Str(required=True, load_only=True)
    
