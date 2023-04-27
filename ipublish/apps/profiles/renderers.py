from ipublish.apps.core.renderers import IprofileJSONRenderer

class ProfileJsonRenderer(IprofileJSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'