class Quote(object):
    
    def __init__(self, recipient, quote):
        self.quote = '@{RECIPIENT} {QUOTE}'.format(RECIPIENT=recipient, QUOTE=quote)
    
    def __unicode__(self):
        return self.quote
    
    def __str__(self):
        return unicode(self).encode('UTF-8')
    
    def __repr__(self):
        return unicode(self)