from wtforms import Form
from wtforms import StringField, validators, IntegerField
from wtforms.fields import EmailField

#=======Form Student======#
class Student_form(Form):
    id = StringField('Id')
    names = StringField('Names')
    surnames = StringField('Surnames')
    email = EmailField('Email')
    phone = IntegerField('Phone')

#=======Form Course======#
class Course_form(Form):
    name = StringField('Name',
                        [
                            validators.DataRequired()
                        ]
                    )
    credits = IntegerField('Credits',
                            [
                                validators.DataRequired()
                            ]
                        )
