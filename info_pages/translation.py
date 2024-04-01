from modeltranslation.translator import TranslationOptions, register
from .models import LegalDocument, Team, Partners, Guarantees, AboutUs, ContactInfo, SocialNetwork, PhoneNumber

@register(LegalDocument)
class LegalDocumentTranslationOptions(TranslationOptions):
    fields = ('name', 'text',)  # Укажите поля, которые требуется перевести

@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ('name', 'position',)  # Укажите поля, которые требуется перевести

@register(Partners)
class PartnersTranslationOptions(TranslationOptions):
    fields = ('name',)  # Укажите поля, которые требуется перевести

@register(Guarantees)
class GuaranteesTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)  # Укажите поля, которые требуется перевести

@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)  # Укажите поля, которые требуется перевести

@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('address', 'address_url',)  # Укажите поля, которые требуется перевести

@register(SocialNetwork)
class SocialNetworkTranslationOptions(TranslationOptions):
    fields = ('name',)  # Укажите поля, которые требуется перевести

@register(PhoneNumber)
class PhoneNumberTranslationOptions(TranslationOptions):
    fields = ('phone_number',)  # Укажите поля, которые требуется перевести
