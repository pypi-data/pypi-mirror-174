from marshmallow import (
    Schema,
    fields,
    validate,
)


class ActionLogResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    action_type = fields.String(required=True)
    endpoint = fields.String(required=True)
    payload = fields.String(required=True)
    timestamp = fields.DateTime(dump_only=True)
