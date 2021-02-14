from datetime import date
from wtforms import Form, StringField, DateField, DecimalField, HiddenField, SelectField, validators


class ExpenseForm(Form):
    class Meta:
        locales = ['de']

    PAYER_CHOICES = [('Dierk', 'Dierk'), ('Jochen', 'Jochen')]

    id = HiddenField('Id')
    description = StringField('Beschreibung', [validators.DataRequired(), validators.Length(min=3, max=255)], default='')
    amount = DecimalField('Betrag', [validators.DataRequired()], use_locale=True)
    payer = SelectField(label='Zahler', choices=PAYER_CHOICES, default='D')
    date = DateField('Datum', [validators.DataRequired()], format='%d.%m.%Y', default=date.today())
