from wtforms import Form, StringField, DateField, DecimalField, HiddenField, validators

class ExpenseForm(Form):
    id = HiddenField('Id')
    description = StringField('Beschreibung', [validators.DataRequired(), validators.Length(min=3, max=255)])
    amount = DecimalField('Betrag', [validators.DataRequired()], places=2)
    payer = StringField('Zahler', [validators.DataRequired(), validators.Length(min=3, max=32)])
    date = DateField('Datum', [validators.DataRequired()], format='%d.%m.%Y')