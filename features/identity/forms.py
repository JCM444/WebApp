from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class DisplayNameForm(FlaskForm):
    display_name = StringField(
        "Anzeigename",
        validators=[DataRequired(), Length(max=100)],
    )
    submit = SubmitField("Weiter")
