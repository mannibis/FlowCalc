from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CalcForm(FlaskForm):
    pipe_diameter_field = StringField('Pipe Diameter (inches)', validators=[DataRequired()])
    delta_p_field = StringField('Pressure Drop (psig)', validators=[DataRequired()])
    pipe_length_field = StringField('Pipe Length (feet)', validators=[DataRequired()])
    submit = SubmitField('Calculate Flows')
