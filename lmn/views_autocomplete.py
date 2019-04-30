from dal import autocomplete

from .models import Venue, Artist, Note

# This errors out right now.

class VenueAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        # TODO: This always returns false, must fix and then handle the resulting error
        #if not self.request.user.is_authenticated:
        #    return Venue.objects.none()

        qs = Venue.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
