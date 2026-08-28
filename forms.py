from flask_wtf import FlaskForm 
from wtforms import IntegerField, SubmitField

class TierForm(FlaskForm):
    mmpOneCutOff = IntegerField('MMP Tier 1 Cutoff', default=0)
    mmpTwoCutOff = IntegerField('MMP Tier 2 Cutoff', default=0)
    wmpOneCutOff = IntegerField('WMP Tier 1 Cutoff', default=0)
    wmpTwoCutOff = IntegerField('WMP Tier 2 Cutoff', default=0)
    save = SubmitField('Save')