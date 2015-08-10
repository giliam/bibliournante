from django.db import models
from django.contrib.auth.models import User
from library.models import Book
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User)
    informations = models.TextField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '0123456789'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=25)

    def __unicode__(self):
        return u"Profile of {0}".format(self.user.username)

class Lending(models.Model):
    borrower = models.ForeignKey(User,blank=True,verbose_name=_("borrower"))
    book = models.ForeignKey(Book,verbose_name=_("book"))
    status = models.BooleanField(default=False,verbose_name=_("status"),help_text=_("is it lent now ?"))
    beginning_date = models.DateTimeField(_('beginning date of the lending'),blank=True,null=True)
    end_date = models.DateTimeField(_('end date of the lending'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return unicode(self.borrower) + u" borrowed " + unicode(self.book)